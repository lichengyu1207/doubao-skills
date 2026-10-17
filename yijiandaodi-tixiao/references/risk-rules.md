# 内置规则说明（references/risk-rules.md）

## 一、敏感信息规则（默认内置 6 类）

| 类型 | 匹配特征 | 默认脱敏方式 |
|---|---|---|
| API Key | sk-、ghp_、gho_、AKIA、Bearer 后接长串 | 只留前缀 + 前 4 位，其余 `*` |
| 私钥 | BEGIN PRIVATE KEY / RSA PRIVATE KEY 块 | 整块打码，仅留首行标记 |
| 手机号 | 1[3-9]\d{9} | 前 3 后 4，中间 `****` |
| 身份证 | 18 位（末位可为 X） | 前 6 后 4，中间 `********` |
| 邮箱 | 常规邮箱格式 | 用户名前 2 位 + `***` + @域名 |
| 密码 | password/passwd/pwd/密码 等键后接值 | 值全部 `*` |

## 二、风险词分级（AIGC 本地校验基础版）

- **高风险**：与内容安全平台红线相关的表达（借贷承诺收益、医疗疗效保证、绝对化疗效/收益承诺等通用风险表述，按 `yihaiyoudao/references/risk-lexicon.md` 精神分级）。
- **中风险**：夸大词（"最""第一""100%""包治"等绝对化表述）。
- **低风险**：可替换的营销话术词。

> 内置词库是"起步级"：真正要跟平台红线对齐，请配合 yihaiyoudao 技能的 `risk-lexicon.md` 一起用，或按你自己的行业补充规则文件。

## 三、自定义规则文件写法

```json
{
  "sensitive": [
    {"name": "自定义编号", "pattern": "[A-Z]{2}\\d{6}", "mask": "前2后2"}
  ],
  "riskwords": ["绝对化词A", "夸大词B"],
  "risk_high": ["高风险表达1"]
}
```

用法：`python scripts/yjd.py check "文本" --rules 你的规则.json`

## 四、监控说明

- `watch --dir`：轮询目录，检测新增文件（.txt/.md/.csv/.json/.log）中的敏感信息，命中即告警到终端并写入告警日志。
- `watch --clipboard`：Windows 下通过 PowerShell `Get-Clipboard` 读取剪贴板文本检测（不读取图片、不记录无文本内容）；轮询间隔默认 5 秒，`--interval 秒` 可调。
- 告警只打码展示，不落原文；如需留证走 `audit`。
