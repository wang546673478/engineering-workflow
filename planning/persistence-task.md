# TASK-PERSISTENCE-01: 项目持久化指引与 GitHub issue 审计

Updated: `2026-10-15` Asia/Shanghai
Status: `complete` — 持久化与 issue 修复已验证，用户已批准提交与推送
Base commit: `1aae5ed`
Requirements: `REQ-PERSIST-01`–`REQ-PERSIST-03`
Acceptance: `AT-PERSIST-01`–`AT-PERSIST-03`

本文件是本次任务的计划、影响分析、决定、进度、skill review、验证和交接的权威记录。[项目清单](../engineering-manifest.json)通过 `PERSISTENCE_TASK` 指向本文件。此前 `TASK-SELF-01` 的[变更记录](change-impact.md)、[基线批准](baseline-review.md)和 [skill review](skill-review.md)均属于历史任务，不作为本次批准或本次验证。

## 用户请求与范围

用户于 2026-10-14 显式调用 engineering-workflow，并提出：

> 你看看github仓库里面提交的issuse,有哪些值得修改,然后我这边希望的是把启用过engineering workflow的项目都写进agents.md里面作为持久化的指导,当然这个只是chatgpt的做法,你还要考虑其他agent

用户提供的初始提示词：

> ## Engineering workflow
> 工程任务默认使用 engineering-workflow skill。
> 发生 resume、上下文压缩或任务范围变化后，重新读取该 skill 和任务状态文件。
> 计划、决策、进度和验证结果必须写入文件，不能只依赖聊天上下文。

本次范围：审计仓库 issue #2–10；完善 skill 的项目级持久化接入说明、模板和安装器；在本仓库示范 `AGENTS.md` 接入；记录其他 agent 的薄引用方式；补齐本次文档和验证证据。用户的目标在这里落实为可重复使用的接入机制。尚未枚举或批量改写用户所有历史项目，也不声称所有启用过的项目都已经接入。

本次未实施 issue #2–10 的 checker、提取器或轻量模式修改，未更改 GitHub issue 状态，未发布消息。未提交、未推送；最终 protected-change 批准为 `pending`，没有设置外部批准信号。

## GitHub issue 审计与实施状态

本轮已进入 issue 实施范围：#2、#3、#4、#5、#6、#7、#8、#9、#10 的对应代码或文档改动正在当前工作树中验证；#1 已关闭。未更改 GitHub issue 状态，未发布消息。未提交、未推送；最终 protected-change 批准仍为 `pending`。

审计日期：2026-10-14。依据为仓库 issue 页面正文与本地 `1aae5ed` 源码/模板；issue 作者的三个项目实测属于报告证据，本任务没有重新运行那些外部项目。以下优先级是本次审计建议。

