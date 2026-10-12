# doubao-skills

豆包办公（Doubao Work）用户技能集（User Skills），采用通用 **Agent Skills（SKILL.md）** 格式，可跨平台使用。

## 技能列表

| 技能 | 说明 |
|---|---|
| [zhanlue-peipao](zhanlue-peipao/) | 战略陪跑教练：自媒体/创业/副业/企业四场景 × 10万/100万/1000万三档目标的诊断、路线图、里程碑与复盘 |
| [qingchuang-shizhan](qingchuang-shizhan/) | 内容创业与轻创业实操教练：定位、内容生产、多平台分发、获客私域、合规变现、现金流风控 |

## 平台支持

仓库已配置 Claude Code marketplace 清单（`.claude-plugin/marketplace.json`），各平台安装方式如下：

### Claude Code（插件市场方式）
```bash
claude plugin marketplace add lichengyu1207/doubao-skills
claude plugin install zhanlue-peipao@doubao-skills
claude plugin install qingchuang-shizhan@doubao-skills
```
或直接复制技能文件夹到技能目录：
```bash
git clone https://github.com/lichengyu1207/doubao-skills.git
cp -r zhanlue-peipao ~/.claude/skills/
```

### Gemini CLI
```bash
gemini skills install https://github.com/lichengyu1207/doubao-skills.git
```

### GitHub CLI
```bash
gh skill install lichengyu1207/doubao-skills zhanlue-peipao
gh skill install lichengyu1207/doubao-skills qingchuang-shizhan
```

### Claude 系（npx skills）
```bash
npx skills add https://github.com/lichengyu1207/doubao-skills.git --skill zhanlue-peipao
npx skills add https://github.com/lichengyu1207/doubao-skills.git --skill qingchuang-shizhan
```

### AWS Bedrock AgentCore
技能源选择 **Git (HTTPS)**，仓库地址填 `https://github.com/lichengyu1207/doubao-skills.git`，子目录填 `zhanlue-peipao` 或 `qingchuang-shizhan`。

### VS Code / GitHub Copilot
克隆仓库后，把技能文件夹放入项目的 `.github/skills/`、`.claude/skills/` 或用户级 `~/.copilot/skills/`、`~/.claude/skills/`。

### Cursor / 其他平台
```bash
git clone https://github.com/lichengyu1207/doubao-skills.git
# 将 zhanlue-peipao / qingchuang-shizhan 文件夹复制到对应平台技能目录，如 ~/.cursor/skills/
```

### 豆包办公（Doubao Work）
把技能文件夹复制到用户技能目录 `workspace/.user_skills/` 下即可自动加载。

## 使用触发示例

- "帮我规划从零到年入100万的自媒体路线" → zhanlue-peipao
- "副业如何起步并稳定变现" → qingchuang-shizhan

## 说明

- 所有技能坚持：真实宣传、合规经营、不承诺收益、不碰灰产。
- 技能内容持续迭代，欢迎 issue 反馈。
- 仓库结构：`skills/` 布局即仓库根目录（每个技能文件夹含 `SKILL.md` + `references/` + 可选 `.claude-plugin/plugin.json`），兼容主流平台技能格式。
