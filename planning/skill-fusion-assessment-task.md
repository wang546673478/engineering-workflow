# TASK-FUSION-ASSESS-01: v3.0 Skill 融合方案评估

状态：隔离试验已完成；正式融合暂缓，实施未授权。正式 skill、检查器和提交门禁没有改变；ScopeCairn 只安装在临时目录。原评估结论保留为历史；旧任务批准不适用于本试验。

来源：用户于 2026-10-16（Asia/Shanghai）要求“认真诚实的评估我给你的md文档,看看可行性多少”。附件 SHA-256：`AD71A1ADCF1C3668C6003C54A7E902D6857D02053126F6F1D3921DD60744E39F`。比较基线为本仓库 1.4.3、提交 `82f87c4d5d48d30ed3610303a5f7864023044038`；开始时 `planning/version-policy-task.md` 已有无关本地修改，保留原样。

## 需求与验收

- REQ-FUSION-ASSESS-01：给出各融合点的可行性、与现有流程的重叠或冲突、关键风险，以及 Token 成本估算的可信程度；将方案保持为候选，不能把评估当成实施批准。
- AT-FUSION-ASSESS-01：对照本仓库规则和上游一手文档，区分已核实描述、未实测效果和建议；明确下一步试点需要的证据。

## 当前结论

这是工程判断，不是实测成功率：方法论层面的按需借鉴约有 70%–80% 可行；按文稿把两个图谱、自动风险分数和文档门禁串成默认强制流程，直接落地程度约 30%–40%。可先采纳证据分级、未知边界和按需影响维度；不应直接把静态图、关键词分数或引用字符串检查当成正确性证明。

| 候选能力 | 评估状态 | 依据与限制 |
| --- | --- | --- |
| investigate-codebase 的证据标签 | 高可行，增量改进 | 现有流程已区分源码、推断、未验证和检查状态；复用当前任务记录，不另建并行账本。调查可保持产品代码只读，但现有规则仍要求持续写任务记录。 |
| ScopeCairn 的图谱与 GRAPH.md | 可选试点 | 静态依赖能辅助定位，不能证明动态调用、运行时行为或业务影响；摘要可能过时，150 行不是 Token 上限。上游版本已到 0.12.0，附件的 0.1.0 不是当前版本。 |
| AgentEdit 影响查询 | 可选试点 | 作者的 1.0 精确率/召回率来自小型自建变异语料，不能外推到真实项目；双图谱串联会增加一致性与维护成本。 |
| impact-analyst 与 codebase-analyzer | 方法可借鉴 | 前者混合了 Harness Forge skill 与 Development Harness agent 两个不同实现；后者和 investigate-codebase 的调查流程重叠，按问题选一种即可。复制外部实现前需固定版本和核对许可。 |
| code-to-prd | 遗留接管辅助 | 自动扫描与骨架只提供初始地图，不满足现有全局基线的语义覆盖和用户审阅门槛。 |
| Blast Radius 风险分数、Protected 文件强制阻断 | 暂缓 | 权重与 0.7 阈值未校准；关键词、TESTED_BY/TESTS 边及文件名回退会误报漏报。临时列表尚未与具体任务、图版本和 Git 基准绑定；现有控制文件已有独立人工批准门禁。 |
| Anchor/证据账本自动校验 | 有限可行 | 可机械检查引用文本是否存在于指定修订；无法证明引用支持结论，也无法证明影响链已完整记录。 |

Token 评估不能作为预算承诺。附件以规范化字符数除以四估算，中文和代码/工具输出未按实际模型分词；本地索引时间与模型 Token 混算，未测缓存、重复读取或输出裁剪。其“按需加载”合计实际上加总了全部七项。按附件自己的综合区间，中等任务相对 8k–12k 基线的比值为约 1.67–4.38 倍，大型任务为约 3.75–8.75 倍，不能据此断言统一的 2.5–6 倍。真实成本需同一模型在固定任务集上记录输入、输出、缓存及工具结果进入上下文的 Token。

