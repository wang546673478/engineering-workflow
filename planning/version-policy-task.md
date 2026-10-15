# TASK-VERSION-01：版本与 CHANGELOG 交付规则

日期：2026-10-15（Asia/Shanghai）；基准：`38e12360aee302529ad9c4fe17ccf934f707e281`，skill 1.4.1。开始时工作树干净。
状态：in_progress — 本地实现、规则审阅和测试已完成；用户已授权本次提交与上传，正在执行最终提交/发布检查。当前任务文件为本文件。适用路径：已有基线上的小范围规则补漏，复用 docs 中现有总览、模块、契约和业务流，不重新开展项目接管。

## 决定与范围

用户先询问版本号/CHANGELOG 的更新规则，随后明确要求：“根据更新版本号的规则是不是应该进行更新skill”。本次落实已解释的交付规则：一批实质变更统一升版，按兼容性决定幅度，同步版本文件和 CHANGELOG。更改 skill 指令本身也纳入版本影响。

本次候选版本：1.4.1 → 1.4.2，补齐遗漏的既定交付说明，未新增运行功能或修改公共 CLI/数据格式。CHANGELOG 使用 Unreleased，未冒称已发布。此前 1.4.1 已发布任务保持历史完成状态，旧提交/推送批准不扩展为本次新规则的最终提交批准。

本轮批准：用户于 2026-10-15（Asia/Shanghai，记录时间约 19:30）明确要求“提交GitHub吧”。该授权覆盖已经展示的版本/CHANGELOG 规则、引用、模板、权威文档和清单、1.4.2 元数据，以及必要的提交、推送和发布回执。此次收紧交付前升版与变更记录要求，保留项目既有策略；没有改变检查器、检查命令、保护路径或批准变量。批准只用于本批差异，不延伸至其他项目、issue 操作、GitHub 设置、标签/托管 Release 或部署。

## Skill review

