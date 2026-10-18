"""Observed imports -> validated evidence graph -> optional Mermaid/text views.

Graph schema/validation/escaping/view separation adapted from GitDiagram
310e2e69, MIT Ahmed Khaleel (2024). Links/evidence are local/source-versioned;
this graph deliberately does not claim runtime calls or business verification.
"""

import hashlib
import re
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile


def validate_graph(graph, sources):
    ids = set()
    issues = []
    for node in graph["nodes"]:
        if node["id"] in ids:
            issues.append("duplicate_node_id")
        ids.add(node["id"])
        if node["path"] not in sources:
            issues.append("unknown_node_source")
    paths = {n["id"]: n["path"] for n in graph["nodes"]}
    for edge in graph["edges"]:
        if edge["from"] not in ids or edge["to"] not in ids:
            issues.append("unknown_edge_endpoint")
            continue
        evidence = edge["evidence"]
        original = sources.get(evidence["path"])
        if original is None or evidence["sha256"] != original["sha256"]:
            issues.append("evidence_source_mismatch")
            continue
        if edge["relation"] not in {
            "import",
            "reexport",
            "import_equals",
            "import_type",
            "dynamic_import_literal",
            "require_literal_syntax",
            "rust_use",
            "rust_mod",
        }:
            issues.append("unsupported_semantic_claim")
        if evidence["path"] != paths[edge["from"]]:
            issues.append("evidence_direction_mismatch")
        if paths[edge["to"]] != edge.get("target_path"):
            issues.append("evidence_target_mismatch")
        observed = original.get("observed_references", [])
        if not any(
            r["to"] == edge["target_path"]
            and r["kind"] == edge["relation"]
            and r["type_only"] == edge["type_only"]
            and r["evidence"]["line"] == evidence["line"]
            and r["specifier"] == evidence["specifier"]
            for r in observed
        ):
            issues.append("reference_record_mismatch")
        lines = original["text"].splitlines()
        if not (1 <= evidence["line"] <= evidence["end_line"] <= len(lines)):
            issues.append("evidence_line_range")
            continue
        fragment = "\n".join(lines[evidence["line"] - 1 : evidence["end_line"]])
        if edge["relation"].startswith("rust_"):
            statement = evidence.get("statement", "").replace("\r\n", "\n").replace("\r", "\n")
            if statement not in fragment:
                issues.append("evidence_statement_missing")
        elif evidence["specifier"] not in fragment:
            issues.append("evidence_specifier_missing")
    return {"valid": not issues, "issues": issues}


