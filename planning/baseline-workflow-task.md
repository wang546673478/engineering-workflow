# TASK-BASELINE-01：自主调查与动态基线维护

## 当前状态

- 日期：2026-10-17（Asia/Shanghai）；阶段：1.4.4规则与模板已验证，用户已授权提交并上传GitHub；实际提交门禁与推送进行中。
- 需求状态：confirmed；规则实施状态：complete；发布状态：authorized / not yet pushed。当前版本仍为1.4.4 / Unreleased，实际推送后补真实发布日期与回执。
- 来源：本仓库SKILL.md 1.4.3；Git基点 `82f87c4d5d48d30ed3610303a5f7864023044038`。当前任务由engineering-manifest.json的workflow.active_task指向本Task。
- 用户先前授权：“[$engineering-workflow] 开始更改skill吧”，范围为已讨论的自主基线调查、隔离环境准备、技术核验职责、可审阅范围与动态纠错规则。
- 最新用户原话：“那就不采用,然后把1.4.4上传github”（2026-10-17，Asia/Shanghai）。实验融合候选已否决；本次仅提交并推送已审阅的原1.4.4及必要发布回执。无新增标签、托管Release、部署或CI保护变更。
- 下一步：在干净发布工作区核对实际暂存内容，运行原commit及committed门禁，正常推送并核对远程SHA；实际发布后补日期和回执。

## Spec、影响与验收

| 需求 / 验收 | 已批准的规则与验证目标 |
| --- | --- |
| REQ-BASELINE-01 / AT-BASELINE-01 | 已授权调查持续执行，分批保存和进度汇报后继续；达到有证据的可审阅结果或真实阻塞才停下，独立工作继续。隔离场景检查实际调查产物与结束原因。 |
| REQ-BASELINE-02 / AT-BASELINE-02 | 自主准备必要的局部运行时、依赖、数据库与缓存，实际运行迁移/相关测试并记录环境及清理；沿用授权与项目规则，不扩大为全局设置/生产部署。隔离场景检查测试库准备与验证证据。 |
| REQ-BASELINE-03 / AT-BASELINE-03 | agent承担源码与测试可回答的语义核验；用户审阅版本、范围、主要发现和限制。当前系统有界覆盖与外部未知分别记录；未知的关键影响保持阻塞，基线调查不自动变成全产品修复或生产认证。 |
| REQ-BASELINE-04 / AT-BASELINE-04 | 测试、运行和调查发现文档错误也触发校正，源码未改同样适用；查证后自主修正所有受影响文档，保留旧审阅/证据。若推翻已批准方案依据，标记并暂停依赖错误的部分，只重审受影响决定。隔离后续场景检查实际纠错、影响和批准状态。 |
| REQ-BASELINE-05 / AT-BASELINE-05 | 初始化时核对适配能力与必需门槛；手工来源如实partial，模板默认不将它设为必过项。已启用项目既有required清单/测试不能自行降级；冲突应尽早定位并准备具体方案。核对模板与full初始化一致，运行现有manual保持partial的回归。 |

权威需求/验收同时在docs/spec.md登记。核心影响链：项目AGENTS入口 → 已授权调查循环 → 隔离环境/源码语义核验 → 版本和范围绑定的基线审阅 → 已批准实施 → 后续发现纠错 → 关联影响与局部重审。

## Plan 与范围选择

1. 正文保留必要行为与停止条件，细则集中在project-documentation及implementation-workflow；同步requirements-interview和接入条款。
2. 更新AGENTS管理模板、本仓库入口与Spec/Plan/Task模板，增加环境、调查覆盖、真实阻塞、清单能力和持续纠错证据字段。
3. 将project-manifest.example的手工清单required默认改为false，与现有init_manifest full行为一致；数据库/契约文档required不变，正文仍要求语义覆盖。只改变新接入示例，不编辑其他项目的清单。
4. 同步README和本仓库Spec/模块地图/契约/业务流。更新VERSION、SKILL metadata、README、agents/openai.yaml与CHANGELOG，候选1.4.4 / Unreleased。
5. 运行TEST、COMPILE、GUIDANCE-COMPILE原命令；change模式核对Git基点及本Task文档影响，quick_validate、版本/链接/差异检查。独立场景在临时目录执行，根agent核对产物。

