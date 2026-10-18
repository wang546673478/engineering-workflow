# Local source-context pilot

Use this optional helper inside the existing discovery/impact/recovery work when inventory/packing/references help. It changes no workflow stage, approval, required check or baseline completion rule. It neither runs project code nor calls models. The tool contains no token estimator, Notebook conversion or incremental cache.

## 什么时候启用引用分析

“按需”由Agent根据任务判断，在已有调查/影响记录中简短说明实际范围；不等待用户点名，也不新增一次审批。先用项目现有资料和搜索定位范围，再决定是否运行当前支持的JS/TS或Rust引用解析。

| 场景 | 引用分析的选择与范围 |
| --- | --- |
| 首次接管陌生项目，需要查清入口和模块引用 | 启用；先盘点全貌，再围绕入口/核心模块读取和扩展。工具结果不能代替完整基线调查 |
| 修改共享类型、公共模块、包入口/导出、路径别名，或调整跨模块连接 | 启用相关范围，核对引用方与被引用方；即使调用方文件未改，也要按影响继续查证 |
| 问题横跨多个文件/包，现有搜索不能确定连接，或文档与源码引用不一致 | 启用有争议的链路，结合源码和测试查证；不要因一个引用线索直接确认业务含义 |
| 用户明确要看模块依赖或要求关系图 | 启用适用范围；已有当前版本、足够的关系数据时可直接复用，但先核对来源新鲜度 |
| 单文件小修、定位清楚且不涉及公共接口/模块连接；纯文案、格式或进度记录 | 通常不运行引用分析，直接沿现有搜索/读取/影响分析处理；发现跨文件疑点再扩大 |

新会话、每次改文件或每次保存本身都不触发全仓解析。引用结果仅覆盖本次实际读取的支持语言文件；定位到一个目标文件不表示读过其正文。若要查“谁引用了它”，须搜索/读取可能的引用方并扩大范围，不能用只读目标文件的结果声称没有调用方。跨语言、动态注册、HTTP/事件和无法解析项继续按原流程查证，保持未知标记。

## 什么时候展示关系图、文字或表格

**计算引用与向模型/用户展开视图是两个决定。**默认只报告和当前任务相关的简短结论、证据位置和未决项；完整数据保存在工件中，不把所有清单/图/表一次性输入模型。

| 输出形式 | 适合什么时候用 | 默认控制 |
| --- | --- | --- |
| 简短文字 | 解释一两条关系、汇报影响或调查结论 | 优先使用；说明源码出处和未核验点即可 |
| 关系表 | 逐项核对“谁引用谁”、比较类型/普通引用、审阅接口或跨包改动、追踪来源 | 展示受影响行；完整表保留文件，不每轮重贴 |
| 局部关系图 | 多条关系用文字已难看清，需要梳理分支/层级/链路，或用户明确要图 | 只画当前模块/任务范围；小关系不必专门画图 |
| 全局包/模块概览图 | 首次接管、整体模块边界调整或整体架构审阅 | 以分组/包概览为主，保留详细数据和范围限制；不强画全部文件节点 |

同一组关系通常选择一种最合适的展示方式；用户要求或审阅需要时再组合。图表由同一份来源版本明确的数据派生，已生成的当前结果可复用，不每次对话重新分析或绘制。出处、未知状态和遗漏清单始终保留；少展示不等于少调查。

`--relations`保存完整引用/图JSON和简短文字。`--views summary`为默认；需要逐项核对时选`table`，需要图时选`diagram`，明确需要全部产物才选`all`。机器证据保存与模型阅读/用户展示分开。场景和范围由Agent判断，程序不自动推断任务意图。

## 推荐组合与顺序

默认采用双项目实测的分场景组合：**盘点/直接搜索定位 → 当前任务所需完整源码 → 有依赖疑点时做引用分析 → 对出处/未知作核验 → 仅展示当前需要的视图**。对首次接管仍须完成原流程的全局基线调查；工具的任务选取不缩减它的范围。

- 小修：连接已清楚时跳过引用分析，直接读取/验证；不是因为文件少就免除影响分析。
- 跨模块：读取已定位入口和相关配置/测试后分析引用，发现必要但未读的来源/引用方再扩展。不要无条件沿所有依赖递归扩大阅读包。要查反向引用，搜索/读取可能调用方，不从单个文件得出“无人引用”。
- 审阅：复用本次当前来源的证据，先简短文字；逐项对比用表，复杂链路用局部图，整体边界用包/模块概览。用户明确要求多种形式时组合。
- 一次执行内可复用同一份扫描结果，前提是根、过滤和扫描政策相同；不是跨运行增量缓存。源码/政策变化重新核对，不以过期结果替代调查。

实测选择限于两份语料与已定义场景；它降低不必要的全量处理/重复输出，不声称所有任务都更快或模型回答质量一定提升。

```text
python scripts/collect_code_context.py --root E:/pi-main --output <new-directory-outside-source>
python scripts/collect_code_context.py --root E:/pi-main --include packages/agent/src/agent-loop.ts --relations --output <another-new-directory>
```

