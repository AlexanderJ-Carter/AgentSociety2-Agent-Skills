<div class="as2-hero">
  <div>
    <span class="as2-kicker">AgentSociety2 Skills</span>
    <h1>社会人仿真技能仓库<br/>Theory-grounded skills for social human agents</h1>
  </div>
  <p>
    这是一个 ClaudeSkill 风格的公开技能库，用于构建更像真实社会人的 Agent：会饥饿和疲劳，会记住关系，会受规范和制度影响，也会学习、误信、反思和遗忘。
  </p>
  <p>
    This repository provides reusable skills, deterministic baseline scripts, and research notes for simulating believable social agents.
  </p>
</div>

## 快速开始 / Start Here

<div class="as2-grid">
  <div class="as2-card">
    <strong><a href="skills/catalog/">技能目录 / Skill Catalog</a></strong>
    <p>按运行链路和社会功能分组查看所有技能。</p>
  </div>
  <div class="as2-card">
    <strong><a href="技能说明/">技能说明 / User Guide</a></strong>
    <p>面向使用者的流程说明，解释每个技能解决什么仿真问题。</p>
  </div>
  <div class="as2-card">
    <strong><a href="theory_basis/">理论依据 / Research Basis</a></strong>
    <p>按模型查看 Ebbinghaus、ACT-R、TPB、程序正义等理论来源。</p>
  </div>
  <div class="as2-card">
    <strong><a href="skill_standard/">技能规范 / Skill Standard</a></strong>
    <p>编写新技能时使用的目录结构、状态文件和引用要求。</p>
  </div>
</div>

## 推荐运行链路 / Recommended Runtime Flow

<div class="as2-flow">
observation -> domain skills -> cognition -> plan -> memory
</div>

领域技能可以按需要启用。身体节律、经济约束、社会关系、规范压力、学习、媒介素养、制度互动等状态都会写入 `state/*.json`，再由 `cognition` 综合成情绪和意图。

Domain skills can be enabled as needed. They write structured state files such as `state/physiology.json`, `state/relationships.json`, `state/media_literacy.json`, or `state/institutions.json`; `cognition` then integrates these signals into emotion and intention.

## 这个仓库有什么 / What You Get

<div class="as2-grid">
  <div class="as2-card">
    <strong>ClaudeSkill-style skills</strong>
    <p>每个技能一个目录，入口是 `SKILL.md`，适合复制进 Agent workspace。</p>
  </div>
  <div class="as2-card">
    <strong>Deterministic baselines</strong>
    <p>`scripts/*.py` 处理可重复计算，减少 LLM 每 tick 临场编公式。</p>
  </div>
  <div class="as2-card">
    <strong>Research notes</strong>
    <p>`references/*.md` 写清楚模型、公式、变量范围、默认参数和引用。</p>
  </div>
  <div class="as2-card">
    <strong>Bilingual docs</strong>
    <p>公开页面尽量同时提供中文解释和 English summary，方便不同用户浏览。</p>
  </div>
</div>

## 适合谁使用 / Intended Users

- Agent simulation researchers who need inspectable behavior modules.
- Builders integrating skills into AgentSociety-style PersonAgent workflows.
- Developers who want scripts and schemas instead of purely prompt-based behavior.
- 需要公开、可审查、可复用技能库的社会仿真项目。

## 设计与研究 / Design Notes

- `agent_context_design.md`：`AGENT.md` 与 workspace 自描述机制。
- `human_agent_research.md`：社会人、生理节律、心理与行为建模要点。
- `agent_framework_design_research.md`：更偏框架层的方案调研与对比。