此方案避免新增没有可信重提取协议的通用源码适配器，不改checker、适配器、CI、hook、检查命令或保护配置。manual/partial仍不满足已声明必需门槛；用户的基线范围接受也不能冒充机械检查通过。现有项目若要调整必需门槛或实现适配器，需要准备对应具体差异并按该项目规则取得批准，本任务不代为授权。

新示例放宽的是“尚未核对来源能力就默认要求两份清单机械通过”，并未放宽源码调查、文档覆盖、用户审阅、项目测试或既有项目门禁。本轮同时收紧持续调查、环境准备与后续纠错责任。此前只授权本地修改；现用户明确要求将已审阅1.4.4上传GitHub，具体提交/控制面审阅范围见下文，不延伸至其他规则或保护修改。

模块为instructions与governance；没有可执行API、manifest schema或数据库适配器变化，无业务数据、schema/迁移或新运行依赖。恢复方式为回退本批规则/模板及候选元数据，保留用户决定历史；不将回退文件视为撤销用户授权。

## Skill review

- 来源：当前会话Skills catalog；检查时间2026-10-17 03:28（Asia/Shanghai）；范围从诊断扩大到skill指令/模板/元数据修改，已重新读取正文、项目规则、当前Task、权威总览、相关引用与工作树。
- engineering-workflow：adopted；来源本仓库SKILL.md；1.4.3基准，1.4.4候选。已读requirements-interview、project-documentation、implementation-workflow、checker、project-agents-clauses及接入/Task/manifest模板。
- skill-creator：adopted；来源C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md；版本未提供；已读正文与references/openai_yaml.md，用于精简指令、保留权限和自动发现、结构校验与独立场景验证。
- planning-with-files：not-adopted；来源C:/Users/54667/.agents/skills/planning-with-files/SKILL.md；版本未提供；复用现有清单与Task。
- tdd：not-adopted；来源C:/Users/54667/.agents/skills/tdd/SKILL.md；版本未提供；本轮不修改可执行逻辑，不新增匹配文案的测试；采用现有回归和实际隔离行为验证。
- 2026-10-17发布范围复核：重新读取本仓库SKILL、AGENTS、当前Task、实现与checker引用和skill-creator；本次交付范围为已验证1.4.4及发布回执。无新技术/依赖；其他项目、checker、CI或新规则仍需独立审阅。

## Release impact

- 版本来源VERSION；1.4.3 → 1.4.4，PATCH。依据：修正指令和初始化示例不一致，兼容既有CLI/schema/适配器；新示例行为变化已在上文说明。
- 同步VERSION、SKILL metadata、README、agents/openai.yaml和CHANGELOG Unreleased；发布状态为已授权提交/推送、尚未实际发布；标签、托管Release和部署不在本次范围。

## 进度与验证

