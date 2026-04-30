# Memory — Research Basis

本技能把“长时记忆维护”拆成两层：写入（LLM 决定哪些值得记）与维护（脚本按模型衰减、检索激活与清理）。

## 采用的遗忘曲线：Ebbinghaus Forgetting Curve（指数衰减形式）

我们使用指数衰减作为可控、可解释、可实现的 baseline：

\[
R(t)=\exp\left(-\frac{t}{S \cdot k}\right)
\]

- \(R(t)\)：保留度（retention），范围 \([0,1]\)
- \(t\)：距离该记忆创建的 tick 数
- \(S\)：强度系数（strength），控制衰减速度（默认建议 \(S=100\) ticks）
- \(k\)：重要性乘子（importance multiplier），例如：high=1.5、medium=1.0、low=0.5

### 为什么选指数形式

- **实现简单**：只需要 tick 差与少量参数
- **可解释**：衰减速度与“强度/重要性”可直觉调参
- **稳定**：不会出现奇异点或不可控的长尾

### 强化（rehearsal / retrieval practice）

被检索或反复提及的记忆会更不容易忘。脚本可用两种简单策略之一：

1) **加性强化**：访问一次使 \(R\leftarrow \min(0.95, R+\Delta)\)
2) **等效时间回拨**：访问一次使 \(t\leftarrow \max(0, t-\tau)\)

仓库脚本默认采用简单可控的加性强化（见 `../scripts/memory_maintenance.py`）。

## ACT-R Base-Level Learning：多次经历/回忆的叠加

只用“创建时间”会低估社会仿真的一个关键事实：一个人反复见到的同事、路线、承诺、冲突，即使第一次发生很久以前，也应当比一次性事件更容易被想起。

因此维护脚本额外计算 ACT-R 风格的 base-level activation：

\[
B_i=\ln\left(\sum_j t_j^{-d}\right)
\]

- \(B_i\)：记忆块 \(i\) 的基础激活。
- \(t_j\)：距离第 \(j\) 次呈现/检索的 tick 间隔，最小按 1 处理，避免除零。
- \(d\)：衰减参数，默认 \(0.5\)。
- 多次呈现以求和方式叠加，因此重复经历会形成更高激活。

脚本实现中还加了两个仿真友好的项：

\[
B_i' = B_i + \ln(k) + 0.08 \cdot \min(10, access\_count)
\]

- \(k\)：重要性乘子，沿用 high=1.5、medium=1.0、low=0.5。
- `access_count`：检索次数，用小幅 bonus 表示 retrieval practice。

再用 logistic 函数把激活转成可解释概率：

\[
P(retrieve)=\frac{1}{1+\exp(-(B_i' - \theta))}
\]

最后：

\[
retention=\max(R_{Ebbinghaus}, P(retrieve))
\]

这样做的好处是：

- 单次低价值事件仍会自然淡出；
- 被反复遇到的人、地点、规则、承诺会更稳定；
- 模拟中“熟悉感”和“社会连续性”不必完全依赖 LLM 临场回忆。

## Spacing effects：间隔复习服务于保持目标

记忆不应该只有“永久保存/立刻遗忘”两个状态。分散学习研究显示，复习间隔和最终保持目标共同影响长期记忆；想保持越久，复习间隔通常也应越长。

仿真中可以给重要记忆加可选调度字段：

```text
next_review_tick = current_tick + round(target_retention_interval * spacing_ratio)
```

- `_target_retention_interval`：这条记忆希望保持多久。
- `_spacing_ratio`：默认可从 `0.1` 到 `0.3` 起步。
- `_next_review_tick`：下一次主动检索/复习时间。
- `_last_retrieval_success`：上次检索是否成功。

更新规则：

- 近期要用的信息：间隔短。
- 长期要用的信息：间隔长。
- 成功回忆：增加 `_access_count`，追加 `_presentations`，并延长下一次间隔。
- 回忆失败：降低有效保留度或缩短下一次间隔。
- 刚刚成功回忆后马上重复：增益较小，避免无限刷高强度。

## 参数建议

| 参数 | 默认 | 含义 | 调参方向 |
|------|------|------|----------|
| `AGENT_MEMORY_STRENGTH` | `100` | Ebbinghaus 指数衰减强度 | tick 很短时调大 |
| `AGENT_MEMORY_ACTR_DECAY` | `0.5` | ACT-R 呈现项的幂律衰减 | 想让重复经历更快淡出时调大 |
| `AGENT_MEMORY_RETRIEVAL_THRESHOLD` | `-2.5` | retrieval probability 的阈值 | 想更严格保留时调高 |
| `AGENT_MEMORY_MAX_ENTRIES` | `1000` | 文件容量上限 | 大规模仿真按成本调节 |

## 参考

- Hermann Ebbinghaus. *Memory: A Contribution to Experimental Psychology* (1885).
- Anderson, J. R. & Schooler, L. J. (1991). Reflections of the environment in memory.
- ACT-R base-level learning equation: repeated presentations add as power-law terms; common decay default \(d=0.5\).
- Roediger, H. L. & Karpicke, J. D. (2006). Test-enhanced learning: taking memory tests improves long-term retention.
- 现代 retrieval practice 综述可用于解释“检索强化”。
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354-380. DOI: `10.1037/0033-2909.132.3.354`.
- Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H. (2008). Spacing effects in learning: A temporal ridgeline of optimal retention. *Psychological Science*, 19(11), 1095-1102. DOI: `10.1111/j.1467-9280.2008.02209.x`.
