#!/usr/bin/env python3
"""Version and recover manifest-declared engineering records in a local SQLite archive.

This tool detects direct workspace changes but cannot prevent arbitrary shell writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
import check_project

ARCHIVE_FORMAT = 1
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,119}$")

class ArchiveError(Exception):
    pass

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")

def open_archive(path: Path, project_id: str, create: bool = False):
    if not IDENTIFIER.fullmatch(project_id): raise ArchiveError("invalid project ID")
    if path.exists() and (path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())): raise ArchiveError("archive must not be a link")
    if not path.exists():
        if not create: raise ArchiveError("archive is missing; run init first")
        path.parent.mkdir(parents=True, exist_ok=True)
    db=sqlite3.connect(path, timeout=15, isolation_level=None)
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA synchronous=FULL")
    db.executescript("CREATE TABLE IF NOT EXISTS meta (id INTEGER PRIMARY KEY CHECK(id=1), format_version INTEGER NOT NULL, project_id TEXT NOT NULL); CREATE TABLE IF NOT EXISTS revisions (revision TEXT PRIMARY KEY, parent TEXT, created_at TEXT NOT NULL, actor TEXT NOT NULL, reason TEXT NOT NULL, source_revision TEXT, manifest_path TEXT NOT NULL, manifest_sha256 TEXT NOT NULL); CREATE TABLE IF NOT EXISTS files (revision TEXT NOT NULL REFERENCES revisions(revision), path TEXT NOT NULL, document_id TEXT NOT NULL, content BLOB NOT NULL, sha256 TEXT NOT NULL, PRIMARY KEY(revision,path)); CREATE TABLE IF NOT EXISTS archive_head (id INTEGER PRIMARY KEY CHECK(id=1), revision TEXT NOT NULL REFERENCES revisions(revision)); CREATE TRIGGER IF NOT EXISTS immutable_revision_update BEFORE UPDATE ON revisions BEGIN SELECT RAISE(ABORT,'archive revisions are immutable'); END; CREATE TRIGGER IF NOT EXISTS immutable_revision_delete BEFORE DELETE ON revisions BEGIN SELECT RAISE(ABORT,'archive revisions are immutable'); END; CREATE TRIGGER IF NOT EXISTS immutable_file_update BEFORE UPDATE ON files BEGIN SELECT RAISE(ABORT,'archive content is immutable'); END; CREATE TRIGGER IF NOT EXISTS immutable_file_delete BEFORE DELETE ON files BEGIN SELECT RAISE(ABORT,'archive content is immutable'); END;")
    meta=db.execute("SELECT format_version,project_id FROM meta WHERE id=1").fetchone()
    if meta is None and create: db.execute("INSERT INTO meta(id,format_version,project_id) VALUES(1,?,?)",(ARCHIVE_FORMAT,project_id))
    elif meta != (ARCHIVE_FORMAT,project_id): db.close(); raise ArchiveError("archive format or project ID mismatch")
    if create:
        rows=db.execute("SELECT revision,parent FROM revisions ORDER BY rowid").fetchall()
        saved=db.execute("SELECT revision FROM archive_head WHERE id=1").fetchone()
        expected_parent=None
        for revision,parent in rows:
            if parent!=expected_parent:
                db.close(); raise ArchiveError("archive revision chain is inconsistent")
            expected_parent=revision
        if (rows and (saved is None or saved[0]!=rows[-1][0])) or (not rows and saved is not None):
            db.close(); raise ArchiveError("archive history/head consistency check failed")
    return db

def declared(root: Path, manifest_arg: str):
    manifest_path=check_project.safe_path(root,manifest_arg)
    manifest=check_project.read_json(manifest_path)
    if not isinstance(manifest,dict) or not isinstance(manifest.get("documents"),list): raise ArchiveError("manifest requires documents array")
    docs=[("ENGINEERING_MANIFEST",manifest_path)]; seen={manifest_path.relative_to(root).as_posix()}
    for item in manifest["documents"]:
        if not isinstance(item,dict) or not isinstance(item.get("id"),str) or not isinstance(item.get("path"),str): raise ArchiveError("invalid document entry")
        path=check_project.safe_path(root,item["path"]); rel=path.relative_to(root).as_posix()
        if rel in seen: raise ArchiveError("duplicate manifest document path: "+rel)
        if not path.is_file(): raise ArchiveError("missing manifest document: "+rel)
        seen.add(rel); docs.append((item["id"],path))
    return manifest,sorted(docs,key=lambda x:x[1].relative_to(root).as_posix())

def declared_from_archived_manifest(root: Path, manifest_path: Path, manifest):
    if not isinstance(manifest,dict) or not isinstance(manifest.get("documents"),list): raise ArchiveError("archived manifest requires documents array")
    docs=[("ENGINEERING_MANIFEST",manifest_path)]; seen={manifest_path.relative_to(root).as_posix()}
    for item in manifest["documents"]:
        if not isinstance(item,dict) or not isinstance(item.get("id"),str) or not isinstance(item.get("path"),str): raise ArchiveError("invalid archived document entry")
        path=check_project.safe_path(root,item["path"]); rel=path.relative_to(root).as_posix()
        if rel in seen: raise ArchiveError("duplicate archived document path: "+rel)
        seen.add(rel); docs.append((item["id"],path))
    return sorted(docs,key=lambda x:x[1].relative_to(root).as_posix())

def head(db):
    row=db.execute("SELECT revision FROM archive_head WHERE id=1").fetchone()
    return row[0] if row else None

def files_for(db,revision):
    rows=db.execute("SELECT path,content,sha256 FROM files WHERE revision=? ORDER BY path",(revision,)).fetchall()
    if not rows: raise ArchiveError("revision has no files")
    result={}
    for path,content,sha in rows:
        raw=bytes(content)
        if digest(raw)!=sha: raise ArchiveError("archive digest mismatch: "+path)
        result[path]=raw
    return result

def insert_revision(db,root,manifest_arg,manifest,docs,parent,actor,reason,source=None,source_files=None):
    revision=uuid.uuid4().hex; mpath=check_project.safe_path(root,manifest_arg); manifest_rel=mpath.relative_to(root).as_posix()
    manifest_bytes=source_files.get(manifest_rel) if source_files is not None and manifest_rel in source_files else mpath.read_bytes()
    msha=digest(manifest_bytes)
    db.execute("INSERT INTO revisions VALUES(?,?,?,?,?,?,?,?)",(revision,parent,utc_now(),actor,reason,source,Path(manifest_arg).as_posix(),msha))
    if source_files is None: entries=[(p.relative_to(root).as_posix(),doc_id,p.read_bytes()) for doc_id,p in docs]
    else: entries=[(rel,next((doc_id for doc_id,p in docs if p.relative_to(root).as_posix()==rel),"RECOVERED"),raw) for rel,raw in source_files.items()]
    for rel,doc_id,raw in entries: db.execute("INSERT INTO files VALUES(?,?,?,?,?)",(revision,rel,doc_id,raw,digest(raw)))
    db.execute("INSERT INTO archive_head(id,revision) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET revision=excluded.revision",(revision,))
    return revision

def compare(root,docs,saved):
    current={p.relative_to(root).as_posix():p for _,p in docs}; diff=[]
    if set(current)!=set(saved): diff.append("manifest document set differs from archive")
    for rel in sorted(set(current)|set(saved)):
        if rel not in current: diff.append("missing workspace document: "+rel)
        elif rel not in saved: diff.append("new manifest document: "+rel)
        elif current[rel].read_bytes()!=saved[rel]: diff.append("workspace document differs: "+rel)
    return diff

def atomic_replace(path,raw):
    if path.is_symlink() or bool(getattr(path,"is_junction",lambda:False)()): raise ArchiveError("refuse linked restore target")
    fd,name=tempfile.mkstemp(prefix="."+path.name+".restore-",dir=path.parent); tmp=Path(name)
    try:
        with os.fdopen(fd,"wb") as stream: stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally: tmp.unlink(missing_ok=True)

def cmd_init(args,root,db):
    manifest,docs=declared(root,args.manifest); db.execute("BEGIN IMMEDIATE")
    try:
        if head(db): raise ArchiveError("archive already has history; refusing reset")
        rev=insert_revision(db,root,args.manifest,manifest,docs,None,args.actor,"initial snapshot: "+args.reason); db.commit()
    except Exception: db.rollback(); raise
    print(json.dumps({"status":"pass","revision":rev,"document_count":len(docs),"message":"snapshot stored outside workspace; Git state unchanged"},ensure_ascii=False)); return 0

def cmd_check(args,root,db):
    current_head=head(db)
    if not current_head: raise ArchiveError("empty archive; run init")
    manifest,docs=declared(root,args.manifest); diff=compare(root,docs,files_for(db,current_head))
    if not args.save:
        print(json.dumps({"status":"pass" if not diff else "fail","head_revision":current_head,"differences":diff},ensure_ascii=False)); return 0 if not diff else 1
    if args.expected_head != current_head:
        print(json.dumps({"status":"error","message":"expected archive head does not match; inspect history and retry","actual_head":current_head},ensure_ascii=False),file=sys.stderr); return 2
    # A checkpoint intentionally turns the current workspace into a new revision.
    db.execute("BEGIN IMMEDIATE")
    try:
        if head(db)!=current_head: raise ArchiveError("archive head changed; retry against latest revision")
        rev=insert_revision(db,root,args.manifest,manifest,docs,current_head,args.actor,args.reason + ("; approved-current-head=" + current_head)); db.commit()
    except Exception: db.rollback(); raise
    print(json.dumps({"status":"pass","revision":rev,"parent_revision":current_head},ensure_ascii=False)); return 0

def cmd_history(args,root,db):
    rows=db.execute("SELECT revision,parent,created_at,actor,reason,source_revision FROM revisions ORDER BY rowid").fetchall()
    names=("revision","parent_revision","created_at","actor","reason","source_revision")
    revisions=[]
    for row in rows:
        item=dict(zip(names,row))
        item["files"]=[{"path":path,"sha256":sha} for path,sha in db.execute("SELECT path,sha256 FROM files WHERE revision=? ORDER BY path",(item["revision"],)).fetchall()]
        revisions.append(item)
    print(json.dumps({"revisions":revisions},ensure_ascii=False,indent=2)); return 0

def cmd_restore(args,root,db):
    current_head=head(db)
    if not current_head: raise ArchiveError("empty archive")
    target_rev=current_head if args.project_head else args.revision
    if not target_rev: raise ArchiveError("provide a revision or --project-head")
    if not db.execute("SELECT 1 FROM revisions WHERE revision=?",(target_rev,)).fetchone(): raise ArchiveError("revision does not exist")
    target=files_for(db,target_rev)
    if args.project_head:
        manifest_path=check_project.safe_path(root,args.manifest)
        manifest_rel=manifest_path.relative_to(root).as_posix()
        archived_manifest=target.get(manifest_rel)
        if archived_manifest is None: raise ArchiveError("archive head does not contain the manifest")
        manifest=check_project.parse_json(archived_manifest,"archived manifest")
        docs=declared_from_archived_manifest(root,manifest_path,manifest)
    else:
        manifest,docs=declared(root,args.manifest)
    diff=compare(root,docs,files_for(db,current_head))
    if diff and not args.project_head: raise ArchiveError("workspace has unsaved differences; checkpoint before restore")
    if set(target)!={p.relative_to(root).as_posix() for _,p in docs}: raise ArchiveError("revision document set differs from manifest")
    db.execute("BEGIN IMMEDIATE")
    try:
        if head(db)!=current_head: raise ArchiveError("archive head changed; retry restore")
        rev=insert_revision(db,root,args.manifest,manifest,docs,current_head,args.actor,args.reason,target_rev,target); db.commit()
    except Exception: db.rollback(); raise
    failures=[]
    for rel,raw in target.items():
        try: atomic_replace(check_project.safe_path(root,rel),raw)
        except (OSError,ArchiveError,check_project.ConfigError) as exc: failures.append({"path":rel,"error":str(exc)})
    print(json.dumps({"status":"pass" if not failures else "partial","revision":rev,"source_revision":target_rev,"failures":failures},ensure_ascii=False)); return 0 if not failures else 1

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",default="."); parser.add_argument("--manifest",default="engineering-manifest.json"); parser.add_argument("--store",required=True,help="local SQLite path outside project root"); parser.add_argument("--project-id",required=True); parser.add_argument("--actor",default="local-agent")
    sub=parser.add_subparsers(dest="command",required=True)
    init=sub.add_parser("init"); init.add_argument("--reason",default="adopt current state")
    chk=sub.add_parser("check"); chk.add_argument("--save",action="store_true"); chk.add_argument("--expected-head"); chk.add_argument("--reason",default="checkpoint")
    sub.add_parser("history")
    rst=sub.add_parser("restore"); rst.add_argument("revision",nargs="?"); rst.add_argument("--project-head",action="store_true"); rst.add_argument("--reason",default="user-requested restore")
    args=parser.parse_args(argv)
    try:
        root=check_project.safe_root(args.root); store=Path(args.store).expanduser().absolute()
        try: store.relative_to(root)
        except ValueError: pass
        else: raise ArchiveError("archive must be stored outside project root")
        db=open_archive(store,args.project_id,create=args.command=="init")
        try: return {"init":cmd_init,"check":cmd_check,"history":cmd_history,"restore":cmd_restore}[args.command](args,root,db)
        finally: db.close()
    except (ArchiveError,check_project.ConfigError,OSError,ValueError,sqlite3.DatabaseError) as exc:
        print(json.dumps({"status":"error","message":str(exc)},ensure_ascii=False),file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
