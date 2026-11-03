"""C1 syntax/import/diff/pins ONLY. No emitter instance or native/RPM/game."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parsed=[]
    for p in OUT.rglob('*.py'):
        text=p.read_text('utf-8-sig');ast.parse(text);compile(text,str(p),'exec');parsed.append(p.relative_to(OUT).as_posix())
    import source_imports
    modules=source_imports.load()
    # Import only. None of the emitter/helper functions are invoked here.
    import x86,build
    n=modules['native'];layout=modules['path_diagnostic_layout']
    assert (n.PLAN_SIZE,layout.PLAN_SIZE,layout.GENERATION_OFFSET,layout.RECORD_OFFSET,layout.STATE_SIZE)==(0x79800,0x79800,0x79800,0x79804,0x79904)
    parent=source_imports.PARENT
    old=(parent/'native.py').read_text('utf-8');new=(OUT/'native.py').read_text('utf-8-sig')
    def part(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
    for a,b in [(" r.push(1);r.push(0);r.push(1);r.lea('eax',m('ebp',-32))","r.mov(m('ebp',-36),'eax')"),("r.label('path_free')","r.label('path_done')"),("def safety(r):","def path(r):")]:
        assert part(old,a,b)==part(new,a,b),a
    for name in ('policy.py','path_diagnostic_layout.py'):
        assert (OUT/name).read_bytes()==(parent/name).read_bytes(),name
    gate=json.loads((OUT/'ROOT-VRIJGAVE.json').read_text('utf-8'))
    assert all(v is False for v in gate.values()),'all root gates stay false'
    assert not any(OUT.rglob('*.dll')) and not any(OUT.rglob('*.exe')) and not any(OUT.rglob('*.bin'))
    diffdir=OUT/'diffs';diffdir.mkdir(exist_ok=True)
    changed=[]
    originals=('native.py','policy.py','path_diagnostic.py','path_diagnostic_layout.py','reader/path_failure_decoder.py')
    for name in originals:
        before=parent/name;after=OUT/name
        if before.read_bytes()==after.read_bytes():continue
        changed.append(name)
        (diffdir/(name.replace('/','__')+'.diff')).write_text(''.join(difflib.unified_diff(before.read_text('utf-8').splitlines(True),after.read_text('utf-8-sig').splitlines(True),fromfile=before.relative_to(ROOT).as_posix(),tofile=after.relative_to(ROOT).as_posix())),'utf-8')
    imported={Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).lower().startswith(str(ROOT).lower())}
    # Modules whose functions are deferred until future emission, plus exact
    # parent source/binary provenance. Pin the already frozen full parent set.
    provenance=json.loads((parent/'SOURCE-PINS.json').read_text('utf-8'))
    external={ROOT/row['path'] for row in provenance['sources']}
    for row in provenance['sources']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
    external|={parent/name for name in originals}
    external|={parent/'SOURCE-PINS.json',parent/'candidate-manifest.json',parent/'U30-40.prepared.dll',parent/'build_candidate.py',parent/'input-pins.py',parent/'input-pins.json'}
    external|={ROOT/'ONTWERP/PAD-LOKAAL-ONBEKEND-2026-10-22.md',ROOT/'ANALYSE/PAD-ONBEKEND-EN-SELECTIEPREFIX-2026-10-22.md'}
    result=dict(stage='C1_SOURCE_READY_FOR_ROOT_REVIEW_ONLY',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),AST=sorted(parsed),imports={k:str(Path(m.__file__).relative_to(ROOT)).replace('\\','/') for k,m in modules.items()},changed=changed,policy_and_layout_byte_identical=True,native_twenty_args_and_cleanup_and_safety_source_identical=True,emitter_invoked=False,candidate_build=False,native=False,RPM=False,game=False,install=False,gameplay_measured=False,remaining=['root C1 source review','separate C2 emission/byte/callsite review','separate native gate and fixture adaptation','separate host gate/horizon'])
    (OUT/'SOURCE-REVIEW.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
    paths=imported|external|set(OUT.rglob('*.py'))|set(diffdir.glob('*.diff'))|{OUT/'SOURCE-REVIEW.json',OUT/'ROOT-VRIJGAVE.json',OUT/'BRONOVERDRACHT.md'}
    pins=dict(stage=result['stage'],parent_candidate_sha256=sha(parent/'U30-40.prepared.dll'),parent_manifest_sha256=sha(parent/'candidate-manifest.json'),sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size) for p in sorted(paths)])
    assert pins['parent_candidate_sha256']=='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
    assert pins['parent_manifest_sha256']=='5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152'
    (OUT/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2)+'\n','utf-8')
    print(json.dumps(dict(stage=result['stage'],AST=len(parsed),pins=len(pins['sources']),changed=changed,emission=False,native=False)))

if __name__=='__main__':main()