清单来源：本会话 Skills catalog；检查时间：2026-10-15T19:22:55+08:00。范围：通用版本策略、变更记录、skill 指令及任务模板、元数据同步。
- engineering-workflow：adopted；来源 `../SKILL.md`；1.4.1 基准、1.4.2 候选；已读正文、implementation-workflow、project-agents-clauses、checker 及当前任务/权威总览，维护影响与状态闭环。
- skill-creator：adopted；来源 `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`，未提供版本；已读正文和 openai_yaml 引用，用于窄范围修正规则与技能结构检查。
- planning-with-files：not-adopted；来源 `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，未提供版本；复用现有 manifest/任务记录。
- tdd：not-adopted；来源 `C:/Users/54667/.agents/skills/tdd/SKILL.md`，未提供版本；不修改可执行行为，不新增只匹配文案的测试。

## 计划与影响分析

1. 正文明确交付时的版本/CHANGELOG 义务，在实施引用中定义细则与例外。
2. 同步项目条款和任务模板的 release impact，更新 README 与权威 Spec/模块/契约/业务流。
3. 同步 VERSION、SKILL metadata、README、agents/openai.yaml 为 1.4.2；CHANGELOG 增加待发布条目。
4. 独立规则审阅、版本一致性及技能结构检查，运行既有必需检查和文档变更范围核对，记录真实结果。

影响链：SKILL.md → implementation-workflow 的版本决策 → Task release impact → 项目既有版本来源与 CHANGELOG → 交付检查。仅 instructions/governance，无 checker/适配器/测试代码、数据库/迁移、业务 API 或依赖变化。收紧交付前的版本和变更说明核对；项目已有政策、无手工版本项目和多包策略有明确边界。无新自动升版器或自动检测器，不改变保护名单/批准变量/检查命令。

## 验收与验证计划

- REQ-VERSION-01 / AT-VERSION-01：明确定义交付单位、PATCH/MINOR/MAJOR 的默认规则、项目已有惯例优先、同步来源与验证证据。
- REQ-VERSION-02 / AT-VERSION-02：CHANGELOG 包含有意义的变更与兼容/迁移影响，未发布和已发布状态分开；只有进度/验证回执的收尾不循环升版，说明理由。
- 新增专业技术或产物类别时重新 review；当前规则变更采用范围不变。既有必需检查 TEST、COMPILE、GUIDANCE-COMPILE 不降低。

## Release impact

- 需要升版：是；类型 PATCH，理由为交付规范补漏、公共工具接口未变。
- 版本来源：本仓库 VERSION；同步位置 SKILL.md metadata、README、agents/openai.yaml，历史任务版本不改写。
- from/to：1.4.1 → 1.4.2；CHANGELOG：1.4.2 / Unreleased，日期待实际发布。
- 验证、提交和发布状态：本地结构、版本一致性及既有测试通过；本轮提交/上传已获授权，正在准备最终门禁。此前没有使用批准信号的报告保留为历史，当前只在本次检查进程中传入本轮批准。

## 进度与下一步

已完成规则恢复、skill review、计划、改前分析及说明和元数据同步。独立审阅指出目标版本可提前注明、免升版条件须保留项目既有规则，两处措辞均已修正；同时去除文档中把历史阶段记录称为“当前任务”的过期标签。用户现已批准提交/上传，下一步按以下发布计划执行。

## 发布计划与范围复核

- 已按当前来源重读 AGENTS、skill 正文、实施/检查器引用、当前任务和受影响文档，核对工作树；origin/main 与本任务基准 38e1236 一致。
- skill review 于 2026-10-15T19:30:42+08:00 复核：继续采用 engineering-workflow 与 skill-creator；产物为同一批说明和元数据的提交与上传，不引入其他专业技术或技能。增加一次独立只读发布审阅。
- 计划：记录本轮批准 → 校验版本、条目与差异 → commit 模式运行既有检查 → 提交 → committed 模式复核实际提交 → 推送并核对 SHA → 将真实发布日期/结果补入 CHANGELOG 与任务，再对收尾提交执行同等门槛并上传。
- 本轮仅更新状态、批准证据与实际发布记录，不改动规则行为；1.4.2 仍为同一交付批次，不再额外升版。远程 CI 没有验证结果时保持未验证。
- 发布前复核：独立只读审阅未发现阻碍发布的内容问题；1.4.2 四处版本值及 CHANGELOG 目标版本一致，quick_validate 与 git diff --check 通过，既有 checks/control_plane 未削弱。实际提交前后结果待运行。

## 实际验证结果

- `python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --run-checks --report work/version-policy-baseline.json`：exit 0，tool_version=1.4.2，TEST、COMPILE、GUIDANCE-COMPILE 均 pass，required_checks_satisfied=true。可选数据库/契约清单仍为 partial；无改动的检查器测试不证明 agent 一定遵循新规则。
- skill-creator `quick_validate.py .`：Skill is valid!；版本一致性核对通过（VERSION、SKILL.md、README、agents/openai.yaml 均为 1.4.2，CHANGELOG 为 1.4.2 / Unreleased）。既有检查命令与保护设置和基准完全相同。
- `change` 模式对 `38e1236`：manifest 与 change-scope pass，errors 为空；完整报告 exit 1，因为本次最终批准 pending，该次未运行的 TEST/COMPILE/GUIDANCE-COMPILE 为 skipped。实际测试通过证据来自上述 baseline，不冒称完整 change/commit/committed/handoff 通过。报告：work/version-policy-change.json。
- 场景复核：同一交付批次多次编辑只升一次；兼容纠错/新增兼容能力/不兼容分别选 PATCH/MINOR/MAJOR；项目政策和无手工版本/多包机制优先；收尾回执不循环升版；未发布目标版本不伪填发布日期；升版不授权远程写入。
- 最终措辞修正仅涉及 Markdown；测试代码、VERSION 和可执行脚本在测试运行后未改变。仅补此验证回执不再次升版，符合本批次规则；收尾技能结构、版本一致性、Markdown 本地链接与差异空白检查已通过。
