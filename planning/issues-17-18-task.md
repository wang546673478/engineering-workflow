# TASK-ISSUES-17-18：初始化默认排除与可选解析诊断

## 当前状态和授权

- 2026-10-19 Asia/Shanghai；阶段：本地实现与验证完成，待提交上传；基点 `0216e4cd341bee534ccc85a8824c83a40a7e9840` / 1.6.2，分支 `codex/issues-17-18`。上一评估记录和证据已保留；切换基点时只合并Baseline顶部冲突，保留1.6.2最新事实和所有历史。
- 用户原话（省略凭据）：“那就按照你建议修改然后回复issue,并关闭问题,然后上传GitHub”。该决定采纳[ASSESS-17-18-01](issues-17-18-assessment.md)的最小候选方案和验收，授权修复、完整验证、提交上传、对#17/#18回复及关闭；不改变checker/CI必需检查或代替托管平台独立环境审批。
- 需求状态：confirmed；完整方案：approved，范围是下列冻结规格/计划；实施状态：in_progress。旧发布批准不作为本次依据。凭据不保存到仓库或报告，不在命令输出中显示。
- 输入Baseline：BASELINE-CONTEXT-06及ASSESS-17-18-01；本批输出：BASELINE-UX-17-18-01。Spec：SPEC-UX-17-18-01；Plan：PLAN-UX-17-18-01；Trace：planning/traceability.md。
- release impact：1.6.2→1.6.3 PATCH，修正默认配置和已有能力的诊断/使用说明，保持旧清单、原状态枚举和可选采集行为兼容。同步VERSION、SKILL metadata、README、agents/openai.yaml、CHANGELOG；上传前保持Unreleased。
- 下一步：原change门禁已通过；执行commit/committed门禁并上传，再回复/关闭两issue并核对回执。

## 冻结规格与实施计划

| ID | 用户目标/验收 | 计划 | 状态 |
| --- | --- | --- | --- |
| REQ-UX-17 / AT-UX-17 | full/lite新清单显式排除各层node_modules；安装依赖前后政策相同；普通源码/相似目录仍覆盖，排除外链接拒绝，旧清单不自动迁移 | UX-01：复用已有 `**/node_modules`，不增加workspace格式解析或checker隐式忽略；端到端初始化/链接剪枝回归 | complete |
| REQ-UX-18 / AT-UX-18 | 终端/汇总清楚说明缺Rust/Node/TypeScript、恢复方法和部分覆盖；核心采集仍可用，已有unsupported契约保留；真正零引用可区分 | UX-02：在source-context中复用已有原因，兼容增加diagnostics/unsupported细节，区分执行错误与缺解析器；补降级、混合语言、空引用回归 | complete |
| REQ-UX-VERIFY / AT-UX-VERIFY | 全量回归环境需两类解析依赖；缺失时集中给出可操作错误，不能靠skip满足required；完整本地验证、上传及issue闭环 | UX-03：测试前置能力诊断、README与指南补安装入口；UX-04：版本/文档和原门槛；UX-05：精确提交上传后事实回复/关闭 | planned |

## Skill review

- catalog_source：当前会话Skills catalog；checked_at：2026-10-19T01:41+08:00；范围由只读评估扩大为已授权兼容修复、测试、skill打包元数据、GitHub上传和issue回复/关闭。
- adopted engineering-workflow：项目 `SKILL.md` 1.6.2 / 0216e4c；用户指定本机skill1.6.1也已读。重新核对AGENTS、manifest、当前Task、评估、Baseline、Spec/Plan、模块地图/契约/业务流及implementation-workflow/checker/source-context引用。延续原流程，版本和清单变化不放宽控制规则。
- adopted skill-creator：`C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`，未提供版本；正文及openai_yaml引用已读。用于窄范围资源修复、保持渐进披露及元数据/validator验证。
- not-adopted triage-issue：`C:/Users/54667/.agents/skills/triage-issue/SKILL.md`，未提供版本；前轮已读，已有issue且已定位，不创建重复issue或启用其委派流程。
- not-adopted planning-with-files：`C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，2.37.0；前轮已读，继续唯一manifest/Task联动状态，不建重复台账。
- 无其他适用候选，无显式多agent授权；单agent实施。工具用Git/公开API和用户本轮授权凭据；消息授权来自用户原话，不来自skill。

## 影响分析与控制文件说明

- instructions：仅新生成清单默认排除由根级扩展至各层node_modules；已有清单不改。README/指南说明依赖准备和新默认。源码阅读collector已有独立按名剪枝，checker显式排除契约不变。
- source-context：分析结果→输出status/summary/CLI增加诊断，保留原枚举和有效部分图；不修改checker或通用门槛，不自动安装被分析项目依赖。
- tests：缺环境时前置集中失败、真实解析回归和模拟缺依赖降级回归分开；不增加skip、不移除断言、不更改原TEST命令/120秒。
- governance：注册独立活动Task/Spec/Plan引用、版本记录和证据。manifest只登记本次范围、文档和授权，不改变checks、exclude_paths、protected_paths、approval_env、旧任务批准；SKILL正文只同步版本。VERSION/CHANGELOG受保护，这些具体变更由本轮用户明确采纳方案并要求上传覆盖；只对相应检查子进程传外部批准，不保存永久批准。
- 模块地图/CLI合约/业务流/Baseline/Spec/Plan/Trace更新；无业务数据库、权限、路由、事件或数据迁移，数据库视图不适用且适配器不变。
- 恢复：Git保留前轮评估stash及最新远程基点；新默认可由项目显式清单审阅调整。没有全局依赖安装、共享系统设置变更或生产数据操作。

## 验证与回执

本地实现完成。当前原change门禁required_checks_satisfied=true：TEST为170项/77.403秒，COMPILE0.232秒，GUIDANCE-COMPILE0.109秒，原120秒时限未改。诊断4、Rust10、JS/TS16、初始化6项focused通过；真实Windows目录连接full/lite夹具均通过，排除外连接继续拒绝。缺Rust/TypeScript时原测试类在setup集中报1个可操作错误、不发生IndexError，无skip。Skill package validator、版本一致、凭据模式扫描和原checker/CI/命令/保护政策不变核对通过。

当前证据：[fix evidence](issues-17-18-fix-evidence.json)，原报告/源码指纹保留在忽略的work/issues-17-18。旧163项评估结果仅作历史。提交/精确提交/远程与issue回执待完成；托管人工审批如要求独立用户决定，保留真实pending状态。辅助元数据核验首轮未显式指定UTF-8而遇到本机GBK解码失败，改为明确UTF-8后通过；未修改产品期望或检查范围。
