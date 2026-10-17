/** Static module references, not a call graph or semantic architecture oracle.
 * Derived from GitDiagram's reference-index/evidence design (MIT Ahmed Khaleel
 * 2024). Parsing/config resolution is a local adaptation using TypeScript.
 * No project code is imported or executed. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { builtinModules } from 'node:module';
import ts from './context-runtime/node_modules/typescript/lib/typescript.js';

const normalize=(p)=>path.resolve(p).replaceAll('\\','/');
const key=(p)=>process.platform==='win32'?normalize(p).toLowerCase():normalize(p);
const hash=(text)=>crypto.createHash('sha256').update(text).digest('hex');
const JS=/\.(?:[cm]?[jt]sx?)$/i;

export function analyze(request) {
  const root=normalize(request.root);
  const files=new Map(request.files.map(p=>[key(path.join(root,p)),p]));
  const directories=new Set([key(root),...request.directories.map(p=>key(path.join(root,p)))]);
  const supported=request.sources.filter(s=>JS.test(s.path));
  const configAudit=new Map();
  const within=(p)=>key(p)===key(root)||key(p).startsWith(key(root)+'/');
  const read=(p)=>{
    if(!within(p)||!files.has(key(p)))return undefined;
    try {
      const absolute=normalize(p);
      if(key(fs.realpathSync(absolute))!==key(absolute)||fs.statSync(absolute).size>512000)return undefined;
      return fs.readFileSync(absolute,'utf8');
    } catch {return undefined;}
  };
  const host={fileExists:p=>within(p)&&files.has(key(p)),readFile:read,
    directoryExists:p=>within(p)&&directories.has(key(p)),realpath:p=>normalize(p),
    getCurrentDirectory:()=>root,useCaseSensitiveFileNames:process.platform!=='win32',
    readDirectory:(folder,extensions)=>[...files.keys()].filter(p=>p.startsWith(key(folder)+'/')&&(!extensions||extensions.some(ext=>p.endsWith(ext)))),
    onUnRecoverableConfigFileDiagnostic:diagnostic=>configAudit.set('error:'+diagnostic.code,ts.flattenDiagnosticMessageText(diagnostic.messageText,' '))};
  const configs=new Map();
  function optionsFor(source) {
    let folder=path.dirname(path.join(root,source));
    while(within(folder)) {
      const candidate=path.join(folder,'tsconfig.json');
      if(files.has(key(candidate))) {
        if(!configs.has(key(candidate))) {
          const parsed=ts.getParsedCommandLineOfConfigFile(candidate,{},host);
          const relative=files.get(key(candidate));
          configs.set(key(candidate),parsed?.options??{});
          configAudit.set(relative,{path:relative,sha256:hash(read(candidate)??''),
            issues:(parsed?.errors??[]).filter(e=>e.code!==18003).map(e=>({code:e.code,message:ts.flattenDiagnosticMessageText(e.messageText,' ')}))});
        }
        return {options:configs.get(key(candidate)),config:files.get(key(candidate))};
      }
      if(key(folder)===key(root))break;
      folder=path.dirname(folder);
    }
    return {options:{moduleResolution:ts.ModuleResolutionKind.Bundler,allowJs:true,resolveJsonModule:true},config:null};
  }
  const workspace=new Map();
  for(const name of request.files.filter(p=>p==='package.json'||/^packages\/[^/]+\/package\.json$/.test(p))) {
    try {
      const data=JSON.parse(read(path.join(root,name))??'null');
      if(data?.name)workspace.set(data.name,{data,folder:path.posix.dirname(name),manifest:name});
    } catch {/* config audit records unresolved references without guessed paths */}
  }
  function explicitWorkspace(specifier) {
    for(const [name,item] of workspace) {
      if(specifier!==name&&!specifier.startsWith(name+'/'))continue;
      const sub=specifier===name?'.':'./'+specifier.slice(name.length+1);
      let entry=item.data.exports;
      if(entry&&typeof entry==='object'&&!Array.isArray(entry)&&Object.keys(entry).some(k=>k.startsWith('.')))entry=entry[sub];
      const choose=value=>typeof value==='string'?value:(value&&typeof value==='object'?choose(value.source??value.import??value.default??value.types):null);
      const picked=choose(entry)??(sub==='.'?item.data.source??item.data.module??item.data.main:null);
      if(typeof picked==='string') {
        const absolute=path.join(root,item.folder,picked);
        if(files.has(key(absolute)))return {target:files.get(key(absolute)),basis:item.manifest};
      }
      return {target:null,basis:item.manifest};
    }
    return null;
  }
  const references=[],unknown=[],fileAudits=[];
  const builtins=new Set(builtinModules.flatMap(s=>[s,s.replace(/^node:/,''),'node:'+s.replace(/^node:/,'')]));
  for(const source of supported) {
    const config=optionsFor(source.path);
    const sourceFile=ts.createSourceFile(source.path,source.text,ts.ScriptTarget.Latest,true,
      /\.tsx$/i.test(source.path)?ts.ScriptKind.TSX:/\.jsx$/i.test(source.path)?ts.ScriptKind.JSX:/\.[cm]?js$/i.test(source.path)?ts.ScriptKind.JS:ts.ScriptKind.TS);
    const parseErrors=sourceFile.parseDiagnostics.map(d=>({code:d.code,message:ts.flattenDiagnosticMessageText(d.messageText,' ')}));
    fileAudits.push({path:source.path,sha256:source.sha256,parser:'typescript-'+ts.version,config:config.config,parse_errors:parseErrors});
    if(parseErrors.length){unknown.push({path:source.path,status:'parse_error',count:parseErrors.length});continue;}
    function record(node,literal,kind,typeOnly=false) {
      const start=sourceFile.getLineAndCharacterOfPosition(node.getStart(sourceFile));
      const end=sourceFile.getLineAndCharacterOfPosition(node.getEnd());
      if(!literal||!ts.isStringLiteralLike(literal)) {
        unknown.push({path:source.path,line:start.line+1,kind,status:'dynamic_specifier_unknown'});return;
      }
      const specifier=literal.text;
      const hit=ts.resolveModuleName(specifier,path.join(root,source.path),config.options,host).resolvedModule;
      let target=hit&&files.get(key(hit.resolvedFileName));
      let basis=target?'typescript_project_resolution':null;
      const packageInfo=explicitWorkspace(specifier);
      if(!target&&packageInfo?.target){target=packageInfo.target;basis='explicit_workspace_entry';}
      const status=target?'resolved':builtins.has(specifier)?'builtin':packageInfo?'workspace_unresolved':specifier.startsWith('.')||specifier.startsWith('/')?'local_unresolved':'external_or_unresolved';
      references.push({from:source.path,to:target??null,specifier,kind,type_only:typeOnly,status,
        evidence:{path:source.path,line:start.line+1,end_line:end.line+1,sha256:source.sha256,
          statement:source.text.slice(node.getStart(sourceFile),node.getEnd()),config:config.config,resolution_basis:basis},
        semantics:'module_reference_observed; runtime invocation and business behavior not established'});
    }
    function visit(node) {
      if(ts.isImportDeclaration(node)) {
        const bindings=node.importClause?.namedBindings;
        const only=node.importClause?.isTypeOnly||(!node.importClause?.name&&bindings&&ts.isNamedImports(bindings)&&bindings.elements.length>0&&bindings.elements.every(e=>e.isTypeOnly));
        record(node,node.moduleSpecifier,'import',Boolean(only));
      } else if(ts.isExportDeclaration(node)&&node.moduleSpecifier) {
        record(node,node.moduleSpecifier,'reexport',Boolean(node.isTypeOnly));
      } else if(ts.isImportEqualsDeclaration(node)&&ts.isExternalModuleReference(node.moduleReference)) {
        record(node,node.moduleReference.expression,'import_equals',Boolean(node.isTypeOnly));
      } else if(ts.isImportTypeNode(node)&&ts.isLiteralTypeNode(node.argument)) {
        record(node,node.argument.literal,'import_type',true);
      } else if(ts.isCallExpression(node)&&node.expression.kind===ts.SyntaxKind.ImportKeyword) {
        record(node,node.arguments[0],'dynamic_import_literal');
      } else if(ts.isCallExpression(node)&&ts.isIdentifier(node.expression)&&node.expression.text==='require') {
        // A shadowed require is syntax-only evidence, never a confirmed loader.
        record(node,node.arguments[0],'require_literal_syntax');
      }
      ts.forEachChild(node,visit);
    }
    visit(sourceFile);
  }
  const unsupported=request.sources.filter(s=>!JS.test(s.path)).map(s=>({path:s.path,status:'language_not_supported'}));
  return {schema_version:1,parser:'typescript-'+ts.version,scope:'Explicitly supplied full JS/TS source; no project execution, call graph or dependency completeness guarantee',
    references,unknown,unsupported,files:fileAudits,configuration:[...configAudit.values()],
    summary:{source_files:supported.length,unsupported_files:unsupported.length,references:references.length,
      resolved:references.filter(r=>r.status==='resolved').length,type_only:references.filter(r=>r.status==='resolved'&&r.type_only).length,
      unresolved:references.filter(r=>!['resolved','builtin'].includes(r.status)).length,dynamic_unknown:unknown.filter(r=>r.status==='dynamic_specifier_unknown').length}};
}

if(process.argv[2]) {
  try {console.log(JSON.stringify(analyze(JSON.parse(fs.readFileSync(process.argv[2],'utf8')))));}
  catch(error){console.log(JSON.stringify({status:'error',error_type:error.name,message:String(error.message)}));process.exitCode=2;}
}
