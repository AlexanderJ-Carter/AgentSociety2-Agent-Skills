# 理论依据索引 / Research Basis Index

本页给使用者一个快速入口：每个技能为什么这样设计、对应哪些心理学/社会科学/认知科学模型、在哪里查看详细公式和参数。

This page gives users a quick map from each simulation skill to the theory, model, formula, and parameter notes behind it. Detailed notes live in each skill's `references/` folder and are also rendered on the generated skill pages.

## 如何阅读 / How To Read This

- **技能页面 / Skill page**：`docs/skills/<skill>.md` 会自动包含 `SKILL.md` 和 `references/*.md`。
- **理论文件 / Reference file**：`skills/<skill>/references/*.md` 是源文件，适合维护和审查。
- **脚本 / Script**：如果技能有 `scripts/*.py`，公式会尽量落实到确定性 baseline，减少 LLM 每次重复“临场算数”。

## 模型总览 / Model Overview

| Skill | 中文说明 | English Summary | Theory / Model | Reference File |
|---|---|---|---|---|
| `memory` | 长时记忆衰减与检索强化 | Long-term memory decay and retrieval reinforcement | Ebbinghaus forgetting curve; ACT-R base-level learning; retrieval practice | `skills/memory/references/research_basis.md` |
| `cognition` | 情绪评估与意图选择 | Emotion appraisal and intention selection | Scherer Component Process Model; Theory of Planned Behavior; OCC-style emotion labels | `skills/cognition/references/research_basis.md` |
| `circadian` | 昼夜节律、睡眠压力、食欲节律 | Circadian rhythm, sleep pressure, appetite rhythm | Two-process sleep regulation; circadian oscillator; chronotype | `skills/circadian/references/research_basis.md` |
| `physiology` | 饥饿、口渴、疲劳、压力等身体需求 | Hunger, thirst, fatigue, stress, pain, illness | Homeostasis/allostasis; metabolic pressure; stress recovery | `skills/physiology/references/research_basis.md` |
| `health` | 疾病、疼痛、慢性压力和恢复 | Illness, pain, chronic stress, recovery | Biopsychosocial health; stress load; recovery dynamics | `skills/health/references/research_basis.md` |
| `routine` | 日常作息和习惯 | Daily routines and habits | Habit loop; cue-routine-reward; automaticity | See `SKILL.md` and script |
| `relationships` | 熟悉度、信任、喜欢、义务、冲突 | Familiarity, trust, liking, obligation, conflict | Interpersonal trust; repeated interaction; reciprocity | `skills/relationships/references/research_basis.md` |
| `norms` | 角色、规范压力、制裁和羞耻/内疚风险 | Roles, norm pressure, sanctions, shame/guilt risk | Social norms; role expectations; sanction risk | See `SKILL.md` and script |
| `economy` | 金钱、消费、工作义务、稀缺压力 | Money, consumption, work obligation, scarcity pressure | Scarcity pressure; bounded economic choice | `skills/economy/references/research_basis.md` |
| `affordance` | 行动可行性、成本、风险和阻碍 | Feasible/costly/risky/blocked actions | Ecological affordances; constraint-based planning | See `SKILL.md` and script |
| `learning` | 熟练度、保持率、自动化程度、自我效能 | Proficiency, retention, automaticity, self-efficacy | Bandura self-efficacy; habit automaticity; retention decay | `skills/learning/references/research_basis.md` |
| `moral_judgment` | 道德基础、道德情绪和修复/惩罚倾向 | Moral foundations, moral emotions, repair/punishment tendencies | Moral Foundations Theory; social intuitionist model | `skills/moral_judgment/references/research_basis.md` |
| `media_literacy` | 来源可信度、误导风险、预辟谣和信念更新 | Source credibility, misinformation risk, inoculation, belief uptake | Motivated reasoning; elaboration likelihood; inoculation theory | `skills/media_literacy/references/research_basis.md` |
| `civic_institution` | 制度互动、程序正义、合规和制度信任 | Institutional encounters, procedural justice, compliance, trust | Procedural justice; institutional legitimacy; access barriers | `skills/civic_institution/references/research_basis.md` |
| `identity` | 身份、自我概念和角色冲突 | Identity, self-concept, role conflict | Social identity and role theory | `skills/identity/references/theory.md` |
| `communication` | 对话、语气、含义和修复 | Conversation, tone, meaning, repair | Pragmatics and communication theory | `skills/communication/references/theory.md` |

## 公开仓库维护约定 / Public Repository Convention

新增或修改技能时，如果使用了曲线、公式或社会科学模型，应同时更新：

When adding or modifying a skill, update all of the following if the skill uses a curve, formula, or social-science model:

1. `skills/<skill>/SKILL.md`：写清楚 tick 内部逻辑、输入、输出和脚本用法。
2. `skills/<skill>/references/*.md`：写清楚模型、公式、变量范围、默认参数和引用。
3. `skills/<skill>/scripts/*.py`：如果有确定性计算，尽量放进脚本，并在 `SKILL.md` 中说明命令。
4. `docs/技能说明.md`：给普通用户的中文说明。
5. This page: add a bilingual row if the skill introduces a new theory family.

## 关键引用 / Key References

- Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*.
- Anderson, J. R. & Schooler, L. J. (1991). Reflections of the environment in memory.
- Ajzen, I. (1991). The theory of planned behavior.
- Scherer, K. R. (2001). Appraisal considered as a process of multilevel sequential checking.
- Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change.
- Lally, P. et al. (2010). How are habits formed: Modelling habit formation in the real world.
- Haidt, J. (2001). The emotional dog and its rational tail.
- Graham, J., Haidt, J., & Nosek, B. A. (2009). Moral foundations.
- Kunda, Z. (1990). The case for motivated reasoning.
- McGuire, W. J. (1964). Inducing resistance to persuasion.
- van der Linden, S. et al. (2017). Inoculating the public against misinformation.
- Tyler, T. R. (1990/2006). *Why People Obey the Law*.
- Lipsky, M. (1980). *Street-Level Bureaucracy*.