- 已完成恢复、实施授权记录、skill review、具体方案和影响分析；起始工作树与本地记录已备份；私有研究记录保留本地。
- 已完成正文、适用引用、接入与Task/manifest模板、README及权威文档同步；本仓库AGENTS管理区由安装器更新，重复调用幂等。VERSION、SKILL metadata、README、agents/openai.yaml与CHANGELOG为1.4.4 / Unreleased。
- 原命令change检查通过：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base 82f87c4d5d48d30ed3610303a5f7864023044038 --task TASK-BASELINE-01 --run-checks --report work/baseline-workflow-change.json`，退出码0；task-gate、change-scope、TEST、COMPILE、GUIDANCE-COMPILE全部pass，required_checks_satisfied=true，errors为空。报告覆盖24条工作树变更（含原有记录），可选手工清单仍partial，不冒充完整语义验证。
- skill-creator原quick_validate通过（UTF-8模式，复用忽略目录work/validation-deps的PyYAML6.0.3，未安装新依赖或改全局环境）。首次本地辅助校验遇默认GBK解码失败，改用Python进程UTF-8模式后原校验通过；没有改变项目必需命令。
- 静态整合通过：65个本地Markdown目标存在；元数据/版本/Unreleased一致；新示例与现有full初始化均源清单optional且DB/CONTRACT文档required；原checks、control_plane、modules、inventories、baseline、exclude_paths及全部旧tasks与起始状态一致；scripts/CI未改；原有version-policy/fusion记录SHA不变；AGENTS管理段外内容与HEAD一致。报告work/baseline-workflow-static.json。
- 两个独立隔离场景已完成并保存实际产物（临时目录路径见work/baseline-forward-location.json）：接管场景自主核对入口、字段、SQLite和10个探针，原定测试因Windows SQLite临时目录清理WinError32失败，未改产品/测试；更正场景测试2/2通过但发现源码ROUND_CEILING与最近分取整基线/需求冲突，已修正当前视图、保留历史并标记受影响报表方案需复核。两个场景均未进入产品实现。该结果仅证明受控模拟行为，不证明生产会话可靠性或真实项目宿主遵循。没有运行commit/committed、暂存/提交/推送或传入控制面批准；最终规则的人类审阅门槛保留。
- 验收结论：REQ/AT-BASELINE-01—05通过规则整合、静态能力比较、既有命令和两个隔离行为场景核对。场景结果证明受控输入下的持续调查、局部环境准备、失败保留和文档纠错行为；不证明所有宿主都会遵循、外部生产集成或未来模型可靠性。
- 补进度后的资料复核报告work/baseline-workflow-record-check.json：manifest、task-gate和change-scope均pass、errors为空；整体退出码1，因为未传run-checks，三项必需执行检查如实skipped。该报告仅作为资料/范围复核，不能称作完整门禁通过；实际测试通过依据仍是前述已运行的change报告，其验证对象未因进度记录变化而改变。

## 1.4.4具体发布审阅与计划

- 用户本次“把1.4.4上传github”明确批准已展示的1.4.4规则/模板差异及必要元数据、清单和文档进入提交并正常推送至当前GitHub仓库main。实验融合候选被明确否决，未安装到正式skill，也不进入本批提交。
- 控制面范围：SKILL.md、references/checker.md、VERSION、CHANGELOG.md及engineering-manifest.json；实际包含原自主调查/校正规则、新任务追溯和版本记录。示例中两份源清单默认optional与现有full初始化一致，DB/CONTRACT文档仍required；现有项目门禁不得自行降级。该放宽及职责收紧已随1.4.4方案和验证说明交付用户。
- checker、适配器、测试、CI、hook、原checks/control_plane/modules/inventories及旧tasks不变；不新增批准变量、保护豁免或自动采用规则。本地批准信号仅用于本次具体内容的单次检查进程，不写仓库或永久环境。
- 从已发布1.4.3建立干净发布树，只纳入1.4.4文件与本Task。私有诊断/融合/成本试验记录及原有未提交笔记保留本地；公开清单不引用未发布文件。
- 检查路径：原TEST、COMPILE、GUIDANCE-COMPILE；quick_validate；实际暂存commit门禁及真实SHA的committed门禁。历史change/场景证据保留为历史，不替代本次提交验证。
- 首次推送仍用Unreleased；推送确认后，以真实日期补CHANGELOG/README及受影响权威文档和本Task。该批仅补发布状态/证据，不改变行为，因此仍为1.4.4，无再次升版。
- 远程CI状态单独观察，不把本地门禁通过宣称为GitHub Actions通过；本任务不修改既有托管保护。

### 发布检查进度

- 发布树复核：21个暂存文件，63个本地Markdown目标存在；技能结构quick_validate通过。没有实验候选、私有研究Task、脚本或CI差异；原checks、control_plane、模块/清单和旧tasks保持不变。
- 首次commit检查中task-gate、control-plane、commit-scope及TEST（63.052秒）、COMPILE、GUIDANCE-COMPILE均pass；整体退出1，因为发布工作区尚无work目录，报告创建失败。该次不记为完整门禁通过。补齐报告目录后按原命令和必需检查重跑，不降低门槛。