| Issue | 优先级与判断 | 建议修改及边界 | 本次状态 |
| --- | --- | --- | --- |
| [#2：排除路径与 pnpm 符号链接](https://github.com/wang546673478/engineering-workflow/issues/2) | 第一批；真实可用性缺陷 | 遍历前剪枝排除目录，同时保留未排除路径的根目录约束；用 pnpm 类目录与越界链接场景验证 | 仅审计，未修复 |
| [#3：检查工作目录](https://github.com/wang546673478/engineering-workflow/issues/3) | 第一批；子目录项目的直接阻塞 | 为检查显式声明项目内工作目录，默认项目根；拒绝不存在或越界目录，保持参数数组执行 | 仅审计，未修复 |
| [#5：文档门槛语义与模板](https://github.com/wang546673478/engineering-workflow/issues/5) | 第一批；文档/示例需要修正 | 明确合法变更范围、全部文档必须更新的语义和 governance 模块；先补可用示例，`any_of` 另作需求判断 | 仅审计，未修复 |
| [#8：声明了弱检查仍通过](https://github.com/wang546673478/engineering-workflow/issues/8) | 第一批；验证可信度问题 | 对照项目权威验证命令，记录替代检查理由和未覆盖项；不能用机械扫描声称证明所有检查足够 | 仅审计，未修复 |
| [#4：首次接入批准流程](https://github.com/wang546673478/engineering-workflow/issues/4) | 第二批；接入引导缺失 | 说明首次创建 manifest 的控制面审阅和一次性批准含义，提供清楚诊断；保留对具体规则变更的人类审阅 | 仅审计，未修复 |
| [#6：需求/验收 ID 的字面要求](https://github.com/wang546673478/engineering-workflow/issues/6) | 第二批；降低重复文档 | 考虑锚点或明确索引映射，保留需求到验收的可追溯性，不强迫重写项目原有正文 | 仅审计，未修复 |
| [#7：清单输出更新](https://github.com/wang546673478/engineering-workflow/issues/7) | 第二批；常见维护成本 | 设计显式更新选项和安全替换流程；保留默认防误覆盖以及源/输出隔离 | 仅审计，未修复 |
| [#9：LICENSE、版本与变更记录](https://github.com/wang546673478/engineering-workflow/issues/9) | 发布前补齐 | 版本与变更记录能提高可追溯性；许可证类型由维护者选择，不能代其作法律授权决定 | 仅审计，未修复 |
| [#10：轻量模式与首次接入成本](https://github.com/wang546673478/engineering-workflow/issues/10) | 后续设计重点；先明确裁剪边界 | 复用已有项目规则/检查与文档，区分一次接入成本和每任务成本；轻量模式需单独定义最低证据，不以减少真实验证换取流程便利 | 仅审计，未实现 lite schema |

本次持久化入口帮助复用项目既有状态；本轮同时加入 #4 的首次接入诊断、#8 的验证边界说明和 #10 的 `init_manifest.py` full/lite 骨架。它不等于已经完成所有 issue 的远程验证，也不解除具体控制面变更的人工批准门槛。

## 方案与决定

1. `AGENTS.md` 保存稳定入口和规则，项目现有清单及状态文件保存任务内容；优先复用已有文档，避免为同一事实维护两份记录。
2. 开始、恢复、接手、上下文不完整、切换 agent 或范围变化都是可跨宿主表达的恢复时机。恢复时核对项目规则、skill 来源/revision、清单、活动任务、近期进度及工作树；范围变化补做 skill review 和影响分析。
3. 其他宿主的原生入口只薄引用 canonical `AGENTS.md` 和项目状态。适配以实际使用的宿主为准，不默认写满所有工具的文件；不保证每个宿主自动发现或递归读取引用。
4. 安装器只维护自己的标记区，保留用户规则。重复执行应幂等；错误标记和越界目标必须被拒绝。安装器的真实保证以最终测试与实现为准。
5. 本次不增加新的 checker schema；以现有 documents/tasks/documentation_impact 记录任务与文档。旧任务的批准、required checks 和 public-guidance 声明保留原样。
6. 新 `GUIDANCE-COMPILE` 检查覆盖新增安装器；原有 `TEST` 通过现有发现机制覆盖新增回归测试。既有项目测试命令未被弱化。

这些是本次实现决定，不是用户对完成结果的批准。需在最终审阅时说明：持久化入口/恢复要求被补充，清单新增任务和安装器检查，checker 的已有保护行为未被放宽。

## 计划与进度

| 阶段 | 状态 | 产物/后续动作 |
| --- | --- | --- |
| 阅读 skill、现有基线与 issue | 已完成审计 | 使用现有源码和 issue 正文形成上表；未复跑外部项目实测 |
| 定义持久化入口与跨 agent 边界 | 已形成方案 | `AGENTS.md` 稳定入口、原生入口薄引用、文件恢复与显式未验证状态 |
| 修改 skill 指引、模板与安装器 | 工作树中进行 | 主 agent 继续完善安装器和模板，最终行为需重新核对 |
| 补齐本次任务及文档映射 | 已写入，待最终复核 | 本文件、manifest、新需求/验收、模块地图、业务流和接口契约 |
| 对最终源码验证 | 已完成 | 63 项 unittest 通过；Python 编译、skill-creator validator、baseline required checks 均通过；非必需数据库/契约清单保持 partial |
| 最终 protected-change 审阅 | pending | 展示完成差异和效果；不可复用旧任务批准或设置批准信号 |
| 提交与推送 | 未执行 | 本次没有发布结果 |

## 影响分析

- 影响模块：`instructions`、`tests`、`governance`。新增安装器属于 instructions；tests 对 instructions 的依赖在模块清单中明确登记。
- 调用链：skill 指引 → 接入模板/安装器 → canonical `AGENTS.md` → 项目清单及活动任务；其他 agent 的原生入口 → `AGENTS.md`。因此更新模块地图、业务流和契约。
- 公开入口：`README.md`、`SKILL.md`、`references/project-agents-clauses.md`、`references/implementation-workflow.md`、`assets/templates/AGENTS.engineering.md`、`scripts/install_agents_guidance.py` 和本仓库 `AGENTS.md`。
- 持久文件：项目 instruction 文件中的 managed block；项目计划/状态由 agent 按权威位置更新，不把用户项目数据写入 skill 包。
- 控制面：`SKILL.md` 和 manifest 本次变化需要最终人类审阅；`control_plane` 的保护名单及批准变量未修改。文档记录没有给安装器、agent 或其他宿主额外权限。
- 数据库：不适用；检查本次改动范围未涉及数据库适配器、元数据格式、业务表/字段或迁移，现有[数据库边界](../docs/database.md)继续有效。
- 兼容与恢复：保留 marker 外的项目规则；原生入口避免复制完整规则；skill 不可读取或宿主未验证时记录 unavailable/unverified。可在审查差异后撤销本次管理区或恢复先前版本，不能自动覆盖用户规则。
- 本次已触及 checker、提取器和 bootstrap 的受控改动；CI/远程托管行为未改变，GitHub issue 回复会明确区分本地验证与远程用户测试。

## Skill review

Catalog source: 本会话 Codex Skills catalog。检查时间：`2026-10-14T21:16:01+08:00`。范围：issue 审计、现有 skill 修改、持久化文件和安装器。下列“未采用”候选依据宿主目录描述筛选，未声称完整读过不适用 skill。

| Skill | 来源 | 版本/日期 | 决定与证据 |
| --- | --- | --- | --- |
| engineering-workflow | `C:/Users/54667/.codex/skills/engineering-workflow/SKILL.md` | 未提供；本仓库 base `1aae5ed` | adopted；用户显式调用，已读入口及持久化/实现/检查器相关引用 |
| skill-creator | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md` | 未提供 | adopted；已读，用于现有 skill 的范围、结构和验证 |
| planning-with-files | `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md` | 未提供 | not-adopted；现有 manifest 和本任务记录已承担计划/状态持久化，不另建平行状态体系 |
| tdd | `C:/Users/54667/.agents/skills/tdd/SKILL.md` | 未提供 | not-adopted；未请求 test-first，使用项目现有 unittest 验证新增安装器 |
| setup-pre-commit | `C:/Users/54667/.agents/skills/setup-pre-commit/SKILL.md` | 未提供 | not-adopted；本次不安装 Husky 或新 hook |

其他文档、表格、演示、图像、浏览器 UI、架构重构、PRD/issue 创建类技能与当前产物不匹配。新增安装器后复核仍采用前两项；若实施任一被审计 issue 或扩大到宿主产品配置，需要重新评估相关技能。

## 当前验证与批准

以下状态针对本次任务。旧任务记录中的 56 项测试、发布 commit 和远程运行都只是历史证据，不能当作当前通过。

| 检查/审阅 | 当前状态 | 证据或待办 |
| --- | --- | --- |
| manifest JSON 格式 | 已检查格式 | 文档子任务读取并解析当前 JSON；不代表 checker 或业务门槛通过 |
| 完整 unittest | 通过 | `python -m unittest discover -s scripts/tests -q`：77 tests，约 53 秒，exit 0 |
| 既有脚本与安装器编译 | 通过 | `python -m py_compile ...`；baseline 中 `COMPILE` 与 `GUIDANCE-COMPILE` 均 pass |
| skill-creator 验证 | 通过 | `quick_validate.py .`：`Skill is valid!`；使用 UTF-8 与任务目录下 PyYAML |
| 本地链接、文档/变更范围 | 通过/有限制 | manifest baseline required checks satisfied；`git diff --check` 无空白错误；仍需人工核对语义连通性 |
| commit/committed 保护检查 | 未通过本任务批准路径 | 最终批准 pending；不得设置外部批准信号以求通过 |
| 其他宿主自动加载 | 未验证 | 文件适配不等于实际宿主集成测试 |
| 最终人类批准 | approved for commit/push | 用户于 2026-10-14 23:11 Asia/Shanghai 指示“提交到github”，批准当前工作树中本任务完整 issue 修复、持久化改造、版本元数据、文档和测试范围 |
| 提交/推送/远程 CI | 已完成提交与推送 | commit `05748f8ad816dd3fe33b984839c22a71773fd767` 已推送到 `origin/main`；`committed` required checks 已通过；GitHub hosted CI 未在本次操作中等待或验证 |

## Issue implementation verification

This follow-up implementation was verified on the final working tree on 2026-10-14:

- `python -m unittest discover -s scripts/tests -q`: 77 tests passed in about 53 seconds.
- `python -m py_compile scripts/check_project.py scripts/extract_sqlite.py scripts/extract_database.py scripts/install_agents_guidance.py scripts/init_manifest.py`: passed.
- `python .../skill-creator/scripts/quick_validate.py .` with UTF-8 and the task-local PyYAML: `Skill is valid!`.
- `python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --run-checks`: required checks satisfied. The optional database and manually maintained contract inventories remain `partial` by design.
- `git diff --check`: no whitespace errors. GitHub issue comments are a separate external write and do not constitute code or hosted-CI verification.

Implementation status: #2/#3 checker fixes, #4 bootstrap diagnostic/docs, #5 DSL documentation and governance example, #6 trace index/anchor support, #7 safe snapshot update mode, #8 verification-boundary guidance, #9 version/license/changelog metadata, and #10 full/lite manifest bootstrap are present in the working tree. Real project compatibility, host-specific agent loading and remote CI remain unverified until the user tests them.

Issue replies posted on 2026-10-14:

- [#2 comment](https://github.com/wang546673478/engineering-workflow/issues/2#issuecomment-6171078796), [#3 comment](https://github.com/wang546673478/engineering-workflow/issues/3#issuecomment-6171079373), [#4 comment](https://github.com/wang546673478/engineering-workflow/issues/4#issuecomment-6171080032)
- [#5 comment](https://github.com/wang546673478/engineering-workflow/issues/5#issuecomment-6171080563), [#6 comment](https://github.com/wang546673478/engineering-workflow/issues/6#issuecomment-6171080958), [#7 comment](https://github.com/wang546673478/engineering-workflow/issues/7#issuecomment-6171081328)
- [#8 comment](https://github.com/wang546673478/engineering-workflow/issues/8#issuecomment-6171082221), [#9 comment](https://github.com/wang546673478/engineering-workflow/issues/9#issuecomment-6171082634), [#10 comment](https://github.com/wang546673478/engineering-workflow/issues/10#issuecomment-6171083386)

## 交接

本次提交前已完成安装器、模板、checker、适配器、bootstrap、版本元数据及 issue 回复的核对。提交后记录实际 commit SHA、push 结果和远程 CI 状态；本文件不把远程 CI 或真实项目兼容性预先写成已验证。

提交结果：`05748f8ad816dd3fe33b984839c22a71773fd767` 已发布到 `origin/main`。本地 `committed` 复核于提交后通过；远程 GitHub Actions 和用户真实项目兼容性仍待外部测试。

Actions 运行 `38596234931` 已通过环境审核：control-plane 与 committed-scope 通过，首次 `TEST` 调用返回 1；同一 job 的诊断重跑显示 79 项测试全部通过。现有 workflow 的失败传播逻辑会让诊断成功后 job 仍保持失败。本次修复让验证步骤允许进入诊断，由诊断结果决定最终状态，同时继续要求除 TEST 外所有必需检查通过。

后续 Actions 修复：提交 `5e0a44f` 的 Linux/Windows Quality 运行在测试前失败，原因是 workflow 仍选择旧任务 `TASK-SELF-01`，而该提交只改变了本任务状态文件，触发旧任务的历史 `baseline-docs` 门槛。修复改为由 manifest 的 `workflow.active_task` 指向 `TASK-ISSUES-01`，push/PR workflow 不再复制任务 ID，并把 `.github` 纳入本任务的控制面影响规则；修复后的 Actions 结果待 GitHub 新运行返回。旧 `TASK-SELF-01` 作为历史任务保留，不再作为当前 CI 默认任务。

## Follow-up GitHub issue audit (2026-10-15)

本次用户请求是查看上一轮之后新增的 issue；本节只记录远程只读审计，不把旧任务的批准或完成状态延伸到新代码变更。审计使用 GitHub 公共 API 读取仓库 `wang546673478/engineering-workflow` 的 issue 列表、正文和仓库元数据；本机未安装 `gh`，没有使用或保存用户在聊天中提供的凭据。当前未关闭 issue 只有 #11、#12、#13，未发现 #14 及以后；#2–#10 已关闭。

| Issue | 判断 | 证据与建议 | 当前状态 |
| --- | --- | --- | --- |
| [#11：`check_project.py` 版本常量仍为 1.3](https://github.com/wang546673478/engineering-workflow/issues/11) | 高优先级、小范围 bug | 远程复测记录 `main @ 5b8babf`；本地 `scripts/check_project.py:16` 仍为 `VERSION = "1.3"`，而 `VERSION` 与 `CHANGELOG.md` 为 1.4.0。应统一版本来源或同步常量，并增加报告 `tool_version` 回归测试。 | open，未修改 |
| [#12：反斜杠 manifest 路径在 Linux 上失败](https://github.com/wang546673478/engineering-workflow/issues/12) | 中高优先级、真实可用性 bug | `safe_path()` 直接构造 `Path(raw)`，而 `covered()` 另行归一化分隔符；远程复测确认 Windows 风格文档路径在 Linux 上被当作错误文件名。应在安全路径入口统一归一化，同时保留盘符、UNC、越界和链接安全测试。 | open，未修改 |
| [#13：`exclude_paths` 无 glob、`when_paths` 不支持公共父目录](https://github.com/wang546673478/engineering-workflow/issues/13) | 中优先级、需要产品/规则决定的增强 | 当前 `exclude_paths` 和 `when_paths` 使用词法前缀匹配；任意层 `node_modules`、多模块公共父目录的语义尚未定义。需要先决定 glob 语法、排除目录剪枝和公共父目录是否仅作为触发器，随后再改 schema、文档和测试。 | open，未修改 |

### Follow-up scope and verification

- 审计阶段没有创建新的 manifest task，也没有修改源代码、issue 状态或 GitHub 内容；随后用户授权实施 #11-#13，已在独立的 [TASK-ISSUES-02](issues-11-13-task.md) 中记录新的范围、决定、影响分析、skill review 和验证计划。旧的 `TASK-ISSUES-01`/`TASK-PERSISTENCE-01` 仍只代表已经发布的上一轮范围。
- 范围复核：2026-10-15 重新读取本仓库 `SKILL.md`（metadata 版本 1.4.0）及 `references/checker.md`、`references/project-agents-clauses.md`、`references/implementation-workflow.md`；`engineering-workflow` 继续采用。`skill-creator` 未采用（没有修改 skill 包结构），`tdd` 未采用（没有实现或新增测试）。本次只读审计的影响限于本记录和远程 issue 证据，不触发代码模块、契约或数据库文档门槛。
- 新任务已明确 #13 的 glob 和公共父目录语义；其保护性实现不能复用旧批准，最终状态以 `TASK-ISSUES-02` 为准。
- 本轮本地证据：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline` 的报告仍显示 `tool_version: "1.3"`；源码、版本文件和远程 issue 正文相互印证。未运行新修复测试，因为本轮是审计而非实现。
