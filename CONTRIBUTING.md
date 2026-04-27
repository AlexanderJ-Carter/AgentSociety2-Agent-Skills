# Contributing

## 你可以贡献什么

- 新技能（`skills/<name>/SKILL.md` + 可选 `references/`、`scripts/`）
- 现有技能的理论依据补全（`references/*.md`）
- 脚本的确定性基线（用于减少 LLM 重复计算）
- 文档与示例（`docs/*.md`）

## 技能目录约定

```text
skills/<skill_name>/
  SKILL.md
  references/        # 理论依据与模型说明（推荐）
  scripts/           # 确定性更新脚本（可选）
  assets/            # 图片/数据（可选）
```

## `SKILL.md` 最小规范

Frontmatter 默认只允许：

```yaml
---
name: skill_name
description: One sentence shown in the skill catalog.
---
```

正文必须可执行（面向“激活后怎么做”），不要写成论文式综述。

## 理论依据规范（强烈建议）

如果技能使用了具体曲线/模型/公式（例如遗忘曲线、Two-Process 睡眠模型、强化学习/习惯形成模型），请把：

- **模型名**
- **核心公式或更新规则**
- **变量含义与取值范围**
- **引用来源（论文/书/综述/公开资料）**

写入 `skills/<skill_name>/references/*.md`，并在 `SKILL.md` 中给出一句话指向。

## 代码与脚本风格

- 脚本优先做“确定性 baseline”，LLM 只做解释与边界情况推断。
- 不做向后兼容：发现设计更清晰的写法就直接调整。

