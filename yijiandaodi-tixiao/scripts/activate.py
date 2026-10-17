# -*- coding: utf-8 -*-
"""首次激活：生成本机安装编号（与其他技能一致的规则）"""
import datetime
import os
import random
import string
import sys

def main():
    home = os.path.expanduser("~")
    base = os.path.join(home, ".yihaiyoudao")
    os.makedirs(base, exist_ok=True)
    activate_file = os.path.join(base, "activate.json")
    if os.path.exists(activate_file):
        try:
            import json
            with open(activate_file, "r", encoding="utf-8") as f:
                old = json.load(f)
            print("已激活过，编号:", old.get("code"))
            print("无需重复生成。登记状态请找作者确认。")
            return
        except Exception:
            pass
    code = "YHYD-" + datetime.date.today().strftime("%Y%m%d") + "-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6))
    import json
    with open(activate_file, "w", encoding="utf-8") as f:
        json.dump({"code": code, "ts": datetime.datetime.now().isoformat(timespec="seconds")}, f, ensure_ascii=False, indent=1)
    print("你的安装编号:", code)
    print("请发给作者骇老师登记（GitHub: lichengyu1207 / 体验群私信）。编号仅存本机，不上传。")
    print("检查: python activate.py --check 只查不重生成")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        p = os.path.join(os.path.expanduser("~"), ".yihaiyoudao", "activate.json")
        if os.path.exists(p):
            import json
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            print("已激活:", d.get("code"), "|", d.get("ts"))
        else:
            print("未激活。运行 python activate.py 生成编号。")
    else:
        main()
