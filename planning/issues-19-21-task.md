# TASK-ISSUES-19-21：提交状态、JSON输入和命令生命周期修复

## 当前状态与授权

- 2026-10-19 Asia/Shanghai；阶段：交付完成，源码发布及issue闭环已核实；基点871bda427d3f46d114e568565dac10cca1395920 / 1.6.3；分支codex/issues-19-21。保留前轮评估、复现与事实校正，不丢弃既有工作。
- 用户原话（不记录凭据）：“那就按照你建议修改然后回复issue,并关闭问题,然后上传GitHub”。明确采纳[ASSESS-19-21-01](issues-19-21-assessment.md)，授权下列方案、必要回归/元数据/文档、提交上传、对#19/#20/#21回复和关闭；独立托管环境审批仍由人类完成。
- 需求状态confirmed；完整方案approved；实施状态complete。输入BASELINE-UX-17-18-01加ASSESS-19-21-01；冻结SPEC-SAFE-19-21-01；计划PLAN-SAFE-19-21-01；输出BASELINE-SAFE-19-21-01。
- release impact：1.6.3→1.6.4 PATCH，修复既有一致性/错误处理/清理合同，不增加工作流阶段、放宽验证或承诺任意恶意代码沙箱。同步VERSION、SKILL、README、agents/openai.yaml和CHANGELOG；实际上传前Unreleased。
- 下一步：源码、原始跨平台验证和issue闭环已完成；仅回执按原门槛提交，后续新SHA的托管状态独立核对。

## 冻结规格和方案

| 需求/验收 | 实施项 | 边界与验证 | 状态 |
| --- | --- | --- | --- |
| REQ-SAFE-19 / AT-SAFE-19 | SAFE-01 | 两种提交模式在读取验证输入前绑定HEAD/index tree，声明命令之后复核HEAD/index/worktree及未忽略新文件；漂移不得通过、不自动还原用户数据。成功报告输出verified_tree和verification_head；测试持久漂移、正常及忽略产物、真实提交绑定。前后恢复的恶意代码、hook后竞争和沙箱继续明确限制 | complete |
| REQ-SAFE-20 / AT-SAFE-20 | SAFE-02 | 文件和Git历史共用JSON异常边界；深度/整数/根类型错误输出JSON配置错误且不执行命令；历史损坏不得静默降为首次接入。不加任意1MB限制、不提高解释器保护上限 | complete |
| REQ-SAFE-21 / AT-SAFE-21 | SAFE-03 | finally清理拥有的进程组/树与读取线程，CLI可处理SIGINT/SIGTERM并恢复handler，中断非成功。Windows使用Job Object及挂起创建→赋予job→恢复，失败时拒绝执行并清理；验证普通子孙、超时和中断。POSIX不可捕获SIGKILL及Windows赋予job前的启动窗口不作绝对保证，强隔离仍延后 | complete |
| REQ-SAFE-DELIVERY / AT-SAFE-DELIVERY | SAFE-04..05 | 1.6.4版本/当前Baseline/Spec/Plan/Task/Trace与模块/合同/业务流同步；原门槛、精确上传、issue回复关闭及真实托管回执分别核对 | complete |

## Skill review

- 来源：当前会话Skills catalog；检查时间2026-10-19约02:30+08:00；范围由评估扩大为用户采纳的Python检查器修复、跨平台进程适配、打包元数据和GitHub发布/issue闭环。
- adopted engineering-workflow：本仓库SKILL.md 1.6.3/871bda4；重新读取AGENTS、manifest、活动Task、评估、基线/Spec/Plan、模块地图/合同/业务流与implementation-workflow/checker相关引用。
- adopted skill-creator：C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md，未提供版本；正文及openai_yaml引用已读，用于限定资源修复与元数据/package validation，不改变调用政策。
- not-adopted triage-issue：C:/Users/54667/.agents/skills/triage-issue/SKILL.md，未提供版本，前轮已读；不创建重复issue或引入其委派流程。
- not-adopted planning-with-files：C:/Users/54667/.agents/skills/planning-with-files/SKILL.md，2.37.0，前轮已读；已有权威工件，不建重复台账。tdd未显式要求，采用公共行为回归但不另加流程。
- 单agent执行；未授予多agent。来源/技术范围改变时重新review。凭据只供本次受权远程操作，不进仓库/日志。

## 影响与控制面变化

