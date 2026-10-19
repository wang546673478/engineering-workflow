# TASK-ADOPTION-LIFECYCLE-01：完整接入与阶段门禁

日期：2026-10-19（Asia/Shanghai）
任务 ID：`TASK-ADOPTION-LIFECYCLE-01`；输入基线：`BASELINE-SAFE-19-21-01` / source `3c1cb36`；当前阶段：原流程场景验收与修正；通过后提交上传并更新本地安装。

## 当前状态与范围

- 本轮进度：原流程场景修正已实现，主SKILL原有核心章节与1.6.4逐段完全一致；205项全量测试及原编译门槛通过（TEST109.390秒，原120秒不变）。下一步为暂存/精确提交门禁、安装副本合并演练、上传及实际更新。前轮“未获上传/安装授权”和“保持性未满足”记录保留为历史，已由本轮明确授权和修正取代。
- 最新授权：用户“这样你做一下测试,我看你说的是你打的是补丁,我担心补丁不好用,你先做测试,测试没问题上传github,然后更新本地的skill”。本轮以保持原流程/例外为验收，允许必要修正、测试、提交上传及更新现有安装；不再等待重复发布许可。已明确的托管环境独立人类审批仍不代办。旧保持性不满足记录保留为历史，不当作已解决。
- 当前结论（2026-10-19T23:04:21+08:00）：用户明确“还不能动skill的流程”，要求先回答是否全局修复且流程不变。本次复核确认：跨接入/清单/checker/文档联动已做，原主线阶段顺序未改；但新增强制JSON接入条件、阶段/审批字段及complete/handoff机械条件实际收紧了流程，且未完整核对小修/已有有效基线/恢复复用批准/空实现项目例外。因此不能继续宣称满足“流程不变”的修复完成；原200项程序测试通过不等于流程等价性通过。当前仅核查及记录，暂停按本补丁交付，不改实现、不回滚、不发布。
- 当前工作树 `11f0`，由原 `9276` 未提交补丁恢复，原工作树完整保留。用户本轮“先把上个问题修复了来”授权继续本仓库修复；需求与方案范围沿用本文，未授权外部项目迁移、全局安装更新或发布。当前实现、文档和1.7.0 Unreleased已同步；29项相关回归、技能结构校验、端到端接入核验和原三项必需检查均通过。22:19的核查结论保留在历史段。
- 本任务修复 `engineering-workflow` 自身的接入和阶段控制，不修改任何外部采用项目，包括 `llm-agent`。
- 复现事实：1.6.4 的 `install_agents_guidance.py` 只写项目 `AGENTS.md`；它不会创建 `engineering-manifest.json`，也不会建立可检查的活动阶段和审批状态。独立运行 `init_manifest.py` 才会生成 planned 清单，后续还必须由 agent 映射现有文档并运行 checker。
- 用户原话（2026-10-19，Asia/Shanghai）：“现在是修复engineering workflow的问题,不是修复llm-agent的问题,明白了吗?”；随后授权：“继续处理吧,先看看1.6.4有没有这个问题,有就修复”。本任务范围以此为准。
- 旧 manifest 保持兼容；新完整接入使用统一入口生成清单、记录 skill 来源/版本和生命周期状态。checker 仍位于 skill 仓库，由项目通过路径或固定 CI/hook 调用，不复制成项目源码。

## 需求与验收

| 需求 | 验收 | 内容 |
| --- | --- | --- |
| REQ-ADOPTION-01 | AT-ADOPTION-01 | 完整接入入口同时建立持久化 `AGENTS.md` 入口和 reviewable manifest；已有 manifest 不覆盖，旧项目可显式保留并报告兼容路径。 |
| REQ-ADOPTION-02 | AT-ADOPTION-02 | 新 manifest 记录 active Baseline/Spec/Plan/Task、当前阶段、实现范围、三类独立审批状态和 skill 来源/版本；planned/pending 不伪装成完成或批准。 |
| REQ-ADOPTION-03 | AT-ADOPTION-03 | checker 对声明生命周期执行结构检查；基线未审阅、方案未批准或实施未授权时，阶段状态不允许被写成后续阶段，且变更/提交门禁拒绝实现范围内的代码变更。 |
| REQ-ADOPTION-04 | AT-ADOPTION-04 | 阶段门禁与 adoption 工具保持旧 manifest 兼容；checker 仍只验证声明式证据，不能宣称自动证明业务语义或用户理解。 |
| REQ-ADOPTION-05 | AT-ADOPTION-05 | 文档、模板、README、合同、模块图、业务流、版本和测试同步；1.6.4 → 1.7.0 作为兼容新增能力，保留 1.6.4 历史记录。 |

