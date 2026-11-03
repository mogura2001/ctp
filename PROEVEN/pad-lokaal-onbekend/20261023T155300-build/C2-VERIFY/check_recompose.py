"""Exactly one second in-memory compose in a fresh interpreter; no main."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;PACK=OUT.parent
sha=lambda b:hashlib.sha256(b).hexdigest()

def main():
    result=OUT/'DETERMINISM.json'
    assert not result.exists(),'Do not repeat the authorized second compose'
    spec=importlib.util.spec_from_file_location('local4_build_verification',PACK/'build_candidate.py')
    builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    # This is the only compose invocation in C2-VERIFY. The approved own gate
    # and all immutable source pins are checked again by the adapter itself.
    data,code,manifest=builder.compose()
    saved_data=(PACK/'U30-40.prepared.dll').read_bytes()
    saved_code=(PACK/'U30-40.payload.bin').read_bytes()
    saved_manifest=json.loads((PACK/'candidate-manifest.json').read_text('utf-8'))
    checks=dict(candidate=data==saved_data,payload=code==saved_code,manifest_object=manifest==saved_manifest,manifest_serialized=(json.dumps(manifest,indent=2)+'\n').encode()==(PACK/'candidate-manifest.json').read_bytes())
    report=dict(stage='C2B_SECOND_COMPOSE_ONLY_NOT_NATIVE',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,candidate_sha256=sha(data),payload_sha256=sha(code),manifest_sha256=sha((json.dumps(manifest,indent=2)+'\n').encode()),candidate_size=len(data),payload_size=len(code),compose_calls=1,historical_main_called=False,outputs_overwritten=False,native=False,RPM=False,game=False,install=False,pass_all=all(checks.values()))
    result.write_text(json.dumps(report,indent=2)+'\n','utf-8')
    assert report['pass_all'],checks
    print(json.dumps(report))

if __name__=='__main__':main()
