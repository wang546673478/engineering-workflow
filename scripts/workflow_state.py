#!/usr/bin/env python3
"""Manifest-backed engineering index, exact snapshots and guarded batch edits.

Project paths use the shared checker boundary, including Win32 8.3 alias containment.

Windows-only path regression methods are registered on Windows to avoid POSIX required TEST skip summaries."""
from __future__ import annotations
import argparse, difflib, hashlib, json, os, re, sqlite3, sys, tempfile
from pathlib import Path
import check_project, task_archive
LIFECYCLE = {"current", "draft", "completed", "superseded", "obsolete", "deferred", "unverified", "unknown/unverified", "conflict"}
LIFECYCLE_METADATA_STATES = LIFECYCLE - {"conflict"}
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*(\r?\n|$)", re.MULTILINE)
SHA = re.compile(r"^[0-9a-f]{64}$")
class WorkflowStateError(ValueError): pass
class UnsupportedHostError(WorkflowStateError): pass
class BatchConflict(WorkflowStateError): pass
def digest(raw): return hashlib.sha256(raw).hexdigest()
def canonical_json(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def source_snapshot_digest(items):
    snapshot=[{"id":row["id"],"fields":sorted(row.get("fields",[]))} for row in sorted(items,key=lambda item:item["id"])]
    return digest(canonical_json(snapshot))
def strict_json(data,source):
    duplicates=[]
    def pairs(items):
        result={}
        for key,value in items:
            if key in result: duplicates.append(key)
            result[key]=value
        return result
    def reject_constant(value): raise ValueError("invalid JSON constant: "+value)
    try:
        value=check_project.parse_json(data,source,object_pairs_hook=pairs,parse_constant=reject_constant)
    except check_project.ConfigError as exc:
        raise WorkflowStateError(str(exc)) from exc
    if duplicates: raise WorkflowStateError("duplicate JSON key in "+str(source)+": "+duplicates[0])
    return value
def resolve_root(raw):
    root=Path(raw).expanduser().absolute()
    if not root.is_dir(): raise UnsupportedHostError("project root unavailable; no retry attempted; host cwd/workspace recovery unsupported")
    try: return check_project.safe_root(str(root))
    except (check_project.ConfigError,OSError) as exc: raise WorkflowStateError("unsafe project root: "+str(exc)) from exc
def resolve_archive_store(raw,root):
    store=Path(raw).expanduser().absolute()
    cursor=Path(store.anchor)
    for part in store.parts[1:]:
        cursor=cursor/part
        if check_project.is_link(cursor): raise WorkflowStateError("archive store path cannot traverse a symlink or junction")
    try: store.relative_to(root)
    except ValueError: pass
    else: raise WorkflowStateError("archive store must be outside project root")
    resolved=store.resolve()
    try: resolved.relative_to(root)
    except ValueError: return resolved
    raise WorkflowStateError("resolved archive store must be outside project root")
def load_project(root,manifest_arg):
    root=resolve_root(str(root)); mp=check_project.safe_path(root,manifest_arg); manifest=strict_json(mp.read_bytes(),mp)
    if not isinstance(manifest,dict) or not isinstance(manifest.get("documents"),list): raise WorkflowStateError("manifest requires documents array")
    docs={"ENGINEERING_MANIFEST":{"id":"ENGINEERING_MANIFEST","path":mp.relative_to(root).as_posix(),"kind":"manifest"}}; paths={mp.relative_to(root).as_posix()}
    document_ids=set()
    for item in manifest["documents"]:
        if not isinstance(item,dict) or not isinstance(item.get("id"),str) or not item["id"] or not isinstance(item.get("path"),str): raise WorkflowStateError("invalid manifest document")
        if item["id"] in docs: raise WorkflowStateError("duplicate document ID: "+item["id"])
        document_ids.add(item["id"])
        path=check_project.safe_path(root,item["path"]); rel=path.relative_to(root).as_posix()
        if rel in paths: raise WorkflowStateError("duplicate document path: "+rel)
        if not path.is_file(): raise WorkflowStateError("missing document path: "+rel)
        docs[item["id"]]=dict(item,path=rel); paths.add(rel)
        if item.get("lifecycle") is not None:
            errors=lifecycle_metadata_errors(item.get("lifecycle"),manifest)
            if errors: raise WorkflowStateError("invalid lifecycle metadata for "+item["id"]+": "+"; ".join(errors))
    if not isinstance(manifest.get("tasks",[]),list): raise WorkflowStateError("manifest tasks must be an array")
    errors=manifest_diagnostics(manifest)
    if errors: raise WorkflowStateError("manifest index inconsistency: "+"; ".join(errors))
    # Documents and tasks have separate namespaces in established manifests;
    # keep both identities and let callers address them by entry type.
    return root,mp,manifest,docs
def lifecycle(item,current=False):
    data=item.get("lifecycle")
    if data is not None:
        if not isinstance(data,dict): return "unknown/unverified",{"evidence_gap":"lifecycle must be an object"}
        status=data.get("status")
        if status not in LIFECYCLE: return "unknown/unverified",{"evidence_gap":"missing or unsupported lifecycle status"}
        needed={"completed":("evidence",),"superseded":("reason","superseded_by","evidence"),"obsolete":("reason","superseded_by","evidence"),"deferred":("module","conclusion","question","impact","depends_on","resumption_condition")}
        missing=[key for key in needed.get(status,()) if not data.get(key)]
        if missing: return "unknown/unverified",{"evidence_gap":"missing lifecycle evidence: "+", ".join(missing)}
        if current and status!="current": return "conflict",{"declared_status":status,"active_pointer":True,"evidence":data}
        return status,data
    if current: return "current",{"source":"active pointer"}
    return "unknown/unverified",{"evidence_gap":"historical state is not explicit; not inferred from age or inactivity"}
def manifest_diagnostics(manifest):
    errors=[]; documents={item.get("id"):item for item in manifest.get("documents",[]) if isinstance(item,dict)}; tasks={}
    for key in ("active_baseline","active_spec","active_plan"):
        value=manifest.get("workflow",{}).get(key) if isinstance(manifest.get("workflow",{}),dict) else None
        if value is not None and value not in documents: errors.append("workflow."+key+" references unknown document: "+str(value))
    for task in manifest.get("tasks",[]) if isinstance(manifest.get("tasks",[]),list) else []:
        if not isinstance(task,dict) or not isinstance(task.get("id"),str): continue
        if task["id"] in tasks: errors.append("duplicate task ID: "+task["id"])
        tasks[task["id"]]=task
    active=manifest.get("workflow",{}).get("active_task") if isinstance(manifest.get("workflow",{}),dict) else None
    if active is not None and active not in tasks: errors.append("workflow.active_task references unknown task: "+str(active))
    if not isinstance(manifest.get("modules",[]),list): errors.append("manifest modules must be an array")
    for item in manifest.get("documents",[]):
        if not isinstance(item,dict) or item.get("lifecycle") is None: continue
        gaps=lifecycle_metadata_errors(item["lifecycle"],manifest)
        errors.extend("document "+str(item.get("id"))+": "+gap for gap in gaps)
    reqs={item.get("id") for item in manifest.get("requirements",[]) if isinstance(item,dict)} if "requirements" in manifest else None
    ats={item.get("id") for item in manifest.get("acceptance",[]) if isinstance(item,dict)} if "acceptance" in manifest else None
    for task in tasks.values():
        if task.get("lifecycle") is not None:
            gaps=lifecycle_metadata_errors(task["lifecycle"],manifest)
            errors.extend("task "+task["id"]+": "+gap for gap in gaps)
        for field,known in (("requirement_ids",reqs),("acceptance_ids",ats)):
            if known is None: continue
            for ident in task.get(field,[]) if isinstance(task.get(field,[]),list) else []:
                if ident not in known: errors.append("task "+task["id"]+" references unknown "+field+": "+str(ident))
        for name,ident in (task.get("artifact_links",{}) or {}).items() if isinstance(task.get("artifact_links",{}),dict) else []:
            if ident not in documents: errors.append("task "+task["id"]+" artifact link "+str(name)+" references unknown document: "+str(ident))
        revisions=task.get("artifact_revisions",{})
        allowed_revision_metadata={"approved_design_baseline","source_baseline","implementation_basis"}
        if revisions and (not isinstance(revisions,dict) or any(name not in (task.get("artifact_links",{}) or {}) and name not in allowed_revision_metadata for name in revisions)):
            errors.append("task "+task["id"]+" artifact revisions do not match artifact links")
    return errors
def lifecycle_metadata_errors(value,manifest):
    if not isinstance(value,dict): return ["lifecycle must be an object"]
    allowed={"status","reason","superseded_by","evidence","module","conclusion","question","impact","depends_on","resumption_condition","source_revision"}
    unknown=set(value)-allowed
    errors=["unsupported lifecycle fields: "+", ".join(sorted(unknown))] if unknown else []
    status=value.get("status")
    if status not in LIFECYCLE_METADATA_STATES: errors.append("lifecycle status is missing or unsupported (conflict is derived, read-only state)")
    if not isinstance(value.get("source_revision",""),str): errors.append("lifecycle source_revision must be text")
    needed={"completed":("evidence",),"superseded":("reason","superseded_by","evidence"),"obsolete":("reason","superseded_by","evidence"),"deferred":("module","conclusion","question","impact","depends_on","resumption_condition")}
    errors.extend("lifecycle requires "+field for field in needed.get(status,()) if not value.get(field))
    docids={item.get("id") for item in manifest.get("documents",[]) if isinstance(item,dict)}
    paths={item.get("path") for item in manifest.get("documents",[]) if isinstance(item,dict)}
    evidence=value.get("evidence")
    if status in ("completed","superseded","obsolete") and (not isinstance(evidence,str) or (evidence not in docids and evidence not in paths)): errors.append("lifecycle evidence must reference a manifest document ID or path")
    replacement=value.get("superseded_by")
    if status in ("superseded","obsolete") and (not isinstance(replacement,str) or replacement not in docids): errors.append("lifecycle superseded_by must reference a manifest document ID")
    modules={item.get("id") for item in manifest.get("modules",[]) if isinstance(item,dict)}
    if status=="deferred" and (not isinstance(value.get("module"),str) or value.get("module") not in modules): errors.append("deferred lifecycle module must reference a manifest module ID")
    dependencies=value.get("depends_on",[])
    if status=="deferred" and not isinstance(dependencies,list): errors.append("deferred lifecycle depends_on must be an array")
    elif status=="deferred" and any(not isinstance(ident,str) or ident not in docids for ident in dependencies): errors.append("deferred lifecycle depends_on must reference manifest document IDs")
    return errors
def lifecycle_pointer_conflicts(manifest):
    documents={item.get("id"):item for item in manifest.get("documents",[]) if isinstance(item,dict)}
    workflow=manifest.get("workflow",{}) if isinstance(manifest.get("workflow",{}),dict) else {}
    conflicts=[]
    for key in ("active_baseline","active_spec","active_plan"):
        ident=workflow.get(key); item=documents.get(ident)
        if item and isinstance(item.get("lifecycle"),dict) and item["lifecycle"].get("status")!="current": conflicts.append(key+" conflicts with lifecycle status for "+ident)
    return conflicts
def build_index(root,manifest_path,manifest):
    rows=[]; documents={x["id"]:x for x in manifest["documents"]}; w=manifest.get("workflow",{}) if isinstance(manifest.get("workflow",{}),dict) else {}
    linked_tasks={ident:[] for ident in documents}
    for task in manifest.get("tasks",[]):
        if not isinstance(task,dict): continue
        for role,ident in (task.get("artifact_links",{}) or {}).items() if isinstance(task.get("artifact_links",{}),dict) else []:
            if ident in linked_tasks: linked_tasks[ident].append({"task_id":task.get("id"),"role":role})
    pointers={"baseline":w.get("active_baseline"),"spec":w.get("active_spec"),"plan":w.get("active_plan"),"task":w.get("active_task")}
    for ident,item in sorted(documents.items()):
        path=check_project.safe_path(root,item["path"]); raw=path.read_bytes(); active=[k for k,v in pointers.items() if v==ident]; state,life=lifecycle(item,bool(active))
        rows.append({"entry_type":"document","id":ident,"path":item["path"],"kind":item.get("kind","unknown"),"owner":item.get("owner"),"lifecycle_status":state,"lifecycle":life,"revision":item.get("revision"),"basis":item.get("basis"),"sha256":digest(raw),"last_change_summary":item.get("last_change_summary"),"active_for":active,"links":item.get("links",[]),"linked_tasks":linked_tasks.get(ident,[])})
    indexed_paths={item["path"] for item in documents.values()}
    planning=root/"planning"
    if planning.is_dir():
        for path in sorted(planning.rglob("*.md")):
            if any(check_project.is_link(parent) for parent in path.parents if parent != root): continue
            rel=path.relative_to(root).as_posix()
            try: check_project.safe_path(root,rel)
            except check_project.ConfigError: continue
            if rel not in indexed_paths:
                rows.append({"entry_type":"unregistered-document","id":"UNREGISTERED:"+rel,"path":rel,"kind":"markdown","lifecycle_status":"unknown/unverified","lifecycle":{"evidence_gap":"planning Markdown is not declared in manifest; no lifecycle status inferred"},"revision":None,"basis":None,"sha256":digest(path.read_bytes()),"last_change_summary":None,"active_for":[],"links":[]})
    tasks=manifest.get("tasks",[])
    if not isinstance(tasks,list): raise WorkflowStateError("manifest tasks must be an array")
    seen=set()
    for task in tasks:
        if not isinstance(task,dict) or not isinstance(task.get("id"),str): raise WorkflowStateError("invalid task entry")
        ident=task["id"]
        if ident in seen: raise WorkflowStateError("duplicate task ID: "+ident)
        seen.add(ident); path=documents.get(task.get("impact_document"),{}).get("path"); raw=check_project.safe_path(root,path).read_bytes() if path else b""; active=w.get("active_task")==ident
        status=task.get("status"); inferred={"complete":"completed","planned":"draft","in_progress":"current"}.get(status)
        if task.get("lifecycle") is not None: life_state,life=lifecycle(task,active)
        elif inferred=="completed" and active: life_state,life="conflict",{"source":"active task pointer conflicts with completed task status"}
        elif inferred=="completed": life_state,life="completed",{"source":"explicit task.status","evidence":task.get("verification_evidence") or task.get("verification_status") or task.get("impact_document"),"validation_status":task.get("verification_status")}
        elif active: life_state,life="current",{"source":"active task pointer","task_status":status}
        elif inferred=="draft": life_state,life="draft",{"source":"explicit task.status"}
        else: life_state,life="unknown/unverified",{"evidence_gap":"task is nonactive and has no explicit lifecycle"}
        rows.append({"entry_type":"task","id":ident,"path":path,"kind":"task","lifecycle_status":life_state,"lifecycle":life,"revision":task.get("artifact_revisions"),"basis":task.get("requirement_ids",[]),"sha256":digest(raw) if path else None,"last_change_summary":task.get("implementation_status"),"active_for":["task"] if active else [],"links":task.get("artifact_links",{}),"task_status":status,"requirement_state":task.get("requirement_state"),"implementation_status":task.get("implementation_status"),"approval_status":task.get("approval",{}).get("status") if isinstance(task.get("approval"),dict) else None,"acceptance_ids":task.get("acceptance_ids",[])})
    return sorted(rows,key=lambda row:(row.get("path") or "",row["entry_type"],row["id"]))
def render_markdown(rows):
    out=["# Engineering document index","","Generated from manifest and task records. This read-only view preserves historical entries.","","| Type | ID | Path | Kind | Lifecycle | Task status / approval | Requirement / implementation | Revision / basis | SHA-256 | Evidence / links |","| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        task_state={"task_status":row.get("task_status"),"approval_status":row.get("approval_status")}
        req_state={"requirement_state":row.get("requirement_state"),"implementation_status":row.get("implementation_status"),"last_change_summary":row.get("last_change_summary")}
        refs={"links":row.get("links"),"lifecycle":row.get("lifecycle"),"linked_tasks":row.get("linked_tasks")}
        vals=[row["entry_type"],row["id"],row.get("path") or "",row.get("kind") or "",row["lifecycle_status"],json.dumps(task_state,ensure_ascii=False,separators=(",",":")),json.dumps(req_state,ensure_ascii=False,separators=(",",":")),json.dumps(row.get("revision") or row.get("basis"),ensure_ascii=False,separators=(",",":")),row.get("sha256") or "",json.dumps(refs,ensure_ascii=False,separators=(",",":"))]
        out.append("| "+" | ".join(str(v).replace("|","\\|").replace("\n"," ") for v in vals)+" |")
    return "\n".join(out)+"\n"
def sections(text):
    matches=[]; fence=None; offset=0
    for line in text.splitlines(True):
        marker=re.match(r"^ {0,3}(`{3,}|~{3,})",line)
        if fence is not None:
            if marker and marker.group(1)[0]==fence[0] and len(marker.group(1))>=fence[1]: fence=None
            offset+=len(line); continue
        if marker:
            fence=(marker.group(1)[0],len(marker.group(1))); offset+=len(line); continue
        match=HEADING.match(text,offset)
        if match: matches.append(match)
        offset+=len(line)
    result={}
    for i,match in enumerate(matches):
        end=next((later.start() for later in matches[i+1:] if len(later.group(1))<=len(match.group(1))),len(text))
        result.setdefault(match.group(2).strip(),[]).append((match,end))
    return result
def snapshot(root,manifest_path,manifest,ids,section_ids=None):
    if not isinstance(ids,list) or not ids or any(not isinstance(ident,str) for ident in ids) or len(ids)!=len(set(ids)): raise WorkflowStateError("document IDs must be unique non-empty strings")
    if section_ids and (any(not isinstance(ident,str) for ident in section_ids) or len(section_ids)!=len(set(section_ids))): raise WorkflowStateError("section IDs must be unique strings")
    docs={x["id"]:x for x in manifest["documents"]}; result=[]
    for ident in ids:
        item={"id":ident,"path":manifest_path.relative_to(root).as_posix(),"kind":"manifest"} if ident=="ENGINEERING_MANIFEST" else docs.get(ident)
        if item is None: raise WorkflowStateError("unknown document ID: "+ident)
        raw=check_project.safe_path(root,item["path"]).read_bytes(); text=raw.decode("utf-8-sig"); selected=[]
        for sid in section_ids or []:
            found=sections(text).get(sid,[])
            if len(found)!=1: raise WorkflowStateError("section must match exactly once: "+sid)
            match,end=found[0]; selected.append({"section_id":sid,"content":text[match.end():end].strip("\r\n")})
        rev={}; workflow=manifest.get("workflow",{}); task=next((t for t in manifest.get("tasks",[]) if t.get("id")==workflow.get("active_task")),None)
        if task:
            for name,docid in task.get("artifact_links",{}).items():
                if docid==ident: rev[name]=task.get("artifact_revisions",{}).get(name)
        result.append({"id":ident,"path":item["path"],"kind":item.get("kind"),"sha256":digest(raw),"semantic_revision":rev or item.get("revision"),"content":None if section_ids else text,"sections":selected})
    workflow=manifest.get("workflow",{}); active_task=next((task for task in manifest.get("tasks",[]) if task.get("id")==workflow.get("active_task")),None)
    deferred=[]
    for item in manifest.get("documents",[])+manifest.get("tasks",[]):
        life=item.get("lifecycle") if isinstance(item,dict) else None
        if isinstance(life,dict) and life.get("status")=="deferred": deferred.append({"id":item.get("id"),**life})
    summary={"active_artifacts":{key:workflow.get("active_"+key) for key in ("baseline","spec","plan")},"task":None}
    if active_task:
        summary["task"]={key:active_task.get(key) for key in ("id","status","requirement_state","implementation_status","requirement_ids","acceptance_ids","artifact_links","artifact_revisions")}
        approval=active_task.get("approval"); summary["task"]["approval_status"]=approval.get("status") if isinstance(approval,dict) else None
    current=[]
    for key in ("baseline","spec","plan"):
        ident=workflow.get("active_"+key); item=docs.get(ident) if ident else None
        if item is None: continue
        raw=check_project.safe_path(root,item["path"]).read_bytes(); text=raw.decode("utf-8-sig"); excerpts=[]
        for title,entries in sections(text).items():
            if re.search(r"待决|未决|开放问题|延后|deferred|open questions",title,re.I):
                match,end=entries[0]; excerpts.append({"section":title,"content":text[match.end():end].strip()[:1200]})
        current.append({"artifact":key,"id":ident,"path":item["path"],"sha256":digest(raw),"summary":text.strip()[:500],"open_sections":excerpts})
    return {"status":"pass","active":workflow.get("active_task"),"summary":summary,"current_artifacts":current,"open_items":deferred,"documents":result}

def query(root, manifest, ids):
    """Read only current fact slices by stable ID; unsupported sources stay explicit."""
    if not isinstance(ids, list) or not ids or any(not isinstance(value, str) or not value for value in ids):
        raise WorkflowStateError("query requires one or more non-empty stable IDs")
    if len(ids) != len(set(ids)):
        raise WorkflowStateError("query IDs must be unique")
    try:
        import extract_sqlite
    except ImportError:
        extract_sqlite = None
    inventories = manifest.get("inventories", [])
    manifest_path = root / "engineering-manifest.json"
    manifest_evidence = {"path": "engineering-manifest.json", "sha256": digest(manifest_path.read_bytes())}
    if not isinstance(inventories, list):
        inventories = []
    database_adapters = []
    source_derived_adapters = []
    inventory_evidence = []
    inventory_problems = []
    for entry in inventories:
        if not isinstance(entry, dict) or entry.get("kind") not in {"database", "contract"}:
            continue
        try:
            inventory_path = check_project.safe_path(root, entry.get("path"))
            inventory = strict_json(inventory_path.read_bytes(), inventory_path)
        except (OSError, WorkflowStateError, check_project.ConfigError):
            continue
        provenance = inventory.get("provenance", {}) if isinstance(inventory, dict) else {}
        inventory_evidence.append({"path": inventory_path.relative_to(root).as_posix(), "sha256": digest(inventory_path.read_bytes())})
        if provenance.get("type") == "source-derived":
            receipt_ref=provenance.get("source_evidence",{})
            try:
                receipt_path=check_project.safe_path(root,receipt_ref.get("path"))
                receipt=strict_json(receipt_path.read_bytes(),receipt_path)
                adapter_path=check_project.safe_path(root,receipt.get("adapter_path"))
                receipt_hash=receipt.get("evidence_sha256")
                adapter_hash=provenance.get("adapter_sha256")
                problems=[]
                if receipt_ref.get("sha256") != digest(receipt_path.read_bytes()): problems.append("inventory receipt hash is stale")
                if not isinstance(receipt_hash,str) or receipt_hash != digest(canonical_json({k:v for k,v in receipt.items() if k!="evidence_sha256"})): problems.append("receipt evidence digest is invalid")
                if not adapter_path.is_file() or digest(adapter_path.read_bytes()) != adapter_hash: problems.append("source adapter hash is stale")
                receipt_sources=receipt.get("source_files",[])
                if not isinstance(receipt_sources,list):
                    problems.append("receipt source_files is not a list")
                else:
                    for source_ref in receipt_sources:
                        try:
                            source_path=check_project.safe_path(root,source_ref.get("path"))
                            if not source_path.is_file() or source_ref.get("sha256") != digest(source_path.read_bytes()):
                                problems.append("source file hash is stale: "+str(source_ref.get("path")))
                        except (AttributeError,check_project.ConfigError,OSError):
                            problems.append("source file reference is invalid: "+str(source_ref))
                if inventory.get("kind") != receipt.get("kind") or provenance.get("adapter") != receipt.get("adapter"): problems.append("inventory and receipt adapter/kind disagree")
                if provenance.get("snapshot_sha256") != receipt.get("snapshot_sha256"): problems.append("inventory and receipt snapshot differ")
                if source_snapshot_digest(inventory.get("items",[])) != receipt.get("snapshot_sha256"): problems.append("inventory item snapshot digest is invalid")
                if source_snapshot_digest(inventory.get("items",[])) != source_snapshot_digest(receipt.get("items",[])): problems.append("inventory item IDs/fields differ from the bound source receipt")
                if provenance.get("adapter")=="gin-routes-v1":
                    if inventory.get("items")!=receipt.get("items"): problems.append("route inventory fields/review differ from the bound source receipt")
                elif provenance.get("adapter")=="gorm-source-v1":
                    receipt_rows={row.get("id"):row for row in receipt.get("items",[]) if isinstance(row,dict)}
                    model_rows={row.get("id"):row for row in receipt.get("models",[]) if isinstance(row,dict)}
                    for row in inventory.get("items",[]):
                        source_row=receipt_rows.get(row.get("id"),{})
                        model_row=model_rows.get(row.get("id"),{})
                        source_mappings={item.get("column"):item.get("go_name") for item in model_row.get("dictionary_mappings",[])}
                        inventory_mappings={item.get("column"):item.get("go_name") for item in row.get("detail",[])}
                        inventory_sources={item.get("source") for item in row.get("detail",[]) if item.get("source")}
                        if row.get("fields")!=source_row.get("fields") or inventory_mappings!=source_mappings or row.get("model")!=model_row.get("model") or (inventory_sources and model_row.get("source") not in inventory_sources):
                            problems.append("database semantic/model mapping differs from bound source receipt: "+str(row.get("id")))
                            break
                source_derived_adapters.append({"inventory_id":entry.get("id"),"kind":entry.get("kind"),"inventory_path":inventory_path.relative_to(root).as_posix(),"inventory_sha256":digest(inventory_path.read_bytes()),"receipt_path":receipt_path.relative_to(root).as_posix(),"receipt_sha256":digest(receipt_path.read_bytes()),"adapter":provenance.get("adapter"),"adapter_version":receipt.get("adapter_version"),"items":inventory.get("items",[]),"evidence":[{"path":receipt_path.relative_to(root).as_posix(),"sha256":digest(receipt_path.read_bytes())}]+[{"path":x.get("path"),"sha256":x.get("sha256")} for x in receipt.get("source_files",[])],"problems":problems})
            except (OSError,WorkflowStateError,check_project.ConfigError,TypeError,KeyError) as exc:
                source_derived_adapters.append({"inventory_id":entry.get("id"),"kind":entry.get("kind"),"status":"unsupported","reason":"source-derived receipt could not be verified: "+str(exc)})
            continue
        if provenance.get("type") != "sqlite-metadata":
            if provenance.get("type") == "manual":
                inventory_problems.append({"inventory_id": entry.get("id"), "path": inventory_path.relative_to(root).as_posix(), "status": "manual_source_not_derived"})
            continue
        sources = provenance.get("source_files", [])
        if not isinstance(sources, list) or len(sources) != 1 or not isinstance(sources[0], dict):
            continue
        try:
            source_path = check_project.safe_path(root, sources[0].get("path"))
        except check_project.ConfigError:
            continue
        database_adapters.append((entry, inventory, source_path))

    result = []
    modules = {item.get("id"): item for item in manifest.get("modules", []) if isinstance(item, dict)}
    for ident in ids:
        if ident.startswith("module:"):
            module_id = ident[len("module:"):]
            module = modules.get(module_id)
            if module is None:
                result.append({"id": ident, "status": "unsupported", "reason": "module ID is not declared", "evidence": []})
                continue
            manifest_path = root / "engineering-manifest.json"
            evidence = [{"path": "engineering-manifest.json", "sha256": digest(manifest_path.read_bytes())}]
            value = {"source_paths": module.get("source_paths", []), "depends_on": module.get("depends_on", [])}
            fingerprint = hashlib.sha256(json.dumps({"module": value, "manifest": evidence}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            result.append({"id": ident, "status": "pass", "adapter": "manifest-module-map", "adapter_version": "1", "value": value, "evidence": evidence, "source_fingerprint": fingerprint, "coverage": {"supported": ["declared module source paths", "declared module dependencies"], "excluded": ["undocumented runtime edges", "dynamic imports not represented in manifest"], "limitations": ["Manifest dependencies are declared relationships, not an extracted runtime call graph; use --relations for bounded source-reference analysis."]}})
            continue
        table_match = re.fullmatch(r"(?:db:(?:main\.)?|table:)([^.]+)", ident)
        field_match = re.fullmatch(r"field:(?:main\.)?([^.]+)\.([^.]+)", ident)
        route_match = re.fullmatch(r"route:(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD):(.+)", ident)
        if not table_match and not field_match and not route_match:
            result.append({"id": ident, "status": "unsupported", "reason": "no adapter for this stable ID/source kind", "evidence": [], "coverage": {"supported": ["declared SQLite metadata inventories"], "excluded": ["routes", "request/response contracts", "permissions", "runtime behavior"], "limitations": ["Unsupported does not mean the object is absent."]}})
            continue
        table = table_match.group(1) if table_match else field_match.group(1) if field_match else None
        candidates = []
        if route_match:
            route_id = route_match.group(1) + " " + route_match.group(2)
            route_adapters=[adapter for adapter in source_derived_adapters if adapter.get("kind")=="contract" and adapter.get("adapter")=="gin-routes-v1"]
            for adapter in route_adapters:
                if adapter.get("kind") != "contract" or adapter.get("adapter") != "gin-routes-v1":
                    continue
                if adapter.get("problems"):
                    candidates.append({"inventory_id": adapter.get("inventory_id"), "status": "stale", "problems": adapter["problems"]})
                    continue
                matches = [row for row in adapter.get("items", []) if row.get("id") == route_id]
                if matches:
                    item = matches[0]
                    candidates.append({"inventory_id": adapter["inventory_id"], "inventory_path": adapter["inventory_path"], "inventory_sha256": adapter["inventory_sha256"], "receipt_path": adapter["receipt_path"], "receipt_sha256": adapter["receipt_sha256"], "adapter": adapter["adapter"], "adapter_version": adapter["adapter_version"], "value": item, "evidence": adapter["evidence"]})
                else:
                    candidates.append({"inventory_id": adapter.get("inventory_id"), "status": "unknown", "reason": "route ID not in verified fixed Gin route receipt"})
            matched = [item for item in candidates if "value" in item]
            stale = [item for item in candidates if item.get("status") == "stale"]
            if stale:
                result.append({"id": ident, "status": "stale", "reason": "bound route receipt is stale", "evidence": stale, "coverage": {"limitations": ["Regenerate and reverify the route receipt before relying on this slice."]}})
            elif len(matched) > 1:
                result.append({"id": ident, "status": "conflict", "reason": "multiple route receipts provide the same route ID", "evidence": matched})
            elif matched:
                item = matched[0]
                fingerprint = hashlib.sha256(json.dumps({"manifest": manifest_evidence["sha256"], "inventory": item["inventory_sha256"], "receipt": item["receipt_sha256"]}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
                result.append({"id": ident, "status": "pass", "adapter": item["adapter"], "adapter_version": item["adapter_version"], "value": item["value"], "evidence": [{"path": "engineering-manifest.json", "sha256": manifest_evidence["sha256"]}, *item["evidence"], {"path": item["inventory_path"], "sha256": item["inventory_sha256"]}, {"path": item["receipt_path"], "sha256": item["receipt_sha256"]}], "source_fingerprint": fingerprint, "coverage": {"supported": ["fixed Gin route and bound source/semantic review receipt"], "excluded": ["dynamic plugin routes", "live middleware/handler execution", "deployed configuration"], "limitations": item["value"].get("limitations", []) + ["Receipt verification does not certify deployed authorization behavior."]}})
            else:
                status="unknown" if route_adapters else "unsupported"
                reason="route ID is not in a verified fixed-route receipt" if route_adapters else "no verified fixed-route adapter is declared"
                result.append({"id": ident, "status": status, "reason": reason, "evidence": candidates, "coverage": {"supported": ["fixed Gin route source receipts"], "excluded": ["dynamic routes","permissions","runtime behavior"], "limitations": ["A missing result does not mean the route is absent."]}})
            continue
        derived_candidates = []
        for adapter in source_derived_adapters:
            if adapter.get("kind") != "database" or adapter.get("adapter") != "gorm-source-v1":
                continue
            if adapter.get("problems"):
                derived_candidates.append({"status": "stale", "inventory_id": adapter.get("inventory_id"), "problems": adapter["problems"]})
                continue
            for row in adapter.get("items", []):
                if row.get("id") != table:
                    continue
                if field_match:
                    detail = next((value for value in row.get("detail", []) if value.get("column") == field_match.group(2)), None)
                    if detail is None:
                        derived_candidates.append({"status": "stale", "inventory_id": adapter["inventory_id"], "reason": "field missing from source-derived inventory"})
                    else:
                        derived_candidates.append({"status": "pass", "adapter_ref": adapter, "value": {"id": row["id"], "model": row.get("model"), "field": detail}})
                else:
                    value = {"id": row["id"], "model": row.get("model"), "source": row.get("source"), "fields": row.get("fields", []), "field_details": row.get("detail", []), "lifecycle": row.get("lifecycle")}
                    derived_candidates.append({"status": "pass", "adapter_ref": adapter, "value": value})
        stale_derived = [candidate for candidate in derived_candidates if candidate.get("status") == "stale"]
        matched_derived = [candidate for candidate in derived_candidates if candidate.get("status") == "pass"]
        if stale_derived:
            result.append({"id": ident, "status": "stale", "reason": "source-derived database receipt is stale or missing the requested field", "evidence": stale_derived, "coverage": {"limitations": ["Regenerate and reverify the database receipt before relying on this slice."]}})
            continue
        if len(matched_derived) > 1:
            result.append({"id": ident, "status": "conflict", "reason": "multiple verified source-derived inventories provide this table", "evidence": [{"inventory_id": candidate["adapter_ref"].get("inventory_id")} for candidate in matched_derived]})
            continue
        if matched_derived:
            candidate = matched_derived[0]; adapter = candidate["adapter_ref"]
            evidence = [{"path": "engineering-manifest.json", "sha256": manifest_evidence["sha256"]}] + adapter.get("evidence", []) + [{"path": adapter["inventory_path"], "sha256": adapter["inventory_sha256"]}, {"path": adapter["receipt_path"], "sha256": adapter["receipt_sha256"]}]
            fingerprint = hashlib.sha256(canonical_json({"manifest": manifest_evidence["sha256"], "evidence": evidence})).hexdigest()
            result.append({"id": ident, "status": "pass", "adapter": adapter["adapter"], "adapter_version": adapter["adapter_version"], "value": candidate["value"], "evidence": evidence, "source_fingerprint": fingerprint, "coverage": {"supported": ["hash-verified GORM/model/SQLite schema receipt"], "excluded": ["production business rows", "unlisted dynamic models", "all-dialect migration runtime behavior"], "limitations": ["This verifies the bound offline source receipt, not a live production database."]}})
            continue
        if extract_sqlite is not None:
            for entry, inventory, path in database_adapters:
                try:
                    live = extract_sqlite.extract(path)
                except (OSError, ValueError, __import__("sqlite3").Error) as exc:
                    candidates.append({"inventory": entry.get("id"), "path": path.relative_to(root).as_posix(), "error": str(exc)})
                    continue
                matches = [item for item in live.get("items", []) if item.get("id") == table]
                if not matches:
                    continue
                item = matches[0]
                if field_match:
                    detail = next((field for field in item.get("field_details", []) if field.get("name") == field_match.group(2)), None)
                    if detail is None:
                        candidates.append({"inventory": entry.get("id"), "path": path.relative_to(root).as_posix(), "error": "field is not present"})
                        continue
                    value = {"table": item["id"], "field": detail}
                else:
                    value = item
                candidates.append({"inventory": entry.get("id"), "path": path.relative_to(root).as_posix(), "sha256": digest(path.read_bytes()), "adapter_version": extract_sqlite.TOOL_VERSION, "value": value})
        successful = [candidate for candidate in candidates if "value" in candidate]
        if candidates and any("error" in candidate for candidate in candidates):
            result.append({"id": ident, "status": "unsupported", "reason": "declared SQLite source could not be safely queried", "evidence": candidates, "coverage": {"supported": ["checkpointed SQLite main schema"], "excluded": ["active WAL and unreadable sources"], "limitations": ["Extraction failure is not evidence that the requested object is absent."]}})
            continue
        if len(successful) == 1:
            candidate = successful[0]
            fingerprint = hashlib.sha256(json.dumps({"inventory": candidate["path"], "database_sha256": candidate["sha256"], "manifest": manifest_evidence["sha256"], "inventory_evidence": inventory_evidence}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            result.append({"id": ident, "status": "pass", "adapter": "sqlite-metadata", "adapter_version": candidate["adapter_version"], "value": candidate["value"], "evidence": [{"path": "engineering-manifest.json", "sha256": manifest_evidence["sha256"]}, *inventory_evidence, {"path": candidate["path"], "sha256": candidate["sha256"]}], "source_fingerprint": fingerprint, "coverage": {"supported": ["main schema table/view metadata", "table_xinfo fields"], "excluded": ["business rows", "active WAL databases", "permissions", "runtime behavior"], "limitations": ["Only checkpointed SQLite files declared by a database inventory are queried."]}})
        elif len(successful) > 1:
            result.append({"id": ident, "status": "conflict", "reason": "multiple declared SQLite inventories provide this ID", "evidence": successful})
        else:
            status = "unsupported" if candidates and any("error" in c for c in candidates) else "unknown"
            result.append({"id": ident, "status": status, "reason": "no supported declared SQLite source produced this object", "evidence": candidates, "coverage": {"supported": ["declared checkpointed SQLite metadata"], "excluded": ["undeclared databases", "active WAL", "routes", "permissions"], "limitations": ["No result is not evidence that the object is absent."]}})
    return {"status": "pass" if all(item.get("status") == "pass" for item in result) else "partial", "tool_version": "1", "inventory_problems": inventory_problems, "items": result}

def query_relations(root, module_id, source_paths):
    """Run the existing source relation adapters over a bounded current snapshot."""
    try:
        import collect_code_context
        import source_relations
    except ImportError as exc:
        return {"status": "unsupported", "reason": "source relation adapter unavailable", "detail": str(exc)}
    includes = []
    supported_suffixes = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts", ".rs")
    for raw in source_paths:
        try:
            source = check_project.safe_path(root, raw, file_only=False)
        except check_project.ConfigError:
            continue
        try:
            relative = check_project._relative_to_root(source,root).as_posix()
        except (OSError,ValueError):
            try:
                # Validate the declared relative source so safe_path and the
                # source collector agree on the ordinary project root spelling.
                plain_source = check_project.safe_path(root, raw, file_only=False)
                relative = plain_source.relative_to(root).as_posix()
                source = plain_source
            except (check_project.ConfigError, ValueError):
                continue
        if source.is_dir():
            for suffix in supported_suffixes:
                includes.append(relative.rstrip("/") + "/**/*" + suffix)
        elif source.is_file():
            if source.suffix.lower() in supported_suffixes:
                includes.append(relative)
    if not includes:
        return {"status": "unsupported", "reason": "module declares no readable source paths"}
    source_candidates = []
    for raw in source_paths:
        try:
            source = check_project.safe_path(root, raw, file_only=False)
        except check_project.ConfigError:
            continue
        if source.is_file() and source.suffix.lower() in supported_suffixes:
            source_candidates.append(source)
        elif source.is_dir():
            source_candidates.extend(candidate for candidate in source.rglob("*") if candidate.is_file() and candidate.suffix.lower() in supported_suffixes)
    if not source_candidates:
        return {"status": "unsupported", "reason": "module scope contains no supported JS/TS/Rust source files", "coverage": {"supported": ["JS/TS/Rust sources only"], "excluded": ["documentation, Python and other sources"], "limitations": ["No supported source input is not evidence that the module has no dependencies."]}}
    result = collect_code_context.collect(
        root, includes=includes, max_file_bytes=512 * 1024, max_total_bytes=8 * 1024 * 1024,
        max_files=200, max_depth=40, respect_gitignore=True,
    )
    analysis = source_relations.analyze_result(result)
    relations = analysis.get("references", [])
    evidence = analysis.get("files", [])
    coverage = {
        "supported": ["syntax-level JavaScript/TypeScript and Rust references when parsers are installed"],
        "excluded": ["runtime calls", "business semantics", "unread/oversized/excluded files", "dynamic resolution beyond adapter support"],
        "limitations": ["This is observed source references, not a runtime call graph; see per-file unknown and unsupported entries."],
    }
    if not analysis.get("files"):
        status = "unsupported"
    elif analysis.get("unsupported") or analysis.get("unknown") or not result["inventory"]["scan_complete_for_policy"]:
        status = "partial"
    else:
        status = "pass"
    return {
        "status": status,
        "adapter": "source-context-references",
        "adapter_version": collect_code_context.VERSION,
        "value": {"module_id": module_id, "relations": relations, "unknown": analysis.get("unknown", []), "unsupported": analysis.get("unsupported", [])},
        "evidence": evidence,
        "source_fingerprint": hashlib.sha256(json.dumps({"module": module_id, "sources": evidence, "policy": result["inventory"]["policy"], "analyzer": analysis.get("summary")}, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "coverage": coverage,
    }
def pointer_tokens(pointer):
    if not isinstance(pointer,str) or not pointer.startswith("/"): raise WorkflowStateError("JSON pointer must begin with slash")
    parts=pointer[1:].split("/")
    if any(re.search(r"~(?![01])",part) for part in parts): raise WorkflowStateError("invalid JSON pointer escape")
    if len(parts)>1 and parts[0]=="documents" and not re.fullmatch(r"0|[1-9][0-9]*",parts[1]): raise WorkflowStateError("document array index must use canonical decimal notation")
    return [x.replace("~1","/").replace("~0","~") for x in parts]
def protected_pointer(pointer,manifest):
    tokens=pointer_tokens(pointer)
    if len(tokens)<3 or len(tokens)>4 or tokens[0]!="documents" or tokens[2]!="lifecycle": return True
    if len(tokens)==4 and tokens[3] not in {"status","reason","superseded_by","evidence","module","conclusion","question","depends_on","resumption_condition","source_revision"}: return True
    try: return int(tokens[1])<0 or int(tokens[1])>=len(manifest["documents"])
    except (ValueError,KeyError,TypeError): return True
def is_protected_manifest_path(pointer,manifest=None):
    return protected_pointer(pointer,manifest or {"documents":[]})
def set_pointer(obj,tokens,value):
    cur=obj
    for token in tokens[:-1]:
        try:
            if isinstance(cur,list): cur=cur[int(token)]
            elif isinstance(cur,dict) and token in cur: cur=cur[token]
            elif isinstance(cur,dict) and token=="lifecycle": cur[token]={}; cur=cur[token]
            else: raise KeyError(token)
        except (ValueError,IndexError,KeyError,TypeError): raise WorkflowStateError("JSON pointer does not resolve")
    key=tokens[-1]
    try:
        if isinstance(cur,list): cur[int(key)]=value
        elif isinstance(cur,dict) and (key in cur or key in {"lifecycle","status","reason","superseded_by","evidence","module","conclusion","question","depends_on","resumption_condition","source_revision"}): cur[key]=value
        else: raise WorkflowStateError("JSON pointer target must already exist")
    except (ValueError,IndexError,TypeError): raise WorkflowStateError("JSON pointer target must already exist")
def replace_section(text,sid,content):
    if not isinstance(content,str): raise WorkflowStateError("replacement content must be text")
    found=sections(text).get(sid,[])
    if len(found)!=1: raise WorkflowStateError("section must match exactly once: "+str(sid))
    match,end=found[0]; nl="\r\n" if "\r\n" in match.group(0) else "\n"; body=content.replace("\r\n","\n").replace("\r","\n").strip("\n").replace("\n",nl)
    return text[:match.start()]+match.group(0)+(nl+body+nl if body else nl)+text[end:]
def atomic_replace(path,raw):
    if check_project.is_link(path): raise WorkflowStateError("refusing linked write target: "+str(path))
    fd,name=tempfile.mkstemp(prefix="."+path.name+".batch-",dir=path.parent); temp=Path(name)
    try:
        with os.fdopen(fd,"wb") as stream: stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(temp,path)
    finally: temp.unlink(missing_ok=True)
def read_request(root,path):
    try:
        request_path=check_project.safe_path(root,str(path))
        raw=request_path.read_bytes(); req=strict_json(raw,str(path))
    except (OSError,check_project.ConfigError) as exc: raise WorkflowStateError("cannot read batch request: "+str(exc)) from exc
    if not isinstance(req,dict) or set(req)-{"operation_id","expected_archive_head","operations"} or not isinstance(req.get("operation_id"),str) or not req["operation_id"].strip() or not isinstance(req.get("operations"),list) or not req["operations"]: raise WorkflowStateError("request requires operation_id and non-empty operations; unknown fields are rejected")
    if not isinstance(req.get("expected_archive_head"),str) or not req["expected_archive_head"]: raise WorkflowStateError("request requires expected_archive_head")
    return req,digest(raw),request_path
def apply_batch(root,manifest_path,manifest,request_path,store,project_id,apply=False,actor="local-agent"):
    req,req_hash,request_path=read_request(root,request_path); opid=req["operation_id"]
    if not task_archive.IDENTIFIER.fullmatch(opid): raise WorkflowStateError("invalid operation_id")
    task_by_id = {task.get("id"): task for task in manifest.get("tasks", []) if isinstance(task, dict)}
    for operation in req["operations"]:
        if isinstance(operation, dict) and operation.get("type") == "replace-section":
            task = task_by_id.get(operation.get("task_id"))
            if task is None:
                raise WorkflowStateError("section change-set operation requires a known task_id")
            role = operation.get("authority")
            expected = task.get("impact_document") if role == "impact" else (task.get("artifact_links", {}) or {}).get(role)
            if operation.get("document_id") != expected:
                raise WorkflowStateError("change-set target is not the selected Task's authority or linked view")
    try: db=task_archive.open_archive(store,project_id,create=False)
    except (task_archive.ArchiveError,sqlite3.DatabaseError) as exc: raise WorkflowStateError("batch apply requires initialized task archive: "+str(exc)) from exc
    try:
        prefix="workflow_state-operation="+opid+";"
        old=db.execute("SELECT revision,reason FROM revisions WHERE substr(reason,1,?)=?",(len(prefix),prefix)).fetchall()
        if old:
            matches=[rev for rev,reason in old if "request-sha256="+req_hash in reason]
            if matches: return {"status":"already_applied","operation_id":opid,"archive_revision":matches[0],"diff":[]}
            raise BatchConflict("operation_id reused with different request")
        head=task_archive.head(db)
        if req["expected_archive_head"]!=head: raise BatchConflict("archive head conflict: expected "+req["expected_archive_head"]+", found "+str(head))
        docs_list=[("ENGINEERING_MANIFEST",manifest_path)]+[(x["id"],check_project.safe_path(root,x["path"])) for x in manifest["documents"]]
        declared_paths={path for _,path in docs_list}
        if request_path in declared_paths: raise WorkflowStateError("batch request must not be one of its mutable manifest documents")
        saved=task_archive.files_for(db,head); drift=task_archive.compare(root,docs_list,saved)
        if drift: raise BatchConflict("workspace differs from archived head: "+"; ".join(drift))
        docs={x["id"]:x for x in manifest["documents"]}; docs["ENGINEERING_MANIFEST"]={"id":"ENGINEERING_MANIFEST","path":manifest_path.relative_to(root).as_posix(),"kind":"manifest"}; prepared={}; diffs=[]
        for operation in req["operations"]:
            if not isinstance(operation,dict) or operation.get("document_id") not in docs: raise WorkflowStateError("operation references unknown document")
            ident=operation["document_id"]
            allowed={"document_id","expected_sha256","type","section_id","content","task_id","authority"} if operation.get("type")=="replace-section" else {"document_id","expected_sha256","type","pointer","value"} if operation.get("type")=="set-json-pointer" else set()
            if not allowed or set(operation)-allowed or not {"document_id","expected_sha256","type"}<=set(operation): raise WorkflowStateError("operation fields do not match an exact supported schema")
            if ident in prepared: raise WorkflowStateError("each document may be targeted once per batch")
            item=docs[ident]; path=check_project.safe_path(root,item["path"]); before=path.read_bytes(); expected=operation.get("expected_sha256")
            if not isinstance(expected,str) or not SHA.fullmatch(expected) or digest(before)!=expected: raise BatchConflict("document hash conflict: "+ident)
            kind=operation.get("type")
            if kind=="replace-section":
                if operation.get("authority") not in {"baseline", "spec", "plan", "task", "impact", "traceability"}:
                    raise WorkflowStateError("change-set operation requires explicit authority classification")
                if ident=="ENGINEERING_MANIFEST" or item.get("kind") not in {"spec","plan","task","impact","assessment","verification","baseline","decision-log","traceability-index"}: raise WorkflowStateError("section update unsupported for this document kind")
                if not isinstance(operation.get("section_id"),str) or not operation["section_id"]: raise WorkflowStateError("section_id must be a non-empty string")
                after=replace_section(before.decode("utf-8-sig"),operation.get("section_id"),operation.get("content"))
                out=after.encode("utf-8-sig" if before.startswith(bytes.fromhex("efbbbf")) else "utf-8")
            elif kind=="set-json-pointer":
                if ident!="ENGINEERING_MANIFEST": raise WorkflowStateError("JSON updates restricted to manifest lifecycle metadata")
                pointer=operation.get("pointer")
                if protected_pointer(pointer,manifest): raise WorkflowStateError("batch cannot modify workflow, approval, task or check state")
                current=strict_json(before,"manifest")
                set_pointer(current,pointer_tokens(pointer),operation.get("value"))
                errors=manifest_diagnostics(current)
                if errors: raise WorkflowStateError("manifest update breaks references: "+"; ".join(errors))
                for entry in current.get("documents",[]):
                    if entry.get("lifecycle") is not None:
                        errors=lifecycle_metadata_errors(entry["lifecycle"],current)
                        if errors: raise WorkflowStateError("invalid lifecycle metadata for "+entry.get("id","document")+": "+"; ".join(errors))
                conflicts=lifecycle_pointer_conflicts(current)
                if conflicts: raise WorkflowStateError("manifest update creates lifecycle conflicts: "+"; ".join(conflicts))
                out=(json.dumps(current,ensure_ascii=False,indent=2)+"\n").encode("utf-8-sig" if before.startswith(bytes.fromhex("efbbbf")) else "utf-8")
            else: raise WorkflowStateError("unsupported operation type")
            prepared[ident]=(path,before,out)
            diff="".join(difflib.unified_diff(before.decode("utf-8-sig").splitlines(True),out.decode("utf-8-sig").splitlines(True),fromfile="a/"+item["path"],tofile="b/"+item["path"]))
            diffs.append({"document_id":ident,"path":item["path"],"before_sha256":digest(before),"after_sha256":digest(out),"diff":diff})
        report={"operation_id":opid,"expected_archive_head":head,"request_sha256":req_hash,"diff":diffs}
        if not apply: return {"status":"dry-run",**report}
        full={p:bytes(content) for p,content in saved.items()}
        for _,(path,_,out) in prepared.items(): full[path.relative_to(root).as_posix()]=out
        db.execute("BEGIN IMMEDIATE")
        try:
            if task_archive.head(db)!=head: raise BatchConflict("archive head changed; refresh snapshot")
            reason="workflow_state-operation="+opid+"; request-sha256="+req_hash
            drift=task_archive.compare(root,docs_list,saved)
            if drift: raise BatchConflict("workspace changed after batch validation: "+"; ".join(drift))
            revision=task_archive.insert_revision(db,root,manifest_path.relative_to(root).as_posix(),manifest,docs_list,head,actor,reason,source="workflow_state:"+opid,source_files=full)
            done=[]
            try:
                for path,before,out in prepared.values():
                    if digest(path.read_bytes())!=digest(before): raise BatchConflict("document changed during apply: "+str(path))
                    done.append((path,before)); atomic_replace(path,out)
                drift=task_archive.compare(root,docs_list,full)
                if drift: raise BatchConflict("workspace changed during batch apply: "+"; ".join(drift))
                db.commit()
            except Exception as write_error:
                rollback_failures=[]
                for path,before in reversed(done):
                    try: atomic_replace(path,before)
                    except Exception as rollback_error: rollback_failures.append(str(rollback_error))
                if rollback_failures: raise WorkflowStateError("batch projection may be partial; run task_archive restore --project-head; rollback failures: "+"; ".join(rollback_failures)) from write_error
                raise
        except Exception: db.rollback(); raise
        return {"status":"applied",**report,"archive_revision":revision}
    finally: db.close()
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",default="."); parser.add_argument("--manifest",default="engineering-manifest.json"); sub=parser.add_subparsers(dest="command",required=True)
    index=sub.add_parser("index"); index.add_argument("--format",choices=("json","markdown"),default="json")
    snap=sub.add_parser("snapshot"); snap.add_argument("--document-id",action="append",required=True); snap.add_argument("--section",action="append",default=[])
    query_parser=sub.add_parser("query"); query_parser.add_argument("--id",action="append",required=True); query_parser.add_argument("--relations",action="store_true")
    batch=sub.add_parser("apply-batch"); batch.add_argument("--request",required=True); batch.add_argument("--store",required=True); batch.add_argument("--project-id",required=True); batch.add_argument("--actor",default="local-agent"); batch.add_argument("--apply",action="store_true")
    args=parser.parse_args(argv)
    try:
        root,mp,manifest,_=load_project(args.root,args.manifest)
        if args.command=="index":
            rows=build_index(root,mp,manifest); print(render_markdown(rows) if args.format=="markdown" else json.dumps({"status":"pass","entries":rows},ensure_ascii=False,indent=2)); return 0
        if args.command=="snapshot": print(json.dumps(snapshot(root,mp,manifest,args.document_id,args.section),ensure_ascii=False,indent=2)); return 0
        if args.command=="query":
            result=query(root,manifest,args.id)
            if args.relations:
                modules = {item.get("id"): item for item in manifest.get("modules", []) if isinstance(item, dict)}
                for ident in args.id:
                    if not ident.startswith("module:"):
                        continue
                    module = modules.get(ident[len("module:"):])
                    if module is None:
                        continue
                    result["items"].append({"id": ident + ":relations", **query_relations(root, ident, module.get("source_paths", []))})
                result["status"] = "pass" if all(item.get("status") == "pass" for item in result["items"]) else "partial"
            print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result["status"]=="pass" else 1
        store=resolve_archive_store(args.store,root)
        result=apply_batch(root,mp,manifest,Path(args.request),store,args.project_id,args.apply,args.actor); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (WorkflowStateError,check_project.ConfigError,task_archive.ArchiveError,sqlite3.DatabaseError,OSError,ValueError) as exc:
        status="unsupported" if isinstance(exc,UnsupportedHostError) else "conflict" if isinstance(exc,BatchConflict) else "error"
        print(json.dumps({"status":status,"message":str(exc)},ensure_ascii=False),file=sys.stderr); return 1 if isinstance(exc,BatchConflict) else 2
if __name__=="__main__": raise SystemExit(main())