## 方案与执行项

1. 增加 `scripts/adopt_project.py`，把 guidance、manifest skeleton 和实际 skill provenance 作为一个可重复的完整接入入口；默认拒绝覆盖现有 manifest。
2. 扩展 initializer 的 document override 和 skill provenance 参数，使已有项目能映射现有权威文档，不强行生成或覆盖业务文档。
3. 在 manifest workflow 中增加 `stage`、`implementation_paths`、`baseline_review`、`proposal_approval`，在任务中增加 `implementation_authorization`，在顶层 `adoption` 保存来源与版本；checker 对新字段执行生命周期一致性与实现路径门禁，旧清单未声明时走兼容路径。
4. 更新 `SKILL.md`、接入模板、README、checker 合同和项目条款，明确“安装入口”和“完成采用”是两件事；说明 checker 的真实来源和调用方式。
5. 增加 observable CLI/fixture 回归：完整接入、已有 manifest 保护、skill 版本记录、阶段不一致、未批准阶段的代码变更拒绝和旧 manifest 兼容。

## Skill review

- catalog source：当前会话 Skills catalog；checked at `2026-10-19 16:44 +08:00`；范围包括 skill 资源结构、Python CLI、manifest/checker 生命周期、文档和回归验证。
- adopted `engineering-workflow`：来源本仓库 `SKILL.md`，版本 `1.6.4` / source `3c1cb36`；本任务直接修复其接入、清单和阶段门禁。
- adopted `skill-creator`：来源 `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`，版本未提供；用于保持现有 skill 结构、渐进披露、脚本验证和兼容边界。
- adopted `tdd`：来源 `C:/Users/54667/.agents/skills/tdd/SKILL.md`，版本未提供；本任务需要 observable CLI/fixture 回归，采用行为回归而不改变产品测试策略。
- not-adopted `planning-with-files`：来源 `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，版本未提供；本仓库已有 manifest、Spec、Plan、Task 和 traceability 权威体系，不新增平行台账。
- recheck：若生命周期字段、接入命令、受保护路径或输出范围改变，重新检查 skill applicability 和 documentation impact。

## 影响与限制

- instructions：`SKILL.md`、README、接入模板、项目条款、initializer、guidance installer 和新 adoption CLI。
- checker：生命周期字段、stage gate、实现范围变更门禁；不改变旧 manifest 的既有验证语义。
- tests：initializer/guidance/checker 的临时项目回归；不改变业务项目测试命令。
- governance：manifest、Spec、Plan、Baseline、合同、业务流、模块图、traceability、版本和 CHANGELOG。
- database/API/product runtime：不适用；本仓库没有业务数据库或产品 API，adapter 仍是 metadata-only。
- 限制：checker 不能发现聊天中完全未写入的需求、判断用户是否理解、发现所有动态依赖或证明 skill 已被宿主加载；这些边界保留为人工审阅责任。

## 验证与发布

- 必需检查：`TEST`、`COMPILE`、`GUIDANCE-COMPILE`；另运行 skill-creator quick validation、`git diff --check` 和隔离接入/阶段 fixture。
- 版本：1.6.4 → 1.7.0，MINOR；原因是增加兼容的完整接入入口、provenance 和生命周期门禁，不改变旧 manifest 的默认兼容路径。
- 当前实施状态：已有实现，保持原流程的语义验收未满足；原200项程序验证通过证据保留。整体任务in_progress，版本1.7.0 Unreleased，未提交、未推送。commit/committed及托管结果不声明为通过。

## 当前下一步

先向用户说明本补丁做过跨模块联动，但接入/批准/完成条件已被收紧，不能称为流程不变。记录“保持原流程与全部适用例外”为当前约束；依赖原“兼容新增门禁”前提的交付结论待复核。后续修正须先逐条映射原规则和例外，区分落实已有规则与新加流程；本轮用户只要求回答，不继续改实现或发布。

## 恢复核查（2026-10-19 22:19 +08:00）

- 用户原话：“你看看刚才说的问题,有没有解决”。本轮范围为状态核验与证据记录；未修改工具代码、提交、推送或更新全局安装，也未操作 `llm-agent`。
- 恢复来源：当前会话 Skills catalog、用户显式提供的全局 skill 1.6.1，以及本仓库规则所指定的 `SKILL.md` 1.6.4、manifest、Task/Impact、Baseline/Plan 和 checker/implementation 引用。核查由 `11f0` 工作树发起；修复实际位于同仓库 `9276` 工作树。两者 HEAD 都是 `3c1cb36e22747fe134d4b9b0f64d5ca282227da9`；未复制、合并或覆盖已有变更。
- `skill_review`：checked_at `2026-10-19T22:19:20+08:00`；采用 engineering-workflow（本仓库 `SKILL.md` 1.6.4 / `3c1cb36`；恢复权威状态、区分实施和验证/发布）。本轮只检查已有 Python CLI 和文档证据，不修改 skill 资源，不新增测试，未重新采用 skill-creator 或 tdd；planning-with-files 不采用，继续使用本 Task，避免重复台账。未扩大至产品项目或全局安装修复。
- 已观察实现：新增 `scripts/adopt_project.py`；guidance installer 校验真实 JSON manifest；initializer 建立 `takeover_discovery`、来源/版本和独立审批占位；checker 已包含 `discovery`、`workflow-lifecycle` 与 `implementation-gate`。这些是未提交工作树事实，非发布承诺。
- 新运行命令：`python -m unittest scripts.tests.test_adoption scripts.tests.test_guidance scripts.tests.test_init scripts.tests.test_checker.CheckerTests.test_discovery_mode_allows_an_existing_incomplete_baseline_without_claiming_completion scripts.tests.test_checker.CheckerTests.test_implementation_scope_changes_are_blocked_before_separate_approvals scripts.tests.test_checker.CheckerTests.test_implementation_scope_changes_pass_only_after_all_lifecycle_approvals -v`。结果：22 tests / 14.069s，exit 0。只覆盖上述相关回归，不代表全量 TEST 或 commit/committed 门槛通过。
- 新运行诊断：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base HEAD --task TASK-ADOPTION-LIFECYCLE-01`。checker exit 1、`required_checks_satisfied=false`；`change-scope` 报告 `docs/module-map.md`、`docs/contracts.md`、`docs/business-flow.md` 缺少同批更新。本次未传 `--run-checks`，TEST/COMPILE/GUIDANCE-COMPILE 均明确 skipped，不记为测试失败或通过。
- 交付缺口：主 `SKILL.md` 尚未指向新增完整接入入口；VERSION、SKILL、CHANGELOG 等仍为 1.6.4，尚无 1.7.0 发布记录；新增源码仍未提交。`git ls-remote origin refs/heads/main` 实查远程 main 为 `3c1cb36e22747fe134d4b9b0f64d5ca282227da9`。
- 全局安装实查：`C:/Users/54667/.codex/skills/engineering-workflow/VERSION` 和 SKILL metadata 均为 1.6.1，HEAD=`a407b112410e8717511d62fda8eead66d18cf043`，另有原有未提交/未跟踪文件，均保留。因此用户继续调用该安装路径仍会加载旧副本；这不是用户触发方式错误。
- 本轮只刷新状态与验证证据，未改变交付内容，无需单独升版。结论：核心修复部分实现并通过相关回归，整体未完成、未发布、未更新到全局安装；保持原验收和必需门槛。