- checker：JSON入口、提交验证链、声明命令/信号/输出线程生命周期；均集中在受保护check_project.py，避免将关键逻辑移到未受保护入口。
- tests：保留旧断言，新增真实Git漂移、异常输入和平台生命周期回归。生成测试marker作为明确忽略产物，另测未忽略新文件失败；不弱化树检查或减少原用例。
- instructions/governance：说明报告新增字段、合法生成产物、取消与强杀保证边界；冻结新Spec/Plan，登记新Task、版本和证据。hook/CI继续消费checker退出码；不声称本地hook是沙箱或独立安全审阅。
- 原checks/120秒与编译时限、排除政策、批准变量、protected_paths和CI/finalizer不放宽。新增verification-state会收紧两种提交模式：检查执行后的持久改变也导致失败；损坏历史JSON会明确失败；Windows无法建立进程约束时拒绝执行。
- 这些具体收紧及checker/参考文档/清单/版本变更由本轮明确采纳方案并要求上传覆盖；外部批准只用于对应子进程，不保存永久批准，不代替GitHub环境required reviewer。
- 无业务数据库、路由、权限或数据迁移；metadata adapters保持原范围。全平台SIGKILL容器/不同身份沙箱、JSON容量上限维持延后；此批不安装WSL或改系统配置，POSIX原生验证由现有CI承担。

## 验证和发布记录

本地核心实现完成，当前状态/输入8项focused及生命周期6项focused全部通过。生命周期包括真实Windows ordinary后代、正常/超时、取消、约束建立后的父进程强制终止、handler恢复和setup失败不运行命令。真实POSIX信号仍待已有Ubuntu CI；没有安装WSL或改系统。

第一轮完整184项TEST/114.516秒以及原COMPILE/GUIDANCE-COMPILE通过。之后只对Git树相等的重复计算、输出EOF后的等待和signal注册异常收尾作等价完善，focused14项重新通过；该第一轮报告保留为历史诊断，最终源码以即将执行的commit/committed结果为准，原120秒不变。

初始checker诊断发现旧marker产生未忽略文件，被新后置检查正确拒绝；fixture明确忽略其生成marker，并另测unexpected文件必定失败。初始历史JSON回归仅断言错误所在字段不当，已改为断言结构化非成功、具体原因和不执行命令；清理了导入TestCase导致重复发现的问题。未删除原回归或放宽任何规则。

版本/package validator、原checks/时限、保护范围/批准变量/排除/CI不变、凭据模式扫描通过；源代码指纹和原始报告见[fix evidence](issues-19-21-fix-evidence.json)。前轮评估仅证明原缺陷，不当作新补丁通过。最终提交、托管及issue回执待完成。


## 最终实现验证、发布与issue回执（2026-10-19）

- 最终暂存门禁通过：TEST184项107.669秒，原COMPILE0.219秒、GUIDANCE-COMPILE0.216秒；实际提交树256d0076690b85b2633e6b433656de6e650feef3与报告verified_tree一致。
- 精确实现提交5f9b3e1d54a0709241fb5f11173e13ce00af3ffd的committed门槛通过：TEST184项107.619秒，原两编译通过，verification-state通过且返回同一tree；原120秒未改。
- 候选分支codex/issues-19-21先上传；[run39157028881](https://github.com/wang546673478/engineering-workflow/actions/runs/39157028881)获wang546673478的独立环境批准。两个原始committed报告均tool_version1.6.4、全部required通过，verification_head=该SHA、verified_tree=该tree；artifact下载SHA256与API digest一致。Windows TEST89.125秒，Ubuntu20.017秒，原编译均通过。实际覆盖POSIX SIGINT/SIGTERM及进程组收尾、Windows Job/普通后代与取消。
- 两平台原始报告核验后，同一SHA非强制上传main并用API核对。实际发布日期（Asia/Shanghai）为2026-10-19，CHANGELOG由Unreleased改为真实日期；未创建Release/tag或改写远程历史。
- 已回复并关闭为completed：[19回复](https://github.com/wang546673478/engineering-workflow/issues/19#issuecomment-6253939392)、[20回复](https://github.com/wang546673478/engineering-workflow/issues/20#issuecomment-6253939733)、[21回复](https://github.com/wang546673478/engineering-workflow/issues/21#issuecomment-6253940030)。回复含实际提交/CI证据，#21明确保留POSIX SIGKILL、Windows pre-assignment窗口及沙箱限制，未冒充实现强隔离。
- 本次仅统一发布日期、完成状态、CI/上传/issue证据；源码指纹和验收不变，仍同批1.6.4，无需再升版。回执仍运行原commit/committed，原始文件为work/issues-19-21/receipt-commit-01.json、receipt-committed-01.json；其后新CI运行按精确SHA独立报告，不复用旧审批作新结果。
