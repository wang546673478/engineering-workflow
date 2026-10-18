# Assessment adopted

On 2026-10-19 the user explicitly adopted this bounded recommendation and requested implementation, upload, replies and closure. Current state and fresh results: [TASK-ISSUES-19-21](issues-19-21-task.md). Candidate/unapproved statements below are historical decision inputs, not current execution status.

# ASSESS-19-21-01：GitHub #19 / #20 / #21 全局评估

## 当前状态和授权边界

- 2026-10-19，Asia/Shanghai；阶段：评估完成、可审阅。源码基点 `871bda427d3f46d114e568565dac10cca1395920` / 1.6.3；开始时工作树干净，GitHub main同一SHA。结论：三项均值得处理；#19最高优先，#20适合小范围补齐，#21必须拆分可处理中断与强制终止保证。[机器证据](issues-19-21-evidence.json)保存实际结果和源码指纹。
- 用户原话：“你再次看看issue,又提交了三个,进行评估是否值得修复,也给了修复建议,修复建议是否值得采用,你最好从全局来看这个修复建议”。本轮仅评估及记录，不继承#17/#18的实施、回复、关闭、上传授权。
- GitHub公开API于2026-10-19约02:13+08:00确认新open issue为[19](https://github.com/wang546673478/engineering-workflow/issues/19)、[20](https://github.com/wang546673478/engineering-workflow/issues/20)、[21](https://github.com/wang546673478/engineering-workflow/issues/21)，均无评论。
- 从manifest活动Task [TASK-ISSUES-17-18](issues-17-18-task.md)链接进入本评估子阶段；原需求/发布状态为历史，不转移其批准。输入事实基线为BASELINE-UX-17-18-01；目标修复仍是候选，不改变冻结Spec或源码。

## Skill review和影响范围

- catalog_source：本次会话Skills catalog；checked_at：2026-10-19约02:16+08:00；范围是Python检查器的输入边界、Git树一致性、子进程生命周期、hook/CI消费者和建议评估。
- adopted engineering-workflow：项目 `SKILL.md` 1.6.3 / 871bda4。重新读取AGENTS、manifest、活动Task及近期发布/验证、Baseline、Spec/Plan、模块地图、checker契约、implementation-workflow、project-documentation适用部分与历史#14-#16任务。源码路径明确，按source-context规则直接阅读，不运行无关JS/TS/Rust引用分析。
- not-adopted triage-issue：`C:/Users/54667/.agents/skills/triage-issue/SKILL.md`，未提供版本；前轮已读，当前已有issue，不创建重复issue或启用其委派/实施流程。
- not-adopted planning-with-files：`C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，2.37.0；前轮已读，复用现有权威状态，不建重复三文件台账。
- not-adopted skill-creator/tdd：本轮不改变skill资源或实施补丁；不需要新打包校验或强制TDD。无其他适用候选，无多agent授权。
- 调查链：输入JSON/历史Git manifest→validate→commit/committed初始树检查→声明命令执行/输出线程→报告→hook或CI消费。模块为checker、tests、instructions/governance；无业务数据库、产品权限、路由或业务数据迁移。

## 已核实源码事实

- #19：commit/committed在运行声明命令前检查工作树/暂存区；`run_checks`之后没有重复树检查，也没有报告验证时tree标识。hook模板仅消费checker退出码。需要同时评估暂存区、工作树、HEAD及最终实际commit绑定，而非只补一个hash比较。
- #20：文件JSON入口和Git历史manifest解析均未捕捉RecursionError；main的结构化异常边界也不包含它。单纯加深度/大小限制会产生新兼容政策；parse_constant与嵌套深度无关。
- #21：POSIX分支已经start_new_session=True，超时/超量已有killpg；Windows创建独立进程组但stop_process仅kill直接子进程。执行/队列等待没有覆盖KeyboardInterrupt的finally，也没有SIGTERM生命周期处理。SIGKILL不能在同一进程内捕获；try/finally不能保证该信号后的清理。

## 真实验证与结果

Windows/Python3.13.5；所有写入和玩具Git提交均在忽略的work/issues-19-21内，不改当前项目index/源码或GitHub。结果如下：

| 对照 | 真实结果 | 意义 |
| --- | --- | --- |
| commit执行期间改源码并git add | exit0、全部required通过，但前后index tree不同；随后玩具git commit确实提交了改变后的内容 | #19原始复现成立 |
| commit执行期间仅改工作树 | exit0、通过；index tree未变，src/app.py存在未暂存差异 | 只补write-tree对比会漏检 |
| commit执行期间改HEAD | exit0、通过；index tree未变，HEAD已变 | 需要同时绑定验证基点 |
| committed模式执行期间改index/仅改工作树 | 两种场景均exit0、通过，运行后分别存在树漂移/工作树差异 | 修复必须覆盖两种提交验证入口 |
| 测试临时改源码、读取它、再恢复并还原index | exit0、通过；最终HEAD/index/工作树均与开始一致，夹具记录已读取临时改变的源码 | 前后快照不能证明恶意命令全程只读取原树；不是沙箱 |
| 10000层对象JSON | 60002字节即RecursionError，exit1、traceback、无JSON报告 | 1MiB上限单独无法解决深度问题 |
| [] / null作为manifest根 | 均AttributeError，exit1、traceback、无JSON报告 | main在根类型验证前调用get，结构验证顺序也需补齐 |
| 10000位整数JSON | 10010字节，Python3.13解释器整数限制触发ValueError并溢出异常边界 | 只捕捉JSONDecodeError/RecursionError仍有同类缺口 |
| Git历史manifest解码10000层对象 | manifest_from_git直接抛RecursionError | 只修read_json漏掉另一个输入入口 |
| 在声明命令已启动后向检查器主线程注入KeyboardInterrupt | 普通直接子进程/孙进程均存活，输出读取线程仍1条 | 复现Python中断异常路径缺少清理；不是POSIX外部SIGINT原生测试 |
| 强制终止真实checker CLI父进程（Windows） | 普通直接子进程/孙进程均存活 | 同进程finally无法覆盖强制杀死 |
| Windows正常超时且存在普通孙进程 | timed_out=true；直接子进程结束，孙进程仍存活，reader_stalled=true | 单纯proc.kill连既有Windows超时的整棵树清理也做不到 |

所有自建子/孙进程在诊断finally中按本任务记录的PID清理，核实全部不再存活，读取线程最终为0。没有残留服务、系统设置或全局依赖变更。WSL不可用且未找到Docker/Podman；POSIX外部SIGINT/SIGTERM/SIGKILL行为仅做源码和操作系统语义分析，没有原生运行认证。不将Windows强制终止冒充Linux SIGKILL，也不据此声称GitHub runner取消一定会泄漏；runner可有额外进程清理机制。

## 逐条建议取舍

| Issue建议 | 评估 | 应采用的边界 |
| --- | --- | --- |
| #19 检查后比较git write-tree并列漂移路径 | 采纳，需扩充 | 在声明命令前后绑定HEAD和index tree，复核工作树/未忽略未跟踪差异；同时覆盖commit与committed。只要持久漂移就保持失败，保留诊断，不自动还原用户文件。采用Git对象语义保留换行/filter兼容。 |
| #19 verified_tree报告 + hook最后核对 | 辅助采纳 | 输出实际验证基点/树有助于报告与后续提交绑定；hook比较只能缩小时间窗口，其他hook或同用户并发代码仍可改变状态。独立CI需核对实际commit tree，不能把一个自报OID当强认证。不要只加字段而不执行后置检查。 |
| #19 只在checker.md声明暗道 | 必须澄清，但不足以修复 | 已作为现状限制补充；既有一致性目标保持有效，不能将缺陷改写为允许篡改的新需求。 |
| #20 read_json捕获RecursionError/ValueError等 | 采纳并统一入口 | 文件与Git历史解码都覆盖可预期的输入异常，根类型验证先于get；保留解释器整数保护，返回结构化配置错误、执行命令保持禁用。历史manifest损坏不能无审阅地视作正常首次接入/降低保护来源。避免用宽泛Exception吞掉真正程序错误。 |
| #20 固定1MB限制或手动深度计数 | 不作为本次主方案 | 已复现60KB深度输入，单纯大小限制无效；固定1MB会拒绝合法大清单。自行扫描须正确处理字符串/转义，维护成本高。资源上限属于单独的兼容政策，应先有容量证据。parse_constant不提供嵌套深度限制。 |
| #20 深度炸弹单测 | 采纳、扩大相关边界 | 验证深对象/数组、非对象根、大整数限制、Git历史/清单入口均结构化失败且不启动声明命令；正常大而浅输入仍按既有规则工作。 |
| #21 start_new_session + SIGINT/SIGTERM killpg | 部分已有，采纳缺失部分 | POSIX已创建独立会话和组终止能力，应复用它；补命令生命周期finally/可处理取消路径、限时wait/join和handler恢复。中断不得产生通过结果。避免在任意库线程中安装全局signal handler。 |
| #21 try/finally + proc.kill | finally采纳，单杀直接进程不足 | finally处理异常/中断的退出路径，清理须覆盖既有进程组/所声明的进程树边界和输出线程；Windows已实测单杀根进程遗留孙进程，需要平台适配而非照搬POSIX调用。 |
| #21 所有SIGKILL也必须无残留 | 不承诺由上述补丁保证 | SIGKILL无法被同一进程捕获。若要强制终止也保证清理，应单独设计OS生命周期约束：例如Linux cgroup/外部supervisor、Windows带kill-on-close的Job Object；考虑权限、嵌套job/runner兼容和进程启动时序。不是多加一个except/finally即可完成。 |
| #21 信号回归 | 采纳 | 原生POSIX信号与Windows取消/强制终止分别测试；验证普通子孙、线程/管道收尾、清理超时、handler恢复与取消不算成功。SIGKILL测试应针对选定的外部/OS约束能力，未提供该能力就明确不保证。 |

## 全局候选方案与影响（未实施）

1. 优先修#19。把提交验证视作“绑定输入状态→运行声明检查→验证状态仍一致→报告与实际commit核对”的单条链，两种提交模式共享一致性逻辑。后置检查必要；逐项检查后尽早发现漂移可缩短失败链，但仍须最终检查。保持有意生成的忽略构建产物可用；不要通过广泛忽略来掩盖源码漂移。
2. #20可作为同批独立小修。统一两个JSON解码入口的可预期异常及manifest根类型校验顺序，保留既有报错/退出语义和历史保护职责。无需引入新JSON库、任意文件上限或提高Python递归限制。
3. #21先确定并实现可处理中断的生命周期清理，同时覆盖Windows普通进程树边界；把不可捕获强杀后的强保证分成独立能力/延后项。若普通Windows父子/孙进程都要可靠绑定，优先评估OS Job Object等机制及CI兼容，不把taskkill/proc.kill或start_new_session当成跨平台完整保证。

这三项分别控制“验证内容是什么”“输入失败如何报告”“命令何时结束”。建议复用现有checker/Git/runner边界，增加有证据的检查，不重写整个工作流、不放宽required或审批。即使完整后置检查通过，同用户恶意代码仍可临时修改又恢复、伪造结果或攻击检查器本身；强安全依赖可信checker、受保护CI和OS隔离。新补丁的保证应写成可验证的状态一致性/生命周期合同，不能宣传任意项目代码已被沙箱化。

受影响文档/验收：模块职责、commit/committed和JSON退出合同、hook/CI结果消费者、进程终止/清理限制及测试矩阵；没有业务表或数据迁移。实际实施将涉及受保护checker/参考文档/版本与清单，按具体修复方案重新核对授权及既有控制门槛。若最终只做兼容缺陷修复，版本类型可为PATCH；新增强隔离/资源政策需另外判断兼容性，本评估不预先冻结版本。

## 基线更正与决定状态

现有文档里的提交树/工作树一致性检查，只能证明声明命令开始前的状态；本次6组对照证明运行期间/之后的一致性缺少实现。这是既有目标的缺陷，不是降低目标的决定。缺陷位于原checker代码，#17/#18批次没有修改它；旧170项及源码指纹证据并未被这次玩具复现推翻，但不能证明对恶意检查代码的防护。

当前事实已同步Baseline、合同和checker限制说明，保留旧审阅历史；未改冻结Spec或执行候选方案。后续涉及提交安全的设计应采用更正后的事实，不能依据旧“全程树一致”推论继续。

决定状态：agent建议，尚无用户采纳/实施批准。延后项：SIGKILL后的强生命周期隔离（checker/治理模块，需明确保证、平台/runner权限和兼容测试后恢复）；JSON资源容量/深度政策（输入模块，需真实规模及限制合同后恢复）；强沙箱/不同身份执行（治理/部署模块，只有明确不可信代码执行场景时另行设计）。保留现有独立有效工作，不把延后当已解决。

## 完成情况和下一步

本轮评估和受控复现完成，详见[证据](issues-19-21-evidence.json)。原始脚本、日志和玩具仓库留在work/issues-19-21；自建进程全部清理。仅补评估与事实文档，不改运行代码、测试、控制配置、版本或GitHub，不运行无关完整170项回归，不声称候选修复已验证。下一步向用户呈现优先级与建议；实施、回复/关闭和上传本批issue仍是未授权状态。