## 本轮实施续接（2026-10-19T22:33:23+08:00）

- 采用 engineering-workflow：本仓库 SKILL.md 起点1.6.4 / 3c1cb36，重读项目规则、当前Baseline/Spec/Plan/Task、implementation/checker和相关视图；采用 skill-creator：C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md，版本未提供，正文及openai_yaml引用已读。catalog为当前会话Skills清单。保留已有行为回归，不另外采用TDD流程；不使用planning-with-files，避免平行台账。单agent执行。
- 补充完整bootstrap真实报告且不运行项目命令；已有清单迁移采用原子替换及写入前原字节复核，失败保持原JSON；统一入口目标预检防止覆盖manifest；实现范围的绝对路径统一规范化。修复initializer重复授权字段并支持existing项目的显式实现范围。
- 同步SKILL、README、AGENTS/模板、checker/adoption引用、模块图/契约/业务流、Baseline/Trace及1.7.0的VERSION/SKILL/README/openai.yaml/CHANGELOG。原TEST/COMPILE命令和120/30秒时限保持；GUIDANCE-COMPILE只追加新adopt_project.py编译，没有减少旧检查。instructions因只读bootstrap新增对checker的真实允许依赖；没有反向依赖和数据库变更。
- 阶段检查只针对显式声明/迁移的清单；保留旧清单兼容。当前维护清单继续沿用原审批体系，未将历史baseline审阅自动伪造为新阶段批准。新增字段的实际拦截由隔离CLI/真实Git fixture核验。
- 相关验证29 tests / 22.526s通过，覆盖bootstrap未完成、幂等、文档映射、已有清单保留、迁移替换失败、错误目标不落盘、阶段/计划版本/任务绑定、绝对路径拦截、handoff阶段及两个提交模式不执行命令。完整原门槛结果后补。
- 验证环境：任务局部work/adoption-validation/env及scripts/context-runtime；安装锁定tree-sitter和TypeScript解析依赖，仅供原全量回归，不改全局Python或外部项目。

