"""Own C2 adapter SOURCE. Import is inert; compose requires own root gate.

Reuse the frozen historical compose(), never its main() or output directory.
No native calls, game process, RPM or installation are provided here.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
C1=OUT.parent/'20261022T180000'
PARENT=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500'
C1_PINS='4a2799b02e68fc2338c655d1f28983e6ee83bcd05a074abb2131521e436f737f'
PARENT_DLL='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
PARENT_MANIFEST='5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152'
PARENT_BUILDER='b042c85eb551bb2178ea84f59bbd68b25c384e5f3afd961c296eb107926b1fea'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj

def check_pins(path):
    pins=json.loads(path.read_text('utf-8'))
    for row in pins['sources']:
        p=(ROOT/row['path']).resolve();p.relative_to(ROOT)
        assert sha(p)==row['sha256'],row['path']
    return pins

def verify_sources():
    assert sha(C1/'SOURCE-PINS.json')==C1_PINS
    check_pins(C1/'SOURCE-PINS.json')
    assert sha(PARENT/'U30-40.prepared.dll')==PARENT_DLL
    assert sha(PARENT/'candidate-manifest.json')==PARENT_MANIFEST
    assert sha(PARENT/'build_candidate.py')==PARENT_BUILDER
    check_pins(OUT/'SOURCE-PINS.json')

def require_build_gate():
    assert OUT==ROOT/'PROEVEN/pad-lokaal-onbekend/20261023T155300-build','Exact reviewed output directory required'
    gate=json.loads((OUT/'ROOT-VRIJGAVE.json').read_text('utf-8'))
    assert gate['candidate_build_allowed'] is True,'Separate root C2 build release required'
    assert gate['reviewed_source_pins_sha256']==sha(OUT/'SOURCE-PINS.json'),'Gate must bind reviewed adapter pins'
    assert all(gate[name] is False for name in ('native_allowed','RPM_allowed','game_allowed','install_allowed'))

def load_recipe():
    # Run in a new interpreter so existing sys.modules cannot silently retain
    # the historical native/policy/Trace modules before local overrides load.
    assert not any(name in sys.modules for name in ('native','policy','path_diagnostic','path_diagnostic_layout','path_failure_decoder','x86','build')),'Fresh interpreter required'
    adapter=module('local4_C1_source_imports',C1/'source_imports.py')
    effective=adapter.load()
    parent=module('local4_historical_compose',PARENT/'build_candidate.py')
    assert parent.OUT==PARENT
    for attr,name in [('native','native'),('policy','policy'),('path_layout','path_diagnostic_layout')]:
        assert getattr(parent,attr) is effective[name],attr
    assert parent.policy.n is effective['native']
    assert sys.modules['path_diagnostic'].Trace is effective['native'].Trace
    return parent,effective

def bind_verify_base(parent):
    def verify_base():
        # Historical verify_base/main never runs and its true gate cannot
        # authorize this adapter. Parent OUT remains read-only input provenance.
        require_build_gate();verify_sources()
        prep=json.loads((PARENT/'preparation-manifest.json').read_text('utf-8'))
        for row in prep['release_pins']+prep['proposals']+prep['source_pins']:
            assert sha(ROOT/row['path'])==row['sha256'],row['path']
        assert sha(parent.C2_PROPOSAL)==parent.C2_PROPOSAL_SHA256
        original=(PARENT/'release-v1.robotcom.backup.dll').read_bytes()
        assert hashlib.sha256(original).hexdigest()==prep['base_sha256']
        assert sha(ROOT/'CTP-proef/ctp_program/ctp/civctp.exe')==prep['engine_sha256']
        assert (parent.native.PLAN_SIZE,parent.path_layout.PLAN_SIZE,parent.path_layout.GENERATION_OFFSET,parent.path_layout.RECORD_OFFSET,parent.path_layout.STATE_SIZE)==(0x79800,0x79800,0x79800,0x79804,0x79904)
        return original,prep
    parent.verify_base=verify_base

def effective_manifest(manifest,effective):
    extension=int(manifest['components']['extension_rva'],16)
    state=int(manifest['components']['state_rva'],16)
    labels=manifest['labels'];layout=effective['path_diagnostic_layout']
    assert extension+labels['pass_state']==state
    assert extension+labels['generation']==state+layout.GENERATION_OFFSET
    manifest['historical_composition_sources']=manifest.pop('sources')
    manifest['historical_source_dependency_pins']=manifest.pop('source_dependency_pins')
    manifest['historical_C1_source_pins_sha256']=manifest.pop('C1_source_pins_sha256')
    manifest['historical_proposal_sha256']=manifest.pop('proposal_sha256')
    manifest['historical_c2_proposal_sha256']=manifest.pop('c2_proposal_sha256')
    paths={name:Path(obj.__file__).resolve() for name,obj in effective.items()}
    paths.update(builder_adapter=Path(__file__).resolve(),historical_compose=PARENT/'build_candidate.py',historical_development=PARENT/'science_development.py',historical_food_components=PARENT/'food_components.py',historical_science_model=PARENT/'science_model.py',H3_builder=ROOT/'PROEVEN/production-h3/build-current.py',B2_builder=ROOT/'PROEVEN/opening-b2/build.py')
    paths.update(x86_emitter=Path(sys.modules['x86'].__file__).resolve(),recipe_base=Path(sys.modules['build'].__file__).resolve())
    manifest['effective_modules']={name:dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for name,p in sorted(paths.items())}
    manifest['sources']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size) for p in sorted(set(paths.values()))]
    manifest['source_dependency_pins']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in (C1/'SOURCE-PINS.json',OUT/'SOURCE-PINS.json')]
    manifest.update(stage='LOCAL_UNKNOWN4_C2_BUILT_NOT_NATIVE_NOT_HOST',proposal_sha256=sha(ROOT/'ONTWERP/PAD-LOKAAL-ONBEKEND-2026-10-22.md'),C1_source_pins_sha256=C1_PINS,adapter_source_pins_sha256=sha(OUT/'SOURCE-PINS.json'),parent_candidate_sha256=PARENT_DLL,parent_manifest_sha256=PARENT_MANIFEST)
    selected={name:extension+rva for name,rva in labels.items() if name in ('direct_path','cached_path','select_direct_plans','path_local_candidate','path_unknown','path_budget','path_free','path_done','source_path','source_next','source_choose','select_add','select_bad','select_ok') or name.startswith(('direct_pre','direct_post','cache_pre','cache_post','source_pre','source_post','selection_','pd_failure_'))}
    manifest['effective_local4_labels_rva']=selected
    diag=manifest['path_diagnostic']
    for row in diag['branches']:row['historical_parent_edge_rva']=row.pop('parent_rva')
    diag.update(parent_candidate_sha256=PARENT_DLL,parent_manifest_sha256=PARENT_MANIFEST,failure_latch='fixed single record; hard0/cache0/select0 or clean local4/cache4/select1; later-query combination UNKNOWN',local4_returnmask=layout.required_mask(4),local4_propagation=[4,4,1],record_is_policy_input=False)
    manifest['local_unknown4']=dict(native_EAX=0,capacity=0,count=0,pointer=0,precontext=0,postcontext=0,canaries=[0x3456ab89,0x4567bc90],executing_compareguards=True,return_code=4,cache_scope='same finalization only; START reset',selection_dispatch='1 credit;2/4 source_next;3 committed-prefix stop;0/other whole fallback',positive_best_snapshot='separate selection-frame snapshot rechecked before credit',policy_unchanged=True,state_rva=state,generation_rva=state+layout.GENERATION_OFFSET,state_size=layout.STATE_SIZE,Plan_size=layout.PLAN_SIZE,Trace_is_policy_input=False)
    return manifest

def compose():
    # Gate and exact pins precede all imports that can expose emission.
    require_build_gate();verify_sources()
    parent,effective=load_recipe();bind_verify_base(parent)
    data,code,manifest=parent.compose()
    return data,code,effective_manifest(manifest,effective)

def main():
    data,code,manifest=compose()
    # All outputs directly in this new package. Historical main is never used.
    for name,raw in [('U30-40.prepared.dll',data),('U30-40.payload.bin',code),('candidate-manifest.json',(json.dumps(manifest,indent=2)+'\n').encode())]:
        target=OUT/name
        assert not target.exists(),'Refuse overwrite: '+str(target)
    (OUT/'U30-40.prepared.dll').write_bytes(data)
    (OUT/'U30-40.payload.bin').write_bytes(code)
    (OUT/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')

if __name__=='__main__':main()