一手来源抽样：ScopeCairn [README](https://github.com/DhaniAAA/ScopeCairn/blob/master/README.md) / [package.json](https://github.com/DhaniAAA/ScopeCairn/blob/master/package.json)，AgentEdit [README](https://github.com/thetaroot/agentedit/blob/main/README.md) / [EVALS](https://github.com/thetaroot/agentedit/blob/main/docs/EVALS.md)，[investigate-codebase](https://github.com/Data-System-School/agent-skills/blob/main/investigate-codebase/SKILL.md)，[code-to-prd](https://github.com/k57597907-netizen/code-to-prd/blob/main/skills/code-to-prd/SKILL.md)，[Blast Radius](https://github.com/athola/claude-night-market/blob/master/plugins/pensive/skills/blast-radius/SKILL.md)，[Harness Forge impact-analysis](https://github.com/ldilov/harness-forge/blob/main/skills/impact-analysis/SKILL.md)，[Development Harness impact-analyst](https://github.com/Jamie-BitFlight/claude_skills/blob/main/plugins/development-harness/agents/impact-analyst.md)，[codebase-analyzer](https://github.com/AthenDrakomin-hub/agent-skills/blob/main/skills/codebase-analyzer/SKILL.md)。上游可能继续更新；若实施须锁定 commit。Harness Forge 仓库为 GPL-3.0，直接复制内容前需另行核对许可兼容性。

## 影响与下一步

本次仅记录候选需求和评估，不变更源代码、对外版本、检查命令或受保护文件的实际检查逻辑。工程清单仅新增当前评估任务入口；这一清单本身属于受保护控制文件，后续若要提交需按既有独立人工审阅规则处理。没有将本次评估当作该批准。

建议先选一个真实 TypeScript/Python 仓库和 5–10 个已知变更任务，以人工审阅的依赖与影响范围作参照；只测试“现有记录中增加来源/未知标签 + 一个可选图谱工具”。记录漏报、误报、人工修正时间、索引耗时、上下文 Token 与任务总耗时，再决定是否扩展。实现前需另立完整方案并由用户批准，受影响部分重新做 skill review、许可与影响分析。

延后项：图谱工具选型（模块：影响调查；依赖：目标语言、仓库规模和真实任务样本；恢复条件：确定试点项目）；风险评分门禁（模块：checker；依赖：误报/漏报与阈值校准；恢复条件：试点数据足够）；PRD 自动同步（模块：接管文档；依赖：基线覆盖与人工审阅标准；恢复条件：明确遗留项目场景）。这些均未确认，也未授权实施。

## Skill review 与验证边界

2026-10-16 检查当前会话 Skills catalog，采用本仓库 `SKILL.md` 1.4.3 及适用的 requirements-interview、project-documentation、checker 引用作为评估规则；本次隔离 forward-test 采用 `skill-creator` 的独立验证原则，并采用 OpenAI Docs 的 `codex exec --json` 用量记录说明。附件中的七个外部项目只把 ScopeCairn 0.12.0 安装到临时目录并实际运行只读 `scan`、`context`、`impact`；其他工具仅做上游资料核查，没有安装或采纳。准确率、风险评分和 Token 试验结果已记录在下方章节；结果不满足采用线。

当前阶段：隔离试验完成；正式融合暂缓，实施未授权。验证：2026-10-16 运行 `python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --run-checks`，退出码 0，`required_checks_satisfied=true`，TEST、COMPILE、GUIDANCE-COMPILE 均 pass；可选的手工清单仍为 partial。该结果仅说明本仓库声明的检查通过，不证明外部方案的准确率、风险评分或 Token 成本。未运行 commit/committed 模式，未提供受保护控制文件的批准信号。

## 隔离 A/B/C 试验结果

用户于 2026-10-16 授权按预注册标准进行隔离试验。临时工作目录及原始事件保存在本机 `work/fusion-pilot/location.json` 指向的目录；没有安装到正式 skill，也没有修改提交门禁或推送。

试验使用同一模型配置、同一批 6 个仓库变更场景和独立 `codex exec --json` 会话。A 使用固定源码上下文和现有流程；B 增加证据等级与未知项协议；C2 在 B 的基础上运行 ScopeCairn 0.12.0 的 `context`/`impact` 只读查询，并把真实查询结果作为静态候选证据。Codex JSON 的 `turn.completed.usage` 记录了实际 input/cached/output/reasoning tokens。ScopeCairn 索引了 59 个文件、219 个符号、816 条关系；6 个查询总耗时约 4.9 秒。

评分基准为每个场景预先人工列出的必需受影响文件集合；S3 修正了最初错误引用的不存在 `scripts/tests/test_adapters.py`，改为仓库实际存在的 `scripts/tests/test_checker.py`。样本只有 6 个，结果用于工程决策信号，不代表统计显著性。完整矩阵和原始 usage 在临时试验目录的 `final-metrics.json`、`packed-results-A2.json`、`packed-results-B.json` 和 `packed-results-C2.json`。

| 变体 | 文件 precision | 文件 recall | 文件 F1 | 总 input+output Token | 相对 A |
| --- | ---: | ---: | ---: | ---: | ---: |
| A 现有流程 | 82.76% | 80.00% | 81.36% | 203,269 | 基准 |
| B 证据协议 | 95.65% | 73.33% | 83.02% | 257,728 | F1 +1.66pp；Token +26.79% |
| C2 证据协议 + 实际图谱查询 | 92.00% | 76.67% | 83.64% | 281,036 | F1 +2.28pp；Token +38.26% |

B 减少了误报，precision 提升 12.89pp，但漏掉了更多必需影响，recall 下降 6.67pp，综合 F1 只提升 1.66pp，同时 Token 增加 26.79%。C2 相对 A 的 F1 只提升 2.28pp，recall 仍下降 3.33pp，Token 增加 38.26%；相对 B 只多提升 0.62pp F1，却再增加 9.04% Token。图谱查询本身很快，但其输出进入上下文后放大了模型输入成本。

按预注册标准（质量至少提升 5pp 且 Token 增幅不超过 25% 才考虑采用），B 和 C2 均未达标。结论：放弃当前“证据协议 + 默认代码图”的正式融合；保留现有流程中已经存在的事实/推断/未知边界，暂不新增账本格式、图谱依赖、风险评分或提交硬门禁。若未来有更大样本和明确漏报痛点，可单独重开一个只读工具试点；需要重新固定版本、许可、任务集和验收标准。

## 2026-10-16 隔离试验批准与预注册

用户原话：“那么按照你的建议来更改然后测试,看看能提升多少个百分点…如果提升巨大…应用…提升很小,甚至token数量消耗巨大…放弃”，随后确认“可以的按照这样开始吧”。批准范围：隔离 A/B/C 试验、一个本地可选图谱、实际用量记录；无提交/推送授权。

- A：原版1.4.3；B：A+简短证据/推断/未知要求；C：B+ScopeCairn 0.12.0（npm注册表，局部安装，固定完整性）。
- 同一CLI默认模型配置、同一源码HEAD、独立上下文；不弱化A。6个真实源码变更问题，先固定参考影响位置与关键行为，再运行，不能用最终答案反向改评分。
- 指标：路径精确率/召回率、F1、关键行为覆盖、无依据结论、input/cached/output Token、墙钟时间；每项结果均保存原始事件。来源标签本身不计正确率加分。
- 采用候选线：找全率+10pp，精确率下降不超过2pp，Token增幅≤25%；不足5pp且Token增幅>25%则放弃。5–10pp或不稳定结果保留为不足证据。样本很小，不外推总体统计显著性。
- Skill review范围扩大：采用skill-creator（当前会话系统路径，版本未提供）的Independent Forward-Testing；采用OpenAI Docs（同目录系统路径，版本未提供），已读官方non-interactive文档，CLI JSON turn.completed记录实际usage。planning-with-files不采用，复用本Task；tdd不采用，本批是流程行为试验。
- 影响：治理记录与work下试验驱动；原始SKILL、脚本、既有保护/检查不改；无数据库业务或迁移影响。试验临时位置存work/fusion-pilot/location.json，不硬编码到通用skill。正式交付能力未变，无需升版；若采纳正式增强再评估版本。