## 原门槛首次诊断（未通过，历史保留）

- `work/adoption-validation/change-01.json`：change-scope和资料检查通过，两项编译通过；TEST在120.020秒超时，整体失败，不当作通过。
- 诊断运行 `python -m unittest discover -s scripts/tests -v`（Python3.14.7任务venv）：200 tests / 139.410s，4个断言失败，均来自原有1.6.4 JSON深度/错误边界fixture；Python3.14可解析fixture的10000层JSON，故原先“必达解释器深度保护”的输入已不是该运行时的解析错误。保留原测试和工具政策，不扩入本任务修复；当前仓库CI固定Python3.11，正在准备局部同版本验证。
- skill-creator quick_validate在默认GBK下读取UTF-8中文失败；使用原脚本配合 `python -X utf8` 后通过，脚本未修改。版本五处及Unreleased条目一致、字典重复键检查和git diff --check通过。

## 局部环境和端到端补充

- 为匹配现有CI，使用uv在`work/adoption-validation/python311`准备Python3.11.15，并将锁定tree-sitter0.25.2/tree-sitter-rust0.24.2及PyYAML6.0.3安装到任务局部`py311-packages`。后续验证只为子进程临时设置PATH/PYTHONPATH，不改系统Python或永久环境。uv意外生成了全局python3.11.exe shim；已用创建时间及二进制内指向本任务路径核实其归属并删除，局部runtime保留。
- `work/adoption-validation/endtoend-01.json`记录真实完整链路：adoption初始化返回initialized_incomplete且bootstrap未通过；补齐合成文档/权威fixture检查后discovery通过；completion_ready仍false、implementation_authorization仍pending。该临时项目已自动清理，未触及外部项目。

## 全量性能诊断与夹具等价优化

