# Source helper combination benchmark

2026-10-18. Four combinations × two read-only corpora × three fixed task scenarios = 24 actual helper executions. All selected capabilities stay available; this compares when/order/scope/views, not removing functions. [Authorizations and exact scope](source-context-task.md).

| Task | P1 global first | P2 task + all local views | P3 reference-led expansion | P4 scenario + selected view |
| --- | --- | --- | --- | --- |
| pi/small | 8.16s / 344,686 | 1.41s / 2,509 | 1.77s / 2,509 | 1.09s / 2,449 |
| pi/cross | 8.26s / 348,137 | 1.49s / 6,975 | 1.96s / 38,155 | 1.48s / 6,479 |
| pi/review | 8.34s / 358,896 | 2.17s / 17,534 | 3.41s / 21,223 | 2.82s / 17,025 |
| codex/small | 35.83s / 3,184,051 | 4.18s / 1,277 | 4.54s / 1,277 | 3.76s / 1,217 |
| codex/cross | 35.15s / 3,223,939 | 9.10s / 49,238 | 17.71s / 433,096 | 9.83s / 46,791 |
| codex/review | 87.04s / 3,268,963 | 9.82s / 123,721 | 19.18s / 592,192 | 9.83s / 86,129 |

Each cell is helper seconds / offline material tokens. Same target content/hash checks pass. Cross/review source-scoped reference sets agree among combinations (Pi10/10; Codex91/609 records respectively). Single executions/ordering do not establish reliable speed rankings; P4 does not beat P2 on every time measurement.

P4 is the selected default: inventory/direct search → full task source → references when relationships need investigation → evidence checks → concise text or appropriate table/diagram. P3 is retained for targeted expansion when actual missing context is identified. P1 is not a normal default; it does not excuse skipping global baseline discovery on takeover. P2 remains useful when the user explicitly needs all local views.

Across these scenarios, P2 material=201,254, P4=160,090 (20.45% less); content was kept whole. This is different output selection, not compression/quality improvement. It excludes original skill/history and is not API billing. More detailed diagnostics remain in local experimental evidence, not published target-source dumps.

Read-only fingerprints: Pi1941 files/24880527 bytes; Codex6739 files/70764425 bytes; all unchanged. No source project tests, code changes, dependency installation or model calls performed. Static reference analysis has declared language/config/macro/cfg limits and cannot prove runtime architecture or business meaning.

This comparison is a constrained local result, not proof of the universal best workflow or model behavior. All seven helper functions remain available under explicit use rules, with original engineering stages/approvals/gates unchanged.

A later regression found that display deduplication merged a conditional Rust edge with an unconditional edge sharing endpoints. Full evidence JSON already retained both. The compiler now keys by relation and conditions; all saved optional graph views were rerendered/recounted. Corrected view renders were under1ms each, while the main helper timings above remain the original run values. Focused Rust tests and the final157-test suite cover the correction.
