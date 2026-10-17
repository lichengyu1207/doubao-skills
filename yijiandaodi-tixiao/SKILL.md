---
name: yijiandaodi-tixiao
description: AI 操作安全审计与提效助手（一鉴到底能力融合版）。适用于：(1) 检测文本/文件/剪贴板中的敏感信息（API Key、密钥、手机号、身份证、邮箱、密码）并自动脱敏；(2) 本地安全审计与哈希链存证，每次操作留痕、不可篡改、可导出报告（给客户交付 AI 服务时自证可信）；(3) 文件与剪贴板实时监控、风险规则拦截告警；(4) AIGC 内容本地安全校验（敏感词/风险表述分级）。当用户要求"检测敏感信息/脱敏/打码/审计/存证/链式记录/监控文件/监控剪贴板/风险拦截/内容安全校验/生成安全报告"时使用本 Skill。
---

# yijiandaodi-tixiao — 一鉴到底·提效（AI 操作安全审计）

## 核心定位

把「一鉴到底（yijiandaodi）」的软件能力以轻量脚本形式融入 yihaiyoudao 技能包：**本地优先、不上传原始数据、开箱即用（纯 Python 标准库）**。与 yihaiyoudao（内容审核）配合时：先查原创性/限流，再用本技能查敏感信息与脱敏、留审计存证。

四大能力：

1. **敏感信息检测 + 脱敏**：识别 API Key / 私钥 / 手机号 / 身份证 / 邮箱 / 密码，自动打码。
2. **审计记录 + 哈希链存证**：每次操作写入链式日志（每条含上一链哈希），可验证不可篡改，一键导出报告。
3. **文件 / 剪贴板监控 + 风险拦截**：轮询监控指定目录与剪贴板，命中规则即告警。
4. **AIGC 内容本地校验**：本地分级检测敏感词与风险表述，不上传原文。

执行标准（交付前必须满足）：

| 维度 | 标准 |
|---|---|
| 检测覆盖 | 6 类敏感信息（API Key/私钥/手机号/身份证/邮箱/密码）+ 可自定义规则 |
| 脱敏规则 | 保留首尾、中间打码；密钥类只留前缀标识 |
| 存证完整 | 每条审计记录含 ts/操作/数据哈希/上一链哈希/本链哈希 |
| 本地优先 | 全程不联网、不上传原始数据；脚本仅用 Python 标准库 |

## 分支判定（收到任务先判定类型）

1. **检测并脱敏一段文本/内容** → `check`：`python scripts/yjd.py check "待检测文本"`
2. **给一次 AI 操作留审计存证** → `audit`：`python scripts/yjd.py audit --op "操作名" --data "内容"`
3. **验证/回看审计链** → `verify`：`python scripts/yjd.py verify`
4. **监控文件或剪贴板** → `watch`：`python scripts/yjd.py watch --dir 目录` / `--clipboard`
5. **导出合规/交付报告** → `report`：`python scripts/yjd.py report`
6. **只做 AIGC 内容安全校验（不脱敏）** → `check --mode safe`：仅输出风险分级

## 脚本用法（scripts/yjd.py）

```
python scripts/yjd.py check "文本"              # 检测+脱敏+风险分级（默认模式）
python scripts/yjd.py check "文本" --mode safe  # 仅内容安全校验，不打码
python scripts/yjd.py audit --op "生成文章" --data "全文摘要或原文"
python scripts/yjd.py verify                     # 校验审计链完整性（防篡改）
python scripts/yjd.py watch --dir D:\素材       # 轮询目录内新增文本/常见文档
python scripts/yjd.py watch --clipboard         # 轮询剪贴板（Windows 自动读取）
python scripts/yjd.py report                     # 导出 Markdown 审计报告
python scripts/yjd.py --rules 你的规则.json      # 自定义规则（见下）
```

- 规则文件格式（可选，默认内置基础规则）：`{"sensitive": [{"name":"手机号","pattern":"1[3-9]\\d{9}","mask":"保留首尾"}], "riskwords": ["高风险词1","中风险词2"]}`
- 日志与报告默认写到技能内 `logs/` 目录；可用 `--logdir 路径` 改位置。

## 与 yihaiyoudao 的组合用法

- **发内容前**：yihaiyoudao 审原创性/限流 → yijiandaodi-tixiao 查敏感信息并脱敏 → 留一条 audit 存证。
- **给客户交付 AI 服务**：每次交付用 `audit` 留链式存证，月底 `report` 导出报告，作为可信交付凭证（配合一鉴到底桌面软件更完整）。

## 底线（不可违反）

- 全部本地完成：不上传原文、不联网、不调用外部 API；学习与日志只存本机。
- 脱敏结果仍要人工复核：机器打码不替代你的判断。
- 不承诺绝对安全：本技能是"提效助手"，真正的深度安全场景请用一鉴到底桌面软件与企业版。
- 涉及他人隐私数据时，先获得授权再检测/存证。

## 参考文件

| 文件 | 内容 | 何时读取 |
|---|---|---|
| `references/risk-rules.md` | 内置敏感信息与风险词规则说明、自定义规则写法 | 自定义规则、排查漏检时 |
| `memory/learning-log.md` | 使用记录与经验沉淀 | 每周复盘、报告使用情况时 |
