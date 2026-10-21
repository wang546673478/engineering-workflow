# 接入工具与原流程映射

## 可选批准合同升级（1.8.0）

新scaffold与显式legacy迁移增加approval_policy，但默认enforcement=diagnostic，不阻断旧证据不完整的流程；strict必须显式`--approval-enforcement strict`。两者都保留pending原批准，不生成真实用户审批，合同字段和证据格式见[checker](checker.md#结构化批准证据合同)。strict只加强审批声明，原阶段、测试、文档同步、例外及有效批准复用保持。

已有stage但尚无approval_policy的项目先预览：`adopt_project.py --root <project> --skill-source <实际来源> --skill-version <实际版本> --upgrade-approval-contract --approval-enforcement strict`。输出前后policy及相应检查结果，不改文件。用户授权具体升级后，加`--apply-approval-contract-upgrade`原子写入；失败保留旧字节。无需strict时选择diagnostic或省略该选项。现有有policy的项目不由重复接入改写，调整仍按项目控制面规则审阅。

legacy无stage继续使用原`--upgrade-legacy-manifest`显式迁移，保留已有checks、required inventory、依赖、历史批准及文档；不能把缺证据的旧approved自动重写成可信新批准。升级完成与门禁通过分开看bootstrap；外层exit=0不表示证据全部满足。

实际入口须用已核对的checker，并给严格项目hook/CI设置`ENGINEERING_APPROVAL_CONTRACT=1`，模板会传`--require-approval-contract 1`；旧checker拒绝未知参数，避免静默忽略新字段。此项是工具能力选择，不是控制面批准变量，不得代替原一次性外部审批。现有模板默认调用保持，只有配置该能力时加参数。

本工具落实SKILL.md既有流程，不新增业务阶段或用户审核轮次。主线、模块审核、持续需求记录、自主调查、有效批准复用和例外均以SKILL及原引用为准。安装副本与维护仓库各自有版本，必须读取实际调用来源；仓库发布不会自动更新全局安装或外部项目。

## 接入与恢复

`install_agents_guidance.py --root <project>`仍可先维护根部AGENTS和显式选择的原生薄入口。清单尚缺时输出`guidance_only_incomplete`，不把入口安装当作调查/接入完成。指定的manifest必须是JSON路径；已存在文件须可读且为schema_version 1对象，Markdown索引不可以冒充JSON。只维护入口不要求先补齐业务文档或审批。

需要一并建立工程清单骨架时运行：

```text
python <skill-dir>/scripts/adopt_project.py --root <project> --profile lite --skill-source <actual-skill-source>/SKILL.md --skill-version <actual-version>
```

已有实现默认existing；无实现显式greenfield。重复`--implementation-path backend --implementation-path frontend`选择实际非根实现范围。`--document SPEC=docs/SPEC.md`等映射已有工件，ID支持BASELINE/SPEC/PLAN/TASK/MAP/DB/CONTRACT/FLOW/IMPACT/TRACE；不创建或覆盖业务文档。`--state-dir`和`--task-id`选择实际状态位置/任务。初始化的发现范围是候选，agent负责核验遗漏和原验证政策。

命令返回`initialized_incomplete`骨架，审批保持pending；bundled checker自动做只读bootstrap，不执行项目命令。外层exit 0表示骨架和入口已建立，实际检查结果见`bootstrap.exit_code/report`，文档缺失/项目检查未执行会明确不通过。后续用已记录checker执行`--mode discovery --run-checks`核查实际声明；成功不代表语义覆盖、基线批准或用户理解。

旧清单默认不覆盖，审核后用`--upgrade-legacy-manifest`显式增补字段。保留文档、检查、任务、历史和既有批准，不自动重新要求人工审阅；agent将仍适用的证据映射到相应字段。缺证据保持pending，不由工具制造approved。迁移同目录临时文件原子替换，失败保留原JSON；写前核对原字节，仍不宣称任意并发编辑互斥。所有入口目标预检后写入，但跨文件写入并非事务，OS失败后保留清单以便核查重跑。

同源/版本/状态目录的重跑保留任务和批准，仅维护入口和诊断；来源不一致要求核对升级影响后显式更新记录，不必再次询问已授权的普通安装维护。`adoption`记录skill_source/skill_version/checker_source/manifest_path/state_dir/checked_at；bootstrap另记本次真正执行的checker_source。checker留在skill包，不复制到业务项目。

## 原规则与字段

`workflow.stage`是可选的当前阶段记录，不要求每个任务重走全部阶段。旧清单无stage继续原检查路径，并报告未启用声明阶段核验的限制。初始化从takeover_discovery开始；agent核对有效现状和证据后可恢复实际阶段。

| 原适用规则 | 对应记录与行为 |
| --- | --- |
| 首次接管无有效基线 | takeover_discovery；既有系统planned/partial只能在discovery诊断，不得越过基线审阅开始详细功能访谈或实施 |
| 空实现项目不审阅不存在的系统 | baseline.origin=greenfield，空实现起点证据已记录；workflow.baseline_review可为not_applicable，必须有reason/evidence；无实现时not_applicable，首批代码partial，交付complete/approved |
| 有效全局基线/历史批准可复用 | baseline_review=approved保留原source_revision/evidence，不要求每个事实修订重新批准；批准实际失效时标invalidated=true或pending，仅重审受影响内容 |
| 小修按既定需求做最小步骤 | tasks[].workflow_kind=small_fix；proposal_approval可为not_applicable，但必须记录已知需求/影响的reason/evidence及scope revision；不能将重大功能标小修绕过方案批准 |
| 完整方案与实施状态区分，但不重复询问 | proposal_approval和implementation_authorization记录不同含义，可引用同一条明确要求按该方案实施的用户指令；授权task_id/plan_revision绑定相应任务和版本 |
| 完成需要事实基线complete/approved | complete阶段和handoff接受complete或approved；不额外强制最新事实修订再次人工批准，不强制新增handoff阶段；原任务完成、依赖、影响和实际验证门槛仍执行 |

阶段可记录takeover_discovery/baseline_review/requirements_interview/plan_confirmation/implementation/verification/complete；implementation与verification是原“实现与验证”的执行状态，不是新用户审核。change/handoff/commit/committed检查已声明implementation_paths；早期未经授权的实现变更被拒绝，两个提交模式失败不执行声明命令。小修/空项目的不适用必须有实际证据，不是普通pending的替代。

checker只核验声明、路径、状态和证据文件，不认证人类批准、理解程度或全部语义/动态依赖；不能阻止编辑器写文件或发现漏声明源码。仍需agent按原规则自主调查、维护Baseline→Spec→Plan→Task，必要时纠正事实和重审失效前提。安装/发布/外部项目迁移只按用户实际授权执行。
