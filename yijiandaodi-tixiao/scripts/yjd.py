# -*- coding: utf-8 -*-
"""yijiandaodi-tixiao 主脚本：AI 操作安全审计与提效（一鉴到底能力融合版）

子命令：
  check  检测敏感信息+脱敏+风险分级  | --mode safe 仅内容安全校验
  audit  哈希链存证一次操作          | --op 操作名 --data 内容
  verify 校验审计链完整性（防篡改）
  watch  监控目录新增文件 / 剪贴板   | --dir 路径 / --clipboard [--interval 秒]
  report 导出 Markdown 审计报告

全部本地完成：不上传、不联网、仅 Python 标准库。
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG_DIR = os.path.join(SKILL_DIR, "logs")
AUDIT_FILE = os.path.join(DEFAULT_LOG_DIR, "audit.json")
WATCH_FILE = os.path.join(DEFAULT_LOG_DIR, "watch_alerts.json")

# ---------------- 内置敏感信息规则 ----------------
DEFAULT_RULES = {
    "sensitive": [
        {"name": "API Key", "pattern": r"(?<![A-Za-z0-9])(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})(?![A-Za-z0-9])", "mask": "key"},
        {"name": "Bearer Token", "pattern": r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}", "mask": "key"},
        {"name": "私钥块", "pattern": r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----", "mask": "block"},
        {"name": "手机号", "pattern": r"(?<!\d)1[3-9]\d{9}(?!\d)", "mask": "phone"},
        {"name": "身份证", "pattern": r"(?<!\d)\d{17}[\dXx](?!\d)", "mask": "idcard"},
        {"name": "邮箱", "pattern": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "mask": "email"},
        {"name": "密码明文", "pattern": r"(?i)(password|passwd|pwd|密码|口令)\s*[=::]\s*[^\s,;]+", "mask": "password"},
    ],
    "risk_high": ["承诺收益", "稳赚", "包治", "包好", "百分百", "绝对安全", "必涨", "保过"],
    "risk_medium": ["最", "第一", "100%", "顶级", "独家", "全网首发", "永久免费"],
}


def _mask(value, kind):
    if kind == "key":
        return value[:8] + "*" * min(12, max(4, len(value) - 8))
    if kind == "block":
        return value.splitlines()[0] + "\n*****（私钥内容已打码）*****"
    if kind == "phone":
        return value[:3] + "****" + value[-4:]
    if kind == "idcard":
        return value[:6] + "********" + value[-4:]
    if kind == "email":
        local, _, domain = value.partition("@")
        return local[:2] + "***@" + domain
    if kind == "password":
        parts = re.split(r"[=::]", value, maxsplit=1)
        return parts[0] + "=" + "*" * 6
    return value


def load_rules(path=None):
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            user = json.load(f)
        merged = {"sensitive": DEFAULT_RULES["sensitive"],
                  "risk_high": DEFAULT_RULES["risk_high"],
                  "risk_medium": DEFAULT_RULES["risk_medium"]}
        merged.update(user)
        return merged
    return DEFAULT_RULES


def detect(text, rules):
    """返回 (敏感信息命中列表, 脱敏后文本, 风险分级)"""
    hits = []
    masked = text
    for rule in rules["sensitive"]:
        for m in re.finditer(rule["pattern"], masked):
            hits.append({"type": rule["name"], "sample": _mask(m.group(0), rule["mask"])})
            masked = masked.replace(m.group(0), _mask(m.group(0), rule["mask"]))
    risk_high = [w for w in rules["risk_high"] if w in text]
    risk_med = [w for w in rules["risk_medium"] if w in text]
    return hits, masked, {"high": risk_high, "medium": risk_med}


def sha256(s):
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def _load_audit():
    if not os.path.exists(AUDIT_FILE):
        return []
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_audit(records):
    os.makedirs(os.path.dirname(AUDIT_FILE), exist_ok=True)
    with open(AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)


def cmd_audit(args):
    records = _load_audit()
    seq = len(records) + 1
    prev = records[-1]["hash"] if records else "GENESIS"
    ts = datetime.now().isoformat(timespec="seconds")
    data_hash = sha256(args.data)
    chain = sha256(f"{seq}|{ts}|{args.op}|{data_hash}|{prev}")
    records.append({"seq": seq, "ts": ts, "op": args.op, "data_hash": data_hash,
                    "prev_hash": prev, "hash": chain})
    _save_audit(records)
    print(f"✓ 已存证 第{seq}条: {args.op} | 数据哈希 {data_hash[:16]}… | 链哈希 {chain[:16]}…")


def cmd_verify(args):
    records = _load_audit()
    if not records:
        print("审计链为空。先用 audit 记录操作。")
        return
    ok = True
    for i, r in enumerate(records):
        expect_prev = records[i - 1]["hash"] if i > 0 else "GENESIS"
        chain = sha256(f"{r['seq']}|{r['ts']}|{r['op']}|{r['data_hash']}|{r['prev_hash']}")
        if r["prev_hash"] != expect_prev or r["hash"] != chain:
            ok = False
            print(f"✗ 第{r['seq']}条 链被破坏!")
        else:
            print(f"✓ 第{r['seq']}条 {r['op']} 链校验通过 ({r['ts']})")
    print("审计链完整性:", "OK，不可篡改" if ok else "FAILED")


def cmd_report(args):
    records = _load_audit()
    if not records:
        print("暂无审计记录，无法生成报告。")
        return
    lines = ["# AI 操作审计报告", "",
             f"- 生成时间：{datetime.now().isoformat(timespec='seconds')}",
             f"- 记录总数：{len(records)} 条",
             f"- 链式存证：哈希链（每条含上一链哈希，不可篡改）", "",
             "## 操作明细", "", "| # | 时间 | 操作 | 数据哈希 | 链哈希 |", "|---|---|---|---|---|"]
    for r in records:
        lines.append(f"| {r['seq']} | {r['ts']} | {r['op']} | {r['data_hash'][:12]}… | {r['hash'][:12]}… |")
    out = os.path.join(DEFAULT_LOG_DIR, f"audit_report_{time.strftime('%Y%m%d_%H%M%S')}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ 报告已导出: {out}")


def cmd_check(args):
    rules = load_rules(args.rules)
    hits, masked, risk = detect(args.text, rules)
    if args.mode == "safe":
        print(f"内容安全校验: 高风险 {len(risk['high'])} 项 / 中风险 {len(risk['medium'])} 项")
        for w in risk["high"]:
            print(f"  [高] {w}")
        for w in risk["medium"]:
            print(f"  [中] {w}")
        return
    print(f"敏感信息命中: {len(hits)} 处")
    for h in hits:
        print(f"  [{h['type']}] {h['sample']}")
    print("风险分级:", f"高{len(risk['high'])}项 {risk['high']} | 中{len(risk['medium'])}项 {risk['medium']}" if (risk["high"] or risk["medium"]) else "无")
    print("----- 脱敏后文本 -----")
    print(masked)


def _watch_file(path, rules):
    hits, _, _ = detect(path, rules) if False else (None, None, None)
    # 文件内容检测
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return None
    hits, _, risk = detect(content, rules)
    if hits or risk["high"]:
        return {"file": os.path.basename(path), "hits": [h["type"] for h in hits],
                "high_risk": risk["high"], "ts": datetime.now().isoformat(timespec="seconds")}
    return None


def cmd_watch(args):
    rules = load_rules(args.rules)
    os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
    alerts = []
    if os.path.exists(WATCH_FILE):
        try:
            with open(WATCH_FILE, "r", encoding="utf-8") as f:
                alerts = json.load(f)
        except Exception:
            alerts = []
    seen = {a["file"] for a in alerts} if alerts else set()
    print(f"监控启动（{args.directory or '剪贴板'}）… Ctrl+C 停止")
    try:
        while True:
            if args.directory:
                for root, _, files in os.walk(args.directory):
                    for fn in files:
                        if fn.lower().endswith((".txt", ".md", ".csv", ".json", ".log")) and fn not in seen:
                            alert = _watch_file(os.path.join(root, fn), rules)
                            if alert:
                                alerts.append(alert)
                                seen.add(fn)
                                print(f"⚠ 告警 {alert['ts']}: {alert['file']} 命中 {alert['hits']} 高险 {alert['high_risk']}")
            else:
                clip = _read_clipboard()
                if clip:
                    hits, _, risk = detect(clip, rules)
                    if hits or risk["high"]:
                        print(f"⚠ 剪贴板告警: {[h['type'] for h in hits]} 高险 {risk['high']}（已打码展示，未落原文）")
            with open(WATCH_FILE, "w", encoding="utf-8") as f:
                json.dump(alerts, f, ensure_ascii=False, indent=1)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n监控已停止。告警记录: " + str(len(alerts)) + " 条")


def _read_clipboard():
    try:
        if sys.platform.startswith("win"):
            r = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
                               capture_output=True, text=True, timeout=10)
            return r.stdout.strip() if r.returncode == 0 else ""
        r = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception:
        return ""


def main():
    p = argparse.ArgumentParser(prog="yjd", description="一鉴到底·提效：AI 操作安全审计")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="检测敏感信息+脱敏+风险分级")
    c.add_argument("text", nargs="?", default="")
    c.add_argument("--mode", choices=["full", "safe"], default="full")
    c.add_argument("--rules")
    c.set_defaults(func=cmd_check)
    a = sub.add_parser("audit", help="哈希链存证")
    a.add_argument("--op", required=True)
    a.add_argument("--data", required=True)
    a.set_defaults(func=cmd_audit)
    v = sub.add_parser("verify", help="校验审计链")
    v.set_defaults(func=cmd_verify)
    r = sub.add_parser("report", help="导出审计报告")
    r.set_defaults(func=cmd_report)
    w = sub.add_parser("watch", help="监控目录/剪贴板")
    w.add_argument("--dir", dest="directory")
    w.add_argument("--clipboard", action="store_true")
    w.add_argument("--interval", type=int, default=5)
    w.add_argument("--rules")
    w.set_defaults(func=cmd_watch)
    args = p.parse_args()
    if args.cmd == "check" and not args.text:
        p.error("check 需要提供待检测文本（用引号包起来）")
    if args.cmd == "watch" and not args.directory and not args.clipboard:
        p.error("watch 需要 --dir 目录 或 --clipboard")
    args.func(args)


if __name__ == "__main__":
    main()
