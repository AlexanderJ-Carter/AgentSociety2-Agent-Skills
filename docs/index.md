<div class="as2-hero">
  <div class="as2-hero__content">
    <p class="as2-kicker">AgentSociety2 Skills</p>
    <h1>社会人仿真技能仓库<br/>Theory-grounded skills for social human agents</h1>
    <p>
      ClaudeSkill 风格的公开技能库，用于构建更像真实社会人的 Agent：有身体节律、关系记忆、规范压力、经济约束，也会学习、误信、反思和遗忘。
    </p>
    <div class="as2-actions">
      <a class="as2-button as2-button--primary" href="skills/catalog/">查看技能目录</a>
      <a class="as2-button" href="skill_standard/">阅读技能规范</a>
    </div>
  </div>
  <div class="as2-hero__panel">
    <strong>Runtime flow</strong>
    <ol>
      <li><span>observe</span> 获取当前世界状态</li>
      <li><span>domain skills</span> 更新身体、关系、制度、信息等压力</li>
      <li><span>cognition</span> 汇总成情绪与意图</li>
      <li><span>plan + memory</span> 执行动作并沉淀经验</li>
    </ol>
  </div>
</div>

## Start Here

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
  <div class="as2-card">
    <strong><a href="policies/">项目治理 / Policies</a></strong>
    <p>查看许可、贡献、安全报告、引用和仿真安全边界。</p>
  </div>
</div>

## Recommended Runtime Flow

<div class="as2-flow" aria-label="Recommended runtime flow">
  <span>observation</span>
  <span>domain skills</span>
  <span>cognition</span>
  <span>plan</span>
  <span>memory</span>
</div>

领域技能可以按需要启用。身体节律、经济约束、社会关系、规范压力、学习、媒介素养、制度互动等状态都会写入 `state/*.json`，再由 `cognition` 综合成情绪和意图。

Domain skills can be enabled as needed. They write structured state files such as `state/physiology.json`, `state/relationships.json`, `state/media_literacy.json`, or `state/institutions.json`; `cognition` then integrates these signals into emotion and intention.

## What You Get

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

## Skill Groups

<div class="as2-split">
  <div>
    <h3>Core loop</h3>
    <p>每 tick 都可能运行：观察、认知、计划、记忆。</p>
  </div>
  <div>
    <h3>Body and routine</h3>
    <p>昼夜节律、饥饿疲劳、健康、日常作息和学习。</p>
  </div>
  <div>
    <h3>Social life</h3>
    <p>关系、规范、文化、沟通、身份和道德判断。</p>
  </div>
  <div>
    <h3>Constraints</h3>
    <p>金钱、行动可行性、制度接触、媒介素养和反思。</p>
  </div>
</div>

## Intended Users

- Agent simulation researchers who need inspectable behavior modules.
- Builders integrating skills into AgentSociety-style PersonAgent workflows.
- Developers who want scripts and schemas instead of purely prompt-based behavior.
- 需要公开、可审查、可复用技能库的社会仿真项目。

## Design Notes

- `agent_context_design.md`：`AGENT.md` 与 workspace 自描述机制。
- `human_agent_research.md`：社会人、生理节律、心理与行为建模要点。
- `agent_framework_design_research.md`：更偏框架层的方案调研与对比。