def escape(text):
    # Same entity strategy as GitDiagram: escape # before Mermaid entity codes.
    replacements = {
        "&": "&amp;",
        "#": "&#35;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "`": "&#96;",
        "\\": "&#92;",
        "|": "&#124;",
        "[": "&#91;",
        "]": "&#93;",
        "{": "&#123;",
        "}": "&#125;",
        "(": "&#40;",
        ")": "&#41;",
    }
    return "".join(replacements.get(c, " " if ord(c) < 32 else c) for c in text)


def compile_mermaid(graph):
    lines = [
        "flowchart TD",
        "%% Observed source-module references; not a runtime call graph",
    ]
    for node in graph["nodes"]:
        lines.append(f'{node["id"]}["{escape(node["label"])}"]')
    seen = set()
    for edge in graph["edges"]:
        group = (
            edge["from"],
            edge["to"],
            edge["type_only"],
            edge["relation"],
            tuple(edge.get("conditions", [])),
        )
        if group in seen:
            continue
        seen.add(group)
        conditional = bool(edge.get("conditions"))
        connector = "-.->" if edge["type_only"] or conditional else "-->"
        label = (
            "type import"
            if edge["type_only"]
            else (
                "conditional " + edge["relation"] if conditional else edge["relation"]
            )
        )
        lines.append(f'{edge["from"]} {connector}|"{label}"| {edge["to"]}')
    return "\n".join(lines) + "\n"


def graph_from_references(analysis, sources):
    refs = [r for r in analysis["references"] if r["status"] == "resolved"]
    names = sorted({x for r in refs for x in [r["from"], r["to"]]})
    ids = {p: "n" + hashlib.sha256(p.encode()).hexdigest()[:16] for p in names}
    graph = {
        "kind": "observed_static_module_references",
        "nodes": [{"id": ids[p], "path": p, "label": p} for p in names],
        "edges": [
            {
                "from": ids[r["from"]],
                "to": ids[r["to"]],
                "target_path": r["to"],
                "relation": r["kind"],
                "type_only": r["type_only"],
                "status": "source_reference_observed; semantics_unreviewed",
                "conditions": r.get("conditions", []),
                "evidence": {**r["evidence"], "specifier": r["specifier"]},
            }
            for r in refs
        ],
    }
    # Existence of a referenced but unselected file comes from inventory. Its
    # content is unknown; validation only needs the caller's complete text.
    return graph


def relation_markdown(graph, root):
    lines = [
        "# Source reference index",
        "",
        "These are source module references, not confirmed runtime calls or business relationships. Type-only edges are marked.",
        "",
        "| From | To | Kind | Source |",
        "| --- | --- | --- | --- |",
    ]
    paths = {n["id"]: n["path"] for n in graph["nodes"]}
    for edge in graph["edges"]:
        ev = edge["evidence"]
        p = Path(root) / ev["path"]
        link = f"[{ev['path']}:{ev['line']}]({p.as_posix()}:{ev['line']})"
        kind = "type " + edge["relation"] if edge["type_only"] else edge["relation"]
        lines.append(
            f"| {paths[edge['from']]} | {paths[edge['to']]} | {kind} | {link} |"
        )
    return "\n".join(lines) + "\n"


def package_graph(graph, inventory_paths):
    """Aggregate observed module references by actual package manifest scope."""
    packages = sorted(
        (
            p.rsplit("/", 1)[0]
            for p in inventory_paths
            if (
                "/" in p
                and (
                    p.endswith("/Cargo.toml")
                    or (
                        p.startswith("packages/")
                        and p.count("/") == 2
                        and p.endswith("/package.json")
                    )
                )
            )
        ),
        key=len,
        reverse=True,
    )

    def owner(p):
        return next(
            (package for package in packages if p.startswith(package + "/")), None
        )

    paths = {n["id"]: n["path"] for n in graph["nodes"]}
    buckets = {}
    for edge in graph["edges"]:
        source, target = owner(paths[edge["from"]]), owner(paths[edge["to"]])
        if not source or not target or source == target:
            continue
        identity = (source, target, edge["type_only"])
        buckets.setdefault(identity, []).append(edge["evidence"])
    names = sorted({p for identity in buckets for p in identity[:2]})
    ids = {p: "p" + hashlib.sha256(p.encode()).hexdigest()[:16] for p in names}
    return {
        "kind": "aggregated_observed_package_imports",
        "nodes": [
            {
                "id": ids[p],
                "path": p
                + (
                    "/Cargo.toml"
                    if p + "/Cargo.toml" in inventory_paths
                    else "/package.json"
                ),
                "label": p,
            }
            for p in names
        ],
        "edges": [
            {
                "from": ids[source],
                "to": ids[target],
                "relation": "import",
                "type_only": only,
                "status": "aggregated_source_references; semantics_unreviewed",
                "reference_count": len(evidence),
                "evidence_samples": evidence[:3],
            }
            for (source, target, only), evidence in sorted(buckets.items())
        ],
    }


def dependency_diagnostics(analysis):
    scripts = Path(__file__).resolve().parent
    npm = ["npm", "ci", "--ignore-scripts", "--prefix", str(scripts / "context-runtime")]
    guidance = {
        "rust_parser_unavailable": (
            "Rust references were not analyzed. Use Python 3.11+ and install the pinned parsers in the environment running collection/tests.",
            [[sys.executable, "-m", "pip", "install", "-r", str(scripts / "reference-requirements.txt")]],
        ),
        "node_runtime_missing": (
            "JavaScript/TypeScript references were not analyzed. Install Node.js, then prepare this tool's TypeScript runtime.",
            [npm],
        ),
        "js_parser_unavailable": (
            "JavaScript/TypeScript references were not analyzed. Prepare this tool's pinned TypeScript runtime.",
            [npm],
        ),
        "js_analysis_failed": (
            "JavaScript/TypeScript analysis failed during execution. Review the analyzer/runtime failure before using its reference coverage.",
            [],
        ),
    }
    groups = {}
    for item in analysis["unsupported"]:
        if item["status"] in guidance:
            groups.setdefault(item["status"], []).append(item["path"])
    return [
        {"status": reason, "files": sorted(set(paths)),
         "message": guidance[reason][0], "setup_commands": guidance[reason][1]}
        for reason, paths in sorted(groups.items())
    ]


def diagnostic_text(diagnostics):
    lines = []
    for item in diagnostics:
        lines.append(f"{item['status']} ({len(item['files'])} files): {item['message']}")
        for command in item["setup_commands"]:
            if os.name == "nt":
                hint = "& " + " ".join("'" + arg.replace("'", "''") + "'" for arg in command)
            else:
                hint = shlex.join(command)
            lines.append("Setup: " + hint)
    return "\n".join(lines)


def analyze_result(result):
    entries = result["inventory"]["entries"]
    request = {
        "root": result["inventory"]["root"],
        "files": [
            e["path"]
            for e in entries
            if e["kind"] == "file" and e["scan_status"] == "available"
        ],
        "directories": [
            e["path"]
            for e in entries
            if e["kind"] == "directory" and e["scan_status"] == "available"
        ],
        "sources": [
            {"path": f["path"], "text": f["text"], "sha256": f["source_sha256"]}
            for f in result["files"]
        ],
    }
    js_sources = [
        s
        for s in request["sources"]
        if re.search(r"\.(?:[cm]?[jt]sx?)$", s["path"], re.I)
    ]
    rust_sources = [s for s in request["sources"] if s["path"].endswith(".rs")]
    analysis = {
        "references": [],
        "unknown": [],
        "unsupported": [],
        "files": [],
        "configuration": [],
    }
    if js_sources:
        node = shutil.which("node")
        if not node:
            analysis["unsupported"].extend(
                {"path": s["path"], "status": "node_runtime_missing"}
                for s in js_sources
            )
        elif not (Path(__file__).with_name("context-runtime") / "node_modules/typescript/lib/typescript.js").is_file():
            analysis["unsupported"].extend(
                {"path": s["path"], "status": "js_parser_unavailable"}
                for s in js_sources
            )
        else:
            with tempfile.TemporaryDirectory(prefix="references-") as temporary:
                inp = Path(temporary) / "request.json"
                inp.write_text(
                    json.dumps({**request, "sources": js_sources}, ensure_ascii=False),
                    encoding="utf-8",
                )
                proc = subprocess.run(
                    [
                        node,
                        str(Path(__file__).with_name("analyze_references.mjs")),
                        str(inp),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=90,
                )
            try:
                js = json.loads(proc.stdout)
            except json.JSONDecodeError:
                js = {"status": "error"}
            if proc.returncode or not isinstance(js, dict) or js.get("status") == "error":
                analysis["unsupported"].extend(
                    {"path": s["path"], "status": "js_analysis_failed"}
                    for s in js_sources
                )
            else:
                for field in analysis:
                    analysis[field].extend(js.get(field, []))
    if rust_sources:
        from rust_references import analyze_rust

        rust = analyze_rust({**request, "sources": rust_sources})
        for field in analysis:
            analysis[field].extend(rust.get(field, []))
    supported = {s["path"] for s in js_sources + rust_sources}
    analysis["unsupported"].extend(
        {"path": s["path"], "status": "language_not_supported"}
        for s in request["sources"]
        if s["path"] not in supported
    )
    refs = analysis["references"]
    analysis["summary"] = {
        "source_files": len(analysis["files"]),
        "references": len(refs),
        "resolved": sum(r["status"] == "resolved" for r in refs),
        "type_only": sum(r["status"] == "resolved" and r["type_only"] for r in refs),
        "unresolved": sum(r["status"] not in ["resolved", "builtin"] for r in refs),
        "unknown": len(analysis["unknown"]),
        "unsupported_files": len(analysis["unsupported"]),
    }
    analysis["scope"] = (
        "Syntax module references for actually read sources; not calls, cfg execution or business verification"
    )
    return analysis


def build_relation_outputs(result, output, views="summary", analysis=None):
    if views not in ["summary", "table", "diagram", "all"]:
        raise ValueError("unknown_relation_view")
    output = Path(output)
    entries = result["inventory"]["entries"]
    request = {
        "root": result["inventory"]["root"],
        "files": [
            e["path"]
            for e in entries
            if e["kind"] == "file" and e["scan_status"] == "available"
        ],
    }
    analysis = analysis if analysis is not None else analyze_result(result)
    sources = {
        e["path"]: {"sha256": e.get("sha256"), "text": ""}
        for e in entries
        if e["kind"] == "file" and e["scan_status"] == "available"
    }
    sources.update(
        {
            f["path"]: {"sha256": f["source_sha256"], "text": f["text"]}
            for f in result["files"]
        }
    )
    for source in sources.values():
        source["observed_references"] = []
    for ref in analysis["references"]:
        if ref["status"] == "resolved":
            sources[ref["from"]]["observed_references"].append(ref)
    graph = graph_from_references(analysis, sources)
    validation = validate_graph(graph, sources)
    if not validation["valid"]:
        raise ValueError("graph evidence invalid: " + str(validation["issues"]))
    (output / "references.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if views in ["table", "all"]:
        (output / "relations.md").write_text(
            relation_markdown(graph, request["root"]), encoding="utf-8"
        )
    diagnostics = dependency_diagnostics(analysis)
    summary_text = f"Observed references: {analysis['summary']['resolved']}; unresolved/external: {analysis['summary']['unresolved']}; unknown: {analysis['summary']['unknown']}; unsupported files: {analysis['summary']['unsupported_files']}. Semantics unreviewed.\n"
    if analysis["unsupported"]:
        summary_text += "Selected source coverage is incomplete; see unsupported records in references.json and relations-status.json.\n"
    if diagnostics:
        summary_text += diagnostic_text(diagnostics) + "\n"
    (output / "relations-summary.txt").write_text(
        summary_text,
        encoding="utf-8",
    )
    packages = package_graph(graph, request["files"])
    (output / "packages.json").write_text(
        json.dumps(packages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if views in ["diagram", "all"] and packages["nodes"]:
        (output / "packages.mmd").write_text(
            compile_mermaid(packages), encoding="utf-8"
        )
    # Large inventories keep full JSON/table; diagram is a bounded optional view.
    if (
        views in ["diagram", "all"]
        and len(graph["nodes"]) <= 120
        and len(graph["edges"]) <= 300
    ):
        (output / "references.mmd").write_text(compile_mermaid(graph), encoding="utf-8")
        diagram_status = "written"
    else:
        diagram_status = (
            "not_requested"
            if views not in ["diagram", "all"]
            else "view_limit; full graph data retained"
        )
    status = {
        "status": "complete_for_read_supported_files"
        if analysis["files"]
        else "unsupported",
        "summary": analysis["summary"],
        "unsupported": analysis["unsupported"],
        "diagnostics": diagnostics,
        "validation": validation,
        "diagram": diagram_status,
        "limits": "Unselected/unsupported/unresolved sources remain unknown; not semantic completeness",
    }
    (output / "relations-status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return status
