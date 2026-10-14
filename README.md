# Engineering Workflow

一个面向复杂软件工程任务的 Codex skill。它帮助 Agent 在修改代码前后维护需求、模块关系、接口契约、业务流程、数据库字典和验证证据。

## 适用场景

- 接管缺少文档的陌生项目
- 跨前端、后端、数据库或后台任务的功能变更
- 影响范围不明确的缺陷定位
- 需要迁移、接口兼容、回滚和恢复记录的改动
- 需要在 Git 提交时确认代码与关联文档同步的项目

## 安装

将仓库克隆到 Codex 的 skills 目录：

```powershell
git clone https://github.com/wang546673478/engineering-workflow.git `
  "$HOME/.codex/skills/engineering-workflow"
```

Windows PowerShell 也可以使用完整路径：

```powershell
git clone https://github.com/wang546673478/engineering-workflow.git `
  "C:\Users\<user>\.codex\skills\engineering-workflow"
```

安装后，使用 `$engineering-workflow` 或让 Codex 根据任务自动选择该 skill。

## 工作流内容

Skill 会引导 Agent：

1. 读取项目规则和现有权威文档。
2. 检查当前任务可用的其他 skills，并记录采用或不采用的理由。
3. 分析页面、接口、业务逻辑、数据库、事件和消费者之间的影响链。
4. 在实现后同步模块地图、业务流程、接口契约和数据库文档。
5. 运行项目检查，并记录通过、失败、跳过、未支持和未验证状态。

## 和用户确认

需要用户决定的事情会先用通俗语言说明：发现了什么、为什么要决定、有哪些选项，以及每个选项的影响。技术名词、文件路径和检查结果会作为补充说明，不会直接替代解释。用户看不懂时，Agent 应换一种更简单的说法；用户确认后，Agent 会复述确认范围，并记录在任务或决定记录中。

## Git 提交门禁

检查器位于 `scripts/check_project.py`。

提交前检查当前暂存区：

```text
python scripts/check_project.py \
  --root <project> \
  --manifest engineering-manifest.json \
  --mode commit \
  --task TASK-01 \
  --run-checks
```

CI 检查已经生成的 commit：

```text
python scripts/check_project.py \
  --root <project> \
  --manifest engineering-manifest.json \
  --mode committed \
  --commit-ref <commit-sha> \
  --task TASK-01 \
  --run-checks
```

`commit` 模式确认代码变更和受影响的模块、业务流程、接口或数据库文档进入同一个提交。`committed` 模式用于 CI 或受保护分支复核实际提交树。可直接使用以下模板：

- `assets/templates/pre-commit.engineering`
- `assets/templates/pre-commit.engineering.ps1`
- `assets/templates/ci-committed.engineering`
- `assets/templates/ci-committed.engineering.ps1`

具体文档门禁由项目清单中的 `task.documentation_impact` 声明。检查器不会自动发现所有动态依赖，模块关联和字段语义仍需要人工复核。

## 数据库元数据适配器

入口：`scripts/extract_database.py`

支持：

- SQLite：受控文件快照
- MySQL：只读 `INFORMATION_SCHEMA`
- PostgreSQL：只读 `information_schema`
- Redis：只读 `INFO keyspace`

适配器只生成元数据快照，不读取业务行、Redis key/value 或连接凭据。MySQL、PostgreSQL 和 Redis 驱动是可选依赖；缺少驱动、凭据或连接不可用时会报告 `unsupported`。普通基线检查不会自动连接远程数据库。

示例：

```text
python scripts/extract_sqlite.py <checkpointed.sqlite> --output database-inventory.json
python scripts/extract_database.py mysql --url-env ENGINEERING_DATABASE_URL --schema app --output database-inventory.json
python scripts/extract_database.py postgresql --url-env ENGINEERING_DATABASE_URL --schema public --output database-inventory.json
python scripts/extract_database.py redis --url-env ENGINEERING_DATABASE_URL --output database-inventory.json
```

## 目录结构

```text
SKILL.md                         Agent 入口规则
agents/openai.yaml               Codex 界面元数据
assets/templates/                项目清单、文档和 hook 模板
references/                      分阶段工作流说明
scripts/check_project.py         项目清单与提交门禁检查器
scripts/extract_database.py      MySQL、PostgreSQL、Redis 元数据适配器
scripts/extract_sqlite.py        SQLite 元数据提取器
scripts/tests/                   检查器和适配器测试
```

## 验证

```text
python -m unittest discover -s scripts/tests -q
python -m py_compile scripts/check_project.py scripts/extract_database.py scripts/extract_sqlite.py
```

本仓库也维护自己的工程清单。可在仓库根目录运行：

```text
python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --run-checks
```

本仓库自带的 GitHub Actions 示例会在 Linux 和 Windows 上运行测试、编译检查和自身基线检查。GitHub Actions 对使用该 skill 的项目是可选能力：项目可以只用本地 hook，或接入其他 CI 服务；选择 GitHub Actions 的项目再复制模板并启用 workflow。无论是否使用远程 CI，提交前都应运行本地 `commit` 门禁，并在采用的 CI 中复核已生成的提交。

检查规则本身被修改时，自动提交检查会暂停，等待人工审阅。检查器会同时参考修改前后的保护范围，不能靠在本次提交中删除保护名单或更换批准变量来直接放行。获批后才能通过专用参数和单次外部批准信号继续；规则检查失败、历史缺失或工作区与提交内容不一致时，不执行该提交声明的项目命令。

本仓库另提供人工运行的 Actions 入口，要求指定审阅过的完整提交 SHA，并配置受保护的 GitHub environment。具体接入条件见 [检查器说明](references/checker.md)。这些配置不会自动安装到其他项目，也不代表 GitHub 仓库设置已经启用保护。

## 安全边界

- 不把密码、Token 或完整连接串写入计划、清单或快照。
- 不为满足检查自动修改、清空或迁移真实数据库。
- 不把检查器通过当成完整的业务语义审查。
- 项目自身的规则、用户决定和安全约束优先于本 skill 的默认流程。
