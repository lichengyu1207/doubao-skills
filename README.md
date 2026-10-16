# yihaiyoudao-skills

面向自媒体、创业、副业、企业的赋能技能集，采用通用 **Agent Skills（SKILL.md）** 格式，可跨平台使用。

## ⚡ 快速开始（30 秒，不需要懂 git）

装技能**不需要克隆、不需要懂 git**。本仓库名：**`lichengyu1207/yihaiyoudao-skills`**，按你的工具选一种：

**① 对话类工具（豆包 / 扣子 / TraeWork / WorkBuddy）——最简单**
直接对你的 AI 说：「**加载 yihaiyoudao-skills 技能**（GitHub: lichengyu1207/yihaiyoudao-skills）」，AI 会按仓库拉取；或下载 zip 解压后粘贴 `SKILL.md` 全文。

**② Claude Code —— 一条命令装 4 个技能**
```bash
claude plugin marketplace add lichengyu1207/yihaiyoudao-skills
claude plugin install zhanlue-peipao@yihaiyoudao-skills
```

**③ 其他命令行工具（Gemini / GitHub CLI / npx / OpenClaw）——一条 install 命令**
```bash
gemini skills install https://github.com/lichengyu1207/yihaiyoudao-skills.git
```
（安装是工具自动完成的，命令里带上仓库地址即可，不需要你手动 git clone。）

## 技能列表

| 技能 | 说明 |
|---|---|
| [zhanlue-peipao](zhanlue-peipao/) | 战略陪跑教练：自媒体/创业/副业/企业四场景 × 10万/100万/1000万三档目标的诊断、路线图、里程碑与复盘 |
| [qingchuang-shizhan](qingchuang-shizhan/) | 内容创业与轻创业实操教练：定位、内容生产、多平台分发、获客私域、合规变现、现金流风控 |
| [content-audit-rewrite](content-audit-rewrite/) | 内容审核与原创改造：原创性判定、限流风险词库与替换、观点化改造、风格统一 |
| [pi-jev](pi-jev/) | 决策层：Jev 式自动选技能 + 模型档位路由 + 使用学习；新任务先跑它确定用哪个技能 |

## 快速安装（zip 方式）

下载本仓库的 zip 压缩包并解压，把 `zhanlue-peipao/`、`qingchuang-shizhan/`、`pi-jev/` 等技能文件夹复制到目标平台用户技能目录即可：

- 豆包办公：`workspace/.user_skills/`
- Claude Code：`~/.claude/skills/`
- Cursor：`~/.cursor/skills/`
- 其他平台：见下方「平台支持」

## 平台支持

仓库已配置 Claude Code marketplace 清单（`.claude-plugin/marketplace.json`），各平台安装方式如下：

### Claude Code（插件市场方式）
```bash
claude plugin marketplace add lichengyu1207/yihaiyoudao-skills
claude plugin install zhanlue-peipao@yihaiyoudao-skills
claude plugin install qingchuang-shizhan@yihaiyoudao-skills
claude plugin install pi-jev@yihaiyoudao-skills
```
或直接复制技能文件夹到技能目录：
```bash
git clone https://github.com/lichengyu1207/yihaiyoudao-skills.git
cp -r zhanlue-peipao ~/.claude/skills/
```

### Gemini CLI
```bash
gemini skills install https://github.com/lichengyu1207/yihaiyoudao-skills.git
```

### GitHub CLI
```bash
gh skill install lichengyu1207/yihaiyoudao-skills zhanlue-peipao
gh skill install lichengyu1207/yihaiyoudao-skills qingchuang-shizhan
gh skill install lichengyu1207/yihaiyoudao-skills pi-jev
```

### Claude 系（npx skills）
```bash
npx skills add https://github.com/lichengyu1207/yihaiyoudao-skills.git --skill zhanlue-peipao
npx skills add https://github.com/lichengyu1207/yihaiyoudao-skills.git --skill qingchuang-shizhan
npx skills add https://github.com/lichengyu1207/yihaiyoudao-skills.git --skill pi-jev
```

### AWS Bedrock AgentCore
技能源选择 **Git (HTTPS)**，仓库地址填 `https://github.com/lichengyu1207/yihaiyoudao-skills.git`，子目录填 `zhanlue-peipao` 或 `qingchuang-shizhan`。

### VS Code / GitHub Copilot
克隆仓库后，把技能文件夹放入项目的 `.github/skills/`、`.claude/skills/` 或用户级 `~/.copilot/skills/`、`~/.claude/skills/`。

## 使用触发示例

- "帮我规划从零到年入100万的自媒体路线" → zhanlue-peipao
- "副业如何起步并稳定变现" → qingchuang-shizhan
- "拿不准该用哪个技能" → pi-jev 决策层（`python pi-jev/scripts/pi_jev.py "任务"`，自动推荐技能、脚本命令与模型档位）

## 说明

- 所有技能坚持：真实宣传、合规经营、不承诺收益、不碰灰产。
- 技能内容持续迭代，欢迎 issue 反馈。
- 仓库结构：每个技能文件夹含 `SKILL.md` + `references/` + `.claude-plugin/plugin.json`，兼容主流平台技能格式；`pi-jev/` 为决策层（`SKILL.md` + `scripts/` + `memory/`，纯 Python 实现，无需 API 密钥，越用越准）。

## 版权与支持

© 2026 骇老师（AI+IP 陪跑变现操盘手）· https://github.com/lichengyu1207

- 本仓库是**开源框架**：可下载学习、可自由用于自己的业务。
- **禁止未授权转售 / 冒充原创 / 抹名分发**（详见 [LICENSE.md](LICENSE.md)）。
- 想转售？走 **C 转 B 授权**（详见 [PARTNER.md](PARTNER.md)）。
- 如果这套框架对你有帮助，**点一个 ⭐**——这是对作者最实在的支持，也是这套包持续更新的动力。