No includes means inventory/tree only. Repeated --include accepts the existing segment-aware glob syntax; quote a whole filename with spaces. --all-text explicitly chooses all files within budgets. Default packs preserve selected full text and show one path/start-end line header; --line-numbers adds per-line labels only when useful. SHA256 and exact counts stay in inventory.json. The tool reads with explicit file/total/count/depth/entry limits, records skipped/binary/error/not-selected, rejects links/junctions and outputs inside source, and respects ordered native Git ignores. Lockfiles, project rules, configs, tests and migrations stay discoverable. Known sensitive filename exclusion is not a comprehensive secret scanner.

Output: inventory.json, tree.txt, reading-pack.txt. Optional relations always retains references.json, graph.json and a compact relations-summary.txt. --views table/diagram/all selects additional relations.md, bounded references.mmd and package overview; no need to read all views. Status/unknown/unsupported conditions remain explicit. A large graph keeps the full data/table and omits a too-large diagram with view_limit. No diagram or zero omitted files proves semantic coverage.

JS/TS relations require Node and scripts/context-runtime (TypeScript6.0.3, exact package-lock). Rust relations require Python3.11+ with the optional pinned tree-sitter dependencies. In a task-local environment:

```text
npm ci --ignore-scripts --prefix <skill>/scripts/context-runtime
python -m venv <task-work>/reference-env
<task-work>/reference-env/Scripts/python.exe -m pip install -r <skill>/scripts/reference-requirements.txt
```

On POSIX use reference-env/bin/python. Install only the parser environment, never dependencies in the analyzed repository. Use that environment's Python to run collection when Rust analysis is wanted. The core inventory/pack remains usable if optional runtimes/parsers are unavailable; missing parser scope is explicitly unsupported, not a successful empty reference set. Run a script-disabled install in that runtime directory only when dependencies are absent; never install target project dependencies or change its configs. The parser reads project tsconfig and explicit workspace entry metadata from the observed inventory, and never executes target source. Static import/reexport, type-only, literal dynamic and require syntax are distinct. Variable dynamic, unresolved or unsupported-language references remain unknown. A require token can be shadowed; it stays syntax evidence, never proof of loader execution. Cross-file calls, HTTP/events and business flows still require agent review.

Relations cite caller path, line/end-line, original hash and literal specifier; direction derives from the syntax occurrence. Validation rejects unsupported business claims, unknown endpoints, duplicate IDs and evidence inconsistent with the extraction record. Source positions and parser/config versions are evidence, not user approval. Evidence statement comparison tolerates LF/CRLF line endings while hashes still bind original bytes. Only source-reference syntax is automatically represented; type-only JS/TS imports and Rust cfg/attribute-conditioned edges are dashed and labelled. Rust resolves module-file prefixes using mod declarations, #[path] and explicit Cargo/workspace dependency paths; it does not evaluate cfg/macros, individual symbols, features or Rust name resolution. A module endpoint is not proof an individual item is defined there. Graph links/relations tables use local source locations; inventory binds file hashes even without Git.

## Selected upstream/local sources

- Gitingest main4e259a02: README-first ordering, directory-tree framing and content organization; local adaptation uses existing checker root/link/glob guards and native ordered Git ignore instead of upstream unordered patterns. MIT notice assets/licenses/gitingest-MIT.txt.
- GitDiagram main310e2e69: reference-index/graph/evidence/view separation and deterministic Mermaid entity escaping; local adaptation uses TypeScript syntax/config resolution and exact evidence records in place of regex guessing and permissive citation fill. MIT notice assets/licenses/gitdiagram-MIT.txt.
- TypeScript compiler API: Apache-2.0, one optional exact dependency for JS/TS resolution. No Next/React/cloud/model SDK needed. Language coverage deliberately limited and explicitly reported.

Actual scope, choices, requirements and validation are in [the current Task](../planning/source-context-task.md).

Rust parser versions are pinned in scripts/reference-requirements.txt; tree-sitter and tree-sitter-rust use MIT licenses. The analysis reads metadata only and never executes Cargo or target code. Unsupported languages, generated macro dependencies, runtime registrations, HTTP/events and unresolved module targets still require normal source/test investigation.

## Parser availability and regression setup

`relations-status.json` and the collector CLI's `relations` object retain the existing status/summary and additionally expose per-file `unsupported` records plus grouped `diagnostics` with messages and setup argv. `relations-summary.txt` states incomplete selected-source coverage and renders actionable setup hints. Rust, Node and TypeScript absence remain distinct; a failure executing an installed JS analyzer is `js_analysis_failed`, without assuming an installation fixes it. Mixed-language results retain valid edges and identify the unsupported part. A parsed file with zero references has a parser file record and no missing-parser diagnostic; empty-graph validation alone does not establish analysis coverage.

These dependencies remain optional for inventory/packing. The repository's full regression suite requires both pinned parser environments: run the setup commands above, then `python -m unittest discover -s scripts/tests -q` with that Python environment active. Required parser fixture setup fails early with preparation guidance when unavailable; it does not skip capability tests. The generic checker continues treating detected required-test skips as partial. No checker policy or collection exit-code change is introduced.
