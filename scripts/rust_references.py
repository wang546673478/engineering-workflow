"""Optional Rust syntax/module reference adapter; never executes Cargo/builds.

File/module endpoints only: macros, cfg evaluation, item reexports and runtime
calls are not resolved. GitDiagram reference-index design, locally adapted.
"""

from pathlib import Path, PurePosixPath
import hashlib
import posixpath
import re


def analyze_rust(request):
    try:
        import tomllib
        from tree_sitter import Language, Parser
        import tree_sitter_rust
    except ImportError:
        return {
            "references": [],
            "unknown": [],
            "files": [],
            "configuration": [],
            "unsupported": [
                {"path": s["path"], "status": "rust_parser_unavailable"}
                for s in request["sources"]
            ],
        }
    parser = Parser(Language(tree_sitter_rust.language()))
    root = Path(request["root"])
    allowed = set(request["files"])
    audit = {}
    manifests = {}

    def metadata(name):
        if name not in allowed:
            return {}
        if name in manifests:
            return manifests[name]
        try:
            file = root / name
            if file.is_symlink() or file.stat().st_size > 512000:
                return {}
            raw = file.read_bytes()
            data = tomllib.loads(raw.decode("utf-8"))
            audit[name] = {"path": name, "sha256": hashlib.sha256(raw).hexdigest()}
            manifests[name] = data
            return data
        except (OSError, UnicodeError, ValueError):
            audit[name] = {"path": name, "status": "manifest_unreadable"}
            manifests[name] = {}
            return {}

    def manifest_for(source):
        for parent in PurePosixPath(source).parents:
            name = (parent / "Cargo.toml").as_posix()
            if name in allowed:
                return name
        return None

    def workspace_for(name):
        for parent in PurePosixPath(name).parents:
            candidate = (parent / "Cargo.toml").as_posix()
            data = metadata(candidate)
            if data.get("workspace"):
                return candidate, data["workspace"]
        return None, {}

    def local_path(base, relative):
        joined = posixpath.normpath(posixpath.join(base, relative))
        return None if joined.startswith(("../", "/")) or joined == ".." else joined

    def library(manifest):
        data = metadata(manifest)
        folder = posixpath.dirname(manifest)
        entry = data.get("lib", {}).get("path", "src/lib.rs")
        full = local_path(folder, entry)
        return full if full in allowed else None

    def dependencies(name):
        data = metadata(name)
        folder = posixpath.dirname(name)
        workspace_name, workspace = workspace_for(name)
        tables = [
            data.get(k, {})
            for k in ["dependencies", "dev-dependencies", "build-dependencies"]
        ]
        for config in data.get("target", {}).values():
            tables.extend(
                config.get(k, {})
                for k in ["dependencies", "dev-dependencies", "build-dependencies"]
            )
        result = {}
        for table in tables:
            for alias, settings in table.items():
                base = folder
                if isinstance(settings, dict) and settings.get("workspace"):
                    settings = workspace.get("dependencies", {}).get(alias, {})
                    base = (
                        posixpath.dirname(workspace_name) if workspace_name else folder
                    )
                if isinstance(settings, dict) and isinstance(settings.get("path"), str):
                    dep_folder = local_path(base, settings["path"])
                    dep_manifest = (
                        posixpath.join(dep_folder, "Cargo.toml") if dep_folder else None
                    )
                    endpoint = library(dep_manifest) if dep_manifest else None
                    result[alias.replace("-", "_")] = endpoint
        return result

    def module_file(base, parts, fallback=None):
        for length in range(len(parts), 0, -1):
            prefix = posixpath.join(base, *parts[:length])
            choices = [prefix + ".rs", posixpath.join(prefix, "mod.rs")]
            existing = [p for p in choices if p in allowed]
            if len(existing) == 1:
                return existing[0]
            if len(existing) > 1:
                return None
        return fallback

    refs, unknown, files = [], [], []
    for source in request["sources"]:
        manifest = manifest_for(source["path"])
        if not manifest:
            unknown.append(
                {"path": source["path"], "status": "cargo_manifest_not_found"}
            )
            continue
        entry = library(manifest)
        default_root = posixpath.join(posixpath.dirname(manifest), "src")
        crate_folder = posixpath.dirname(entry) if entry else default_root
        # A bin's crate root is independent of the package library.
        if source["path"].endswith("/main.rs"):
            entry = source["path"]
            crate_folder = posixpath.dirname(entry)
        rel = posixpath.relpath(source["path"], crate_folder)
        pieces = rel.split("/")
        scope = (
            pieces[:-1]
            if pieces[-1] in ["lib.rs", "main.rs", "mod.rs"]
            else pieces[:-1] + [PurePosixPath(rel).stem]
        )
        deps = dependencies(manifest)
        data = source["text"].encode("utf-8")
        tree = parser.parse(data)
        files.append(
            {
                "path": source["path"],
                "sha256": source["sha256"],
                "parser": "tree-sitter-rust-0.24.2",
                "config": manifest,
                "parse_errors": ["syntax_error"] if tree.root_node.has_error else [],
            }
        )
        if tree.root_node.has_error:
            unknown.append({"path": source["path"], "status": "parse_error"})
            continue

        def flatten(node, prefix=()):
            if node.type == "scoped_use_list":
                path_node = node.child_by_field_name("path")
                new = (
                    prefix + tuple(path_node.text.decode().split("::"))
                    if path_node
                    else prefix
                )
                list_node = node.child_by_field_name("list")
                return (
                    [
                        p
                        for child in list_node.named_children
                        for p in flatten(child, new)
                    ]
                    if list_node
                    else []
                )
            if node.type == "use_list":
                return [
                    p for child in node.named_children for p in flatten(child, prefix)
                ]
            if node.type == "use_as_clause":
                return flatten(node.named_children[0], prefix)
            text = node.text.decode().strip()
            if text == "self":
                return [prefix]
            parts = tuple(
                p for p in text.split("::") if re.fullmatch(r"(?:r#)?\w+|\*", p)
            )
            return [prefix + parts]

        def record(node, specifier, kind, inline, attributes, forced=None):
            parts = [
                part.removeprefix("r#")
                for part in specifier.split("::")
                if part and part != "*"
            ]
            target = forced
            if kind == "rust_use" and parts:
                anchor, rest = parts[0], parts[1:]
                if anchor == "crate":
                    target = module_file(crate_folder, rest, entry)
                elif anchor in ("self", "super"):
                    current = scope + inline
                    if anchor == "super":
                        current = current[:-1]
                    while rest and rest[0] == "super":
                        current, rest = current[:-1], rest[1:]
                    target = module_file(
                        crate_folder, current + rest, entry if not current else None
                    )
                elif anchor in deps and deps[anchor]:
                    dep_entry = deps[anchor]
                    target = module_file(posixpath.dirname(dep_entry), rest, dep_entry)
                else:
                    target = module_file(crate_folder, parts)
            if target == source["path"]:
                return  # Same-file/inline module relationships have no file edge.
            refs.append(
                {
                    "from": source["path"],
                    "to": target,
                    "specifier": specifier,
                    "kind": kind,
                    "type_only": False,
                    "status": "resolved" if target else "rust_unresolved_or_external",
                    "conditions": attributes,
                    "semantics": "module_reference_observed; cfg/macros/runtime/individual items not resolved",
                    "evidence": {
                        "path": source["path"],
                        "line": node.start_point.row + 1,
                        "end_line": node.end_point.row + 1,
                        "sha256": source["sha256"],
                        "statement": node.text.decode(),
                        "config": manifest,
                        "resolution_basis": "rust_module_prefix_and_cargo_paths",
                    },
                }
            )

        def walk(parent, inline=(), inherited=()):
            attributes = []
            for node in parent.named_children:
                if node.type == "attribute_item":
                    attributes.append(node.text.decode())
                    continue
                current = list(inherited) + attributes
                if node.type == "use_declaration":
                    argument = node.child_by_field_name("argument")
                    for parts in flatten(argument) if argument else []:
                        record(
                            node, "::".join(parts), "rust_use", list(inline), current
                        )
                elif node.type == "mod_item":
                    name = node.child_by_field_name("name").text.decode()
                    body = node.child_by_field_name("body")
                    if body:
                        walk(body, inline + (name,), tuple(current))
                    else:
                        override = next(
                            (
                                re.search(r'path\s*=\s*"([^"]+)"', a).group(1)
                                for a in attributes
                                if re.search(r'path\s*=\s*"([^"]+)"', a)
                            ),
                            None,
                        )
                        base = posixpath.join(crate_folder, *(scope + list(inline)))
                        choices = (
                            [local_path(posixpath.dirname(source["path"]), override)]
                            if override
                            else [
                                posixpath.join(base, name + ".rs"),
                                posixpath.join(base, name, "mod.rs"),
                            ]
                        )
                        existing = [p for p in choices if p in allowed]
                        record(
                            node,
                            name,
                            "rust_mod",
                            list(inline),
                            current,
                            existing[0] if len(existing) == 1 else None,
                        )
                elif node.type not in [
                    "token_tree",
                    "macro_definition",
                    "macro_invocation",
                ]:
                    walk(node, inline, inherited)
                attributes = []

        walk(tree.root_node)
    return {
        "references": refs,
        "unknown": unknown,
        "files": files,
        "configuration": list(audit.values()),
        "unsupported": [],
    }
