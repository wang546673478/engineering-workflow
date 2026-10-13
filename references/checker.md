# 项目自动检查

检查器仅依赖 Python 标准库。默认只读，`--report` 仅创建新报告文件，拒绝覆盖；`--run-checks` 才执行项目明确声明的命令。命令是非空参数数组，使用 `shell=False`，不解释管道或命令拼接，运行前需核对项目命令与授权。

```text
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode baseline
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode change --base <commit> --task TASK-01
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode handoff --base <commit> --task TASK-01 --run-checks --report new-handoff-report.json
ENGINEERING_TASK_ID=TASK-01 python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode commit
ENGINEERING_TASK_ID=TASK-01 python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode committed --commit-ref <commit-sha> --run-checks
python <skill-dir>/scripts/extract_sqlite.py <checkpointed-project.sqlite> --output new-database-inventory.json
python <skill-dir>/scripts/extract_database.py mysql --url-env ENGINEERING_DATABASE_URL --schema app --output new-database-inventory.json
python <skill-dir>/scripts/extract_database.py postgresql --url-env ENGINEERING_DATABASE_URL --schema public --output new-database-inventory.json
python <skill-dir>/scripts/extract_database.py redis --url-env ENGINEERING_DATABASE_URL --output new-database-inventory.json
```

baseline 核对声明结构和资料；change/handoff 必须提供 Git base 和任务，包含删除、重命名前后路径及未跟踪文件。base 先解析为 commit OID，不能传 Git 选项。handoff 还核对批准、前置任务、完成状态与本次实际验证。基线不要求 Git；首版无 Git 项目无法完成自动变更范围核对，保持未验证，不以基线检查替代完整交付。

`commit` 是本地提交门禁：只读取当前 Git index 中已暂存的路径，拒绝空暂存区和任何未暂存的工作树差异，防止从工作区读取到与提交内容不一致的文档或清单。它会将源代码路径与 `task.documentation_impact` 中的触发路径关联，源代码变更未声明门槛也会失败；遗漏任一文档时退出失败。初始提交使用空树比较，删除和重命名同时检查旧路径与新路径。任务 ID 可用 `--task` 指定，也可通过 `ENGINEERING_TASK_ID` 提供；命令行参数优先。

`committed` 用于 CI/受保护分支复核已生成的提交：checkout 必须位于 `--commit-ref`，按该 commit 与父提交（根提交则用空树）比较，并拒绝工作树/index 偏离提交树。CI 应对待合并的每个提交运行该模式；本地 hook 可被跳过，不能作为唯一门禁。复制 [POSIX 模板](../assets/templates/pre-commit.engineering) 或 [PowerShell 模板](../assets/templates/pre-commit.engineering.ps1) 作为本地 hook；CI checkout 每个待检 commit 后可调用 [POSIX CI 模板](../assets/templates/ci-committed.engineering) 或 [PowerShell CI 模板](../assets/templates/ci-committed.engineering.ps1)。两个 CI 模板都要求显式指定 commit SHA 和该提交的任务 ID。

