"""C2a AST/import/pins only. Never calls compose(), main() or any emitter."""
from pathlib import Path
import ast,datetime,difflib,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parsed=[]
    for path in OUT.glob('*.py'):
        text=path.read_text('utf-8');ast.parse(text);compile(text,str(path),'exec');parsed.append(path.name)
    spec=importlib.util.spec_from_file_location('local4_builder_adapter',OUT/'build_candidate.py')
    builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    assert sha(builder.C1/'SOURCE-PINS.json')==builder.C1_PINS
    c1=builder.check_pins(builder.C1/'SOURCE-PINS.json')
    assert sha(builder.PARENT/'U30-40.prepared.dll')==builder.PARENT_DLL
    assert sha(builder.PARENT/'candidate-manifest.json')==builder.PARENT_MANIFEST
    assert sha(builder.PARENT/'build_candidate.py')==builder.PARENT_BUILDER
    gate=json.loads((OUT/'ROOT-VRIJGAVE.json').read_text('utf-8'))
    assert gate['reviewed_source_pins_sha256'] is None
    assert all(gate[k] is False for k in ('candidate_build_allowed','native_allowed','RPM_allowed','game_allowed','install_allowed'))
    try:builder.require_build_gate()
    except AssertionError as error:assert str(error)=='Separate root C2 build release required'
    else:raise AssertionError('Closed gate did not reject build entry')
    # Fresh interpreter, exact local modules loaded before historical builder.
    parent,effective=builder.load_recipe()
    builder.bind_verify_base(parent)
    assert parent.verify_base.__module__==builder.__name__
    assert parent.OUT==builder.PARENT
    assert (parent.native.PLAN_SIZE,parent.path_layout.STATE_SIZE)==(0x79800,0x79904)
    assert not any(OUT.rglob('*.dll')) and not any(OUT.rglob('*.exe')) and not any(OUT.rglob('*.bin'))
    # Compact entry-route diff; historical compose is reused byte-for-byte.
    oldtext=(builder.PARENT/'build_candidate.py').read_text('utf-8');newtext=(OUT/'build_candidate.py').read_text('utf-8')
    oldtree=ast.parse(oldtext);newtree=ast.parse(newtext)
    def functions(tree,text,names):return '\n\n'.join(ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names)+'\n'
    old=functions(oldtree,oldtext,{'verify_base','main'})
    new=functions(newtree,newtext,{'require_build_gate','load_recipe','bind_verify_base','effective_manifest','compose','main'})
    (OUT/'ADAPTER-ENTRY.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='historical verify_base/main (compose body reused)',tofile='owned gated adapter entry/manifest/output')),'utf-8')
    imported={Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).lower().startswith(str(ROOT).lower())}
    report=dict(stage='C2A_BUILDER_SOURCE_ONLY_PENDING_ROOT_REVIEW',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),AST=parsed,closed_gate_rejected=True,C1_pins_verified=len(c1['sources']),imports={k:Path(v.__file__).relative_to(ROOT).as_posix() for k,v in effective.items()},historical_builder_imported_only=True,historical_verify_base_replaced=True,historical_main_called=False,compose_called=False,emission=False,native=False,RPM=False,game=False,install=False,remaining=['root adapter source review','separate exact-source C2 build gate','emitted byte/callsite/state/guard checks','separate native gate'])
    (OUT/'SOURCE-REVIEW.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
    # Own root gate is deliberately mutable and excluded. Gate approval must
    # bind this immutable SOURCE-PINS hash; the frozen C1 false gate stays pinned.
    paths=imported|{ROOT/r['path'] for r in c1['sources']}|set(OUT.glob('*.py'))|{builder.C1/'SOURCE-PINS.json',ROOT/'ANALYSE/REVIEW-PAD-LOKAAL-23.md',OUT/'BRONOVERDRACHT.md',OUT/'ADAPTER-ENTRY.diff',OUT/'SOURCE-REVIEW.json'}
    pins=dict(stage=report['stage'],C1_source_pins_sha256=builder.C1_PINS,sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size) for p in sorted(paths)])
    (OUT/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2)+'\n','utf-8')
    builder.verify_sources()
    print(json.dumps(dict(stage=report['stage'],AST=len(parsed),pins=len(pins['sources']),C1=len(c1['sources']),compose=False,emission=False,native=False)))

if __name__=='__main__':main()