- Python3.11.15诊断：200 tests / 122.569s，全部通过，无skip；原门槛`change-02.json`仍在120.016秒超时，不能用诊断通过覆盖正式失败。逐测试耗时见work/adoption-validation/test-timings-311.json。
- 为容纳新增回归并保持原120秒，checker测试夹具将相同初始真实Git仓库的完整`.git`复制到各个临时根；每份为独立普通文件，不使用hardlink、共享worktree/alternates或mock Git。后续commit/config/object删除及HEAD/index漂移验证仍操作真实隔离Git仓库。原断言、用例、命令与时限不删减；只消除每次重复init/add/相同baseline commit的启动开销。

## 最终本地验证（2026-10-19 22:52 +08:00）

- `python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base HEAD --task TASK-ADOPTION-LIFECYCLE-01 --run-checks --report work/adoption-validation/change-03.json`：exit 0，tool_version `1.7.0`，`required_checks_satisfied=true`；TEST 200项/103.828秒，COMPILE 0.235秒，GUIDANCE-COMPILE 0.234秒，所有必需文档/影响检查通过。报告中的数据库清单仍是声明的metadata-only不适用项，未引入业务数据库。
- `python -X utf8 C:/Users/54667/.codex/skills/.system/skill-creator/scripts/quick_validate.py .`：`Skill is valid!`。`git diff --check`通过；版本、SKILL、README、openai.yaml、CHANGELOG一致为1.7.0/Unreleased；200项测试发现数、字典字面量重复键和端到端 adoption/discovery 状态核对通过。
- 这只证明当前未提交工作树在本地规定命令下通过；`verified_tree`/`verification_head`为空，因为没有运行 commit/committed 模式。未提交、未推送、未发布，未更新全局1.6.1安装，未迁移 `llm-agent`。受保护控制文件仍需用户/托管审阅后才能提交；原批准范围不能自动覆盖本次控制面变更。

## 最终记录与交付边界

- 机器证据：[adoption-lifecycle-verification.json](adoption-lifecycle-verification.json)，保留原通过report、源码SHA256、失败历史与运行环境。当前局部依赖保留在ignored work目录便于重跑；无任务子进程残留。
- 只读commit预检未通过：没有暂存内容，工作树与index不同；三项声明命令均未运行。该报告不代表完成提交门禁，也没有给控制面批准变量注入值。源码本地修复完成与发布完成分别记录。
- 最终仅更新证据、Task/manifest状态与引用，没有改变已验证源码或声明检查。按规则复核当前文档链接、变更覆盖和源码新鲜度，不再次重复未受影响的全量测试；不会把后补记录当作新源码通过证据。

## 原流程保持性核查（2026-10-19 23:04 +08:00）

- 用户原话：“其实这个问题应该通过全局来看要怎么改,还不能动skill的流程,你回答我,你的改动是否是通过全局来改的?然后没有动skill的流程?”。这是新的明确约束与解释请求，不是继续扩展门禁或回滚指令。已重读本仓库SKILL/AGENTS、当前Task/Plan/Impact及实际diff，并对照用户调用的全局1.6.1正文和原1.6.4。
- 原核心顺序、模块集中审核、持续需求记录、自主调查及Baseline→Spec→Plan→Task主线仍保留；不能据此推断所有规则未变。原SKILL接入段已修改，guidance安装从入口维护变为要求真实JSON及活动任务，新增stage/authorization约束；complete阶段强制当前Baseline为approved并匹配当前审阅，而原交付允许complete/approved。
- 具体不等价证据：checker.workflow_lifecycle_gaps对requirements_interview及其后阶段无条件要求baseline_review批准；原requirements-interview明确空实现项目无需审阅不存在的系统。新增流程对已有有效基线、小修、恢复复用批准的程序路径也尚未完整对应，不能以legacy兼容替代这些情形的核查。独立授权字段本身可记录同一条适用用户指令，不证明必须额外询问；此次不能夸大成必然新增一次用户确认。
- 全局覆盖已涉及入口→清单初始化→阶段检查→变更/提交→文档/版本/回归；但实际安装/宿主加载不在本次实现范围，且全局流程语义等价审查不足。结论为“有跨模块联动，未满足流程保持性”，不宣称零影响或全场景已闭环。
- 需求与审批：保留原SPEC-ADOPTION-LIFECYCLE-01/PLAN-ADOPTION-LIFECYCLE-01及历史授权；当前“保持原流程”约束要求重审受影响的新增强制规则，不把旧实施授权自动转为对新约束的验收。原源码和测试证据保留，暂停依赖不等价规则的交付。本轮没有修改代码或重跑无关全量测试。
- skill_review续接：当前catalog；采用engineering-workflow（本仓库1.7.0未发布工作树，以1.6.4原文及全局1.6.1对照）；本轮仅流程差异审查，未采用额外实现/设计或多agent技能。来源及版本与先前记录保持可追踪。