The JSON result contains `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, and `errors`. Exit code 0 means every required check passed; 1 means a required validation failed; 2 means malformed configuration, unavailable environment, or an unsupported required check. `pass`, `fail`, `partial`, `unsupported`, `skipped`, and `error` are reported separately. Partial, skipped, or unsupported required checks cannot satisfy completion.

## 项目清单字段

从 [清单示例](../assets/templates/project-manifest.example.json) 调整实际路径；示例状态为 planned，直接复制不会被视为已完成。

| 字段 | 含义及关联 |
| --- | --- |
| schema_version | 整数 1；不是字符串或布尔值 |
| documents | id、path、kind、required；声明文档，required 为布尔值；被需求/模块/任务引用的文档即使标可选也必须存在 |
| requirements / acceptance | id、document；document 指文档 ID，编号必须出现在对应资料里 |
| modules | id、source_paths、document、depends_on、allowed_dependencies；文档为 ID，实际依赖必须属于允许依赖且无循环；此图仅为声明图 |
| inventories | id、kind、path、documentation、required；path 指源清单 JSON，documentation 指文档映射 JSON，不是文档 ID |
| checks | id、command、required、timeout_seconds；command 是参数数组，超时为有限正数；无隐式 shell |
| tasks | id、requirement_ids、acceptance_ids、module_ids、depends_on、status、impact_document、required_checks、approval_required、approval、documentation_impact；commit 门禁通过 `--task` 或 `ENGINEERING_TASK_ID` 选择任务 |
| task.status | planned、in_progress、blocked、complete；handoff 要求 complete，但状态不证明人已审查 |
| task.impact_document | 已声明的文档 ID；对应修改前影响记录 |
| task.required_checks | 已声明检查 ID；选定任务的必需检查强制生效，不能由检查自身 required=false 绕过 |
| task.approval | 需要批准时为 `{status: approved, evidence: 项目内文件路径}`；证据引用用户原话/时间/范围，不能伪造或仅自行写 approved |
| baseline | status 为 complete/approved，evidence 指已存在的基线验收记录；状态与证据存在不能自动证明业务完整性 |
| exclude_paths | 明确排除并在报告列出；不能排除项目根，不得用宽泛排除隐藏业务改动 |

路径限定在项目根内，不允许符号链接/目录连接旁路。source_paths、排除路径和文档路径可为项目内绝对路径，匹配 Git 时规范化为项目相对路径。Markdown 的普通项目内相对链接可跨目录；模板中的外部链接不代表代码依赖。未登记的源路径必须补模块归属，不能为了通过而添加全项目排除。

`task.documentation_impact` 可声明变更触发器与必须同步的文档：`{ "kind": { "when_paths": ["backend/migrations"], "document_ids": ["DB", "FLOW"] } }`。在 change/handoff/commit/committed 中，只要本次变更路径落入 `when_paths`，列出的每份文档必须也出现在本次 diff 中；否则范围检查失败。commit/committed 还要求每个受影响的模块源路径命中至少一条规则，漏声明不能通过。只有实现细节变化时，可声明 `implementation-only` 规则，将对应源路径映射到影响分析文档，并在该文档中写明不更新模块/数据库文档的依据；该记录需与代码同一提交。常见类别包括模块/调用链（module map、business flow、contract）和数据库（database dictionary、business flow）。这是声明式门槛，仍不能自动发现未登记的动态依赖或判断语义是否真实。

## 源清单与文档映射

源清单参见 [示例](../assets/templates/inventory.example.json)。包含 `kind`、`provenance` 和 `items`：

- kind：清单种类，例如 database、contract。
- provenance.type/scope/complete/evidence：提取方法、明确范围、布尔完整性与证据；manual 永远只能报告已声明范围 partial，不能自行声明完整。
- provenance.source_files：`{path, sha256}` 列表，核对来源新鲜度；来源路径须在项目根内。
- items：`{id, fields:[字段名]}` 列表。数据库 id 表示表/视图，接口可用稳定的 method+path 标识；禁止重复条目和字段。

[文档映射示例](../assets/templates/inventory-doc-mapping.example.json) 包含同一种 kind 和 `items:[{id,document,fields}]`。document 是实际 Markdown 路径。源与映射的对象、字段双向核对；映射引用存在不证明字段含义正确，逐字段语义在数据字典人工审查。

内置适配器包括 `sqlite-metadata`、`mysql-metadata`、`postgresql-metadata` 和 `redis-metadata`。SQLite 从受控文件快照只读提取；MySQL/PostgreSQL 只读 `information_schema`；Redis 只读 `INFO keyspace`，不执行 `SCAN`，不读取 key 或 value。远程适配器需要显式调用、可选驱动和环境变量连接 URL，输出带 `source_ref`、`captured_at`、`query_sha256`、`snapshot_sha256` 的 JSON 快照；普通 baseline 不会自动连接数据库。检查器离线核对远程快照的摘要与结构，缺少驱动/凭据或连接失败报告 unsupported，不把未知适配器视为通过。

## 结果的能力限制

检查器核对文件/本地引用、编号、已声明模块图、任务依赖和变更路径、对象字段清单及执行结果。它不能证明所有动态调用已被发现、文档语义正确、认真阅读过资料、达到真实概率 95%、架构合理或整个产品完成。只有声明图的循环得到检查，不是所有语言 import 图。

执行证据包含退出码、耗时、命令与输出摘要；为避免凭据泄露不展示原始参数/输出。常见测试 skip 汇总标记会成为 partial，但没有匹配标记不证明任何框架都没有跳过；人工仍需核对实际测试行为。历史报告不是本次执行证据。必需检查未执行、部分支持或失败都不得标为完成。

SQLite 提取使用只读 immutable 快照和 table_xinfo，覆盖 main schema 的用户表、视图及隐藏/生成字段，附字段类型等详情；不读业务行、不写数据库。活跃 WAL、外部附加库和快照范围外状态不支持；使用项目自身受控的 checkpointed 测试快照，不能自动清空或修改真实库来满足检查。输出只能创建新文件。complete 仅指这个元数据范围，不含字段业务含义、触发器、索引约束、迁移与全系统读写关系。
远程适配器同样只证明声明的元数据快照，没有证明实时数据库状态；快照不得包含连接密码、业务行、Redis key 或 value。
