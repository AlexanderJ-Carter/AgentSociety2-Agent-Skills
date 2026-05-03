# Contributing

感谢你改进 AgentSociety2 Skills。这个仓库的目标不是收集长 prompt，而是维护一组可以被 AgentSociety2 / PersonAgent 发现、审查、复制和运行的 Claude Skill 风格能力模块。

## What To Contribute

- 新技能：`skills/<name>/SKILL.md` + `references/` + 可选 `scripts/`
- 现有技能的理论依据、公式、变量范围和引用补全
- 确定性 baseline 脚本，用于减少 LLM 每 tick 重复计算
- 文档、示例、集成说明和站点样式改进
- 测试、目录生成脚本和 CI 改进

## Before You Start

1. 先读 [技能规范](docs/skill_standard.md)。
2. 查重：确认没有现有技能已经覆盖你的需求。
3. 保持边界清晰：一个技能只负责一种人的能力、状态或约束。
4. 如果引入理论模型，必须补 `references/`，不要只把引用写在 README 里。

## Skill Directory Convention

```text
skills/<skill_name>/
  SKILL.md
  references/        # 理论依据与模型说明（必需）
  scripts/           # 确定性更新脚本（可选）
  assets/            # 图片/数据（可选）
```

## `SKILL.md` Requirements

Frontmatter 默认只写：

```yaml
---
name: skill_name
description: One sentence shown in the skill catalog.
---
```

正文必须面向“激活后怎么做”，不要写成论文式综述。推荐章节：

1. `## Purpose`
2. `## Internal Logic (One Sentence)`
3. `## Use When`
4. `## Procedure`
5. `## Write`
6. `## Output Schema`（如果写结构化状态）
7. `## Notes`

## Research Basis Requirements

如果技能使用了具体曲线、模型、公式或社会科学概念，请把以下内容写入 `skills/<skill_name>/references/*.md`：

- **模型名**
- **核心公式、更新规则或伪代码**
- **变量含义与取值范围**
- **默认参数和调参说明**
- **引用来源**（论文、书、综述或权威公开资料）

`SKILL.md` 里只保留简短入口，例如：

```text
Research basis: `references/research_basis.md`.
```

## Script Requirements

- 脚本优先做确定性 baseline；LLM 负责解释、边界情况和情境化判断。
- 脚本应能在本地直接运行，不依赖隐藏服务。
- 输出 JSON 应包含 `_meta.purpose` 和 `_summary` 或 `summary`。
- 不要把 API key、token、个人数据或真实敏感数据写进示例。

## Documentation Site

生成页面来自技能源文件：

```bash
python scripts/generate_skill_catalog.py
python -m mkdocs build
```

如果你改了 `skills/*/SKILL.md` 或 `references/`，请重新生成 `docs/skills/*`。

## Verification

提交前至少运行：

```bash
python -m unittest tests.test_skill_repository
python scripts/generate_skill_catalog.py
python -m mkdocs build
```

如果本机 `python` 不可用，可以使用项目 `.venv` 或可用的 Python 解释器；关键是测试和文档构建必须通过。

## Pull Request Checklist

- [ ] `SKILL.md` frontmatter 只有必要字段。
- [ ] 技能包含 `Purpose`、`Internal Logic`、`Use When`、`Procedure`、`Write`、`Notes`。
- [ ] 理论依据写在 `references/`，并包含模型、规则、变量、参数和来源。
- [ ] 新脚本有清晰命令示例，输出可解释。
- [ ] `docs/skills/*` 已重新生成。
- [ ] 没有提交密钥、个人数据、仿真参与者敏感信息或临时构建产物。

## Security and Safety

请不要通过公开 issue 披露安全问题。安全报告流程见 [SECURITY.md](SECURITY.md)。

涉及人类行为、心理、健康、制度、经济或媒介影响的技能必须写明建模边界。这个仓库用于仿真研究和软件集成，不提供医疗、法律、金融或公共政策建议。