## 当前修正与验证计划（原流程保持性）

1. 接入入口继续支持先写AGENTS，清单尚缺时明确incomplete；Markdown不能冒充JSON，不把入口安装等同调查完成。恢复原SKILL核心流程和例外，只增加工具使用说明。
2. 阶段字段为对原流程的可选可检查映射，不增加必须依次进入的用户审核轮次。空实现可记录带证据的baseline_review不适用；小修以既定需求/影响证据记录完整方案访谈不适用。
3. 有效历史基线审核可复用，不要求每个事实基线revision都重新批准；失效批准保持pending/显式invalidated。允许交付complete/approved事实基线，不强制新的approved或handoff独立阶段。方案与实施授权可引用同一条明确覆盖二者的用户指令，保留不同状态不增加确认次数。
4. 使用实际临时项目和真实Git，测试允许场景与缺证据必须拒绝的场景；原必需全量测试/时限、compile、skill validation及commit/committed不弱化。通过后上传精确提交并核对远程；备份本地安装中所有已有修改/未跟踪文件，在临时副本演练升级后再更新并核对运行版本。
5. skill review：当前宿主catalog；engineering-workflow本仓库1.7.0未发布基于1.6.4、skill-creator系统技能（未提供版本）已重读；不另开平行planning或TDD流程，不委派。范围新增Git发布、本地Git安装合并验证，复用原仓库标准Git/CI规则；不修改外部采用项目。

## 本轮场景和控制面审阅记录

- 用户授权条件和具体范围：在已解释会涉及接入入口、真实清单、审批字段及完成条件的上下文中，用户明确要求“你先做测试,测试没问题上传github,然后更新本地的skill”；并保持其上轮“还不能动skill的流程”的约束。因此本批修正仅将工具门禁映射回原流程及适用例外，不引入新审核轮次。此授权涵盖本批checker/manifest/SKILL/模板/版本的必要修改与提交上传，不由agent依据测试结果自造额外批准。单次本地控制面信号仅用于该批授权范围；GitHub受保护environment required reviewer仍须人类独立操作，不能用本地授权代办。
- 本轮原门槛报告`work/adoption-validation/parity-change-01.json`：tool_version1.7.0、required_checks_satisfied=true，TEST205项109.390秒、COMPILE0.344秒、GUIDANCE-COMPILE0.235秒。场景含先写入口、无效Markdown、已有清单和文档保持、空项目访谈/实施、已知小修同条指令授权、事实基线刷新复用审阅/失效阻断、complete事实基线交付、无需多走handoff阶段及两种提交未授权不执行命令。
- 主流程不变证据：`work/adoption-validation/core-flow-parity.json`。SKILL从“持续需求记录与模块审核”到“按阶段读取”前，以及“完成门槛”全文均与输入3c1cb36逐段一致；原流程表/例外、访谈/模块审核、自主调查、联动和版本政策未改。接入段保留原文，只增加工具说明和引用。
- 本地安装备份：`work/adoption-validation/local-install-backup`记录原HEAD a407b11、状态、13个修改/未跟踪文件的逐文件SHA256和完整tracked binary patch；尚未改动安装。升级需先在副本演练合并及版本/CLI验证，实际更新后再次核对。

暂存预检首次正确拒绝遗漏的AGENTS文档影响映射，已补入与模板相同的adoption-guidance门槛；未执行的声明检查保持skipped，失败原报告parity-commit-01保留。
