"""Freeze separate C2/source/runtime inputs, never alter historical C1 pins."""
from pathlib import Path
import ast,difflib,hashlib,json,datetime
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size)
def write(p,value):p.write_text(json.dumps(value,indent=2)+'\n','utf-8')
def main():
 c1=OUT/'SOURCE-PINS.json';assert sha(c1)=='be973e49133a516d64327764602050e1426e4d721ef5397775404e239d24dd74'
 old=json.loads(c1.read_text('utf-8'))['sources']
 for row in old:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 for path in OUT.rglob('*.py'):ast.parse(path.read_text('utf-8'))
 a=OUT/'native/NativeFoodCaller.cs';b=OUT/'native-v2/NativeFoodCaller.cs'
 (OUT/'diffs/native-v2-C2.diff').write_text(''.join(difflib.unified_diff(a.read_text('utf-8').splitlines(True),b.read_text('utf-8').splitlines(True),fromfile=a.relative_to(ROOT).as_posix(),tofile=b.relative_to(ROOT).as_posix())),'utf-8')
 paths={ROOT/row['path'] for row in old}|{c1}
 paths.update(OUT/n for n in ['candidate-manifest.json','U30-40.prepared.dll','U30-40.payload.bin','observer_sources_C2.py','check_candidate_C2.py','pin_C2.py','candidate-static-checks-C2.json','recipe-edits-C2.json','C2-OVERDRACHT.md','reader/runtime-pins.json','reader/READER-PINS.json'])
 paths.update(p for p in (OUT/'fixture').iterdir() if p.is_file())
 paths.update(OUT/'native-v2'/n for n in ['NativeFoodCaller.cs','compile-helper.ps1','native-caller.ps1'])
 paths.add(OUT/'diffs/native-v2-C2.diff')
 paths.add(ROOT/'PROEVEN/science-foodreader-host/20261019/host1/variant/T1.json')
 paths.update((OUT/'reader/candidate'/arm/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll') for arm in ['variant','baseline'])
 candidate=sha(OUT/'U30-40.prepared.dll');manifest=sha(OUT/'candidate-manifest.json')
 data=dict(stage='C2_CANDIDATE_STATIC_ONLY_NOT_NATIVE_NOT_HOST',time_amsterdam=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).isoformat(),candidate_sha256=candidate,manifest_sha256=manifest,C1_source_pins_sha256=sha(c1),sources=[pin(p) for p in sorted(paths)],native_compiled=False,native_run=False,installed=False)
 write(OUT/'BUILD-PINS.C2.json',data)
 native=dict(data);native['stage']='C2_NATIVE_V2_SOURCE_ONLY_SEPARATE_REVIEW_REQUIRED';native['sources']=data['sources']+[pin(OUT/'BUILD-PINS.C2.json')]
 write(OUT/'native-v2/NATIVE-SOURCE-PINS.json',native)
 write(OUT/'native-v2/NATIVE-ROOT-REVIEW.json',dict(stage='SOURCE_ONLY_AWAIT_ROOT_REVIEW',compilation_allowed=False,native_allowed=False,host_allowed=False,candidate_sha256=candidate,manifest_sha256=manifest,source_pins_sha256=sha(OUT/'native-v2/NATIVE-SOURCE-PINS.json'),compiled_assembly_sha256=None))
 print(json.dumps(dict(candidate=candidate,manifest=manifest,C2_build_pins=sha(OUT/'BUILD-PINS.C2.json'),C2_build_files=len(data['sources']),native_source_pins=sha(OUT/'native-v2/NATIVE-SOURCE-PINS.json'),native_files=len(native['sources']))))
if __name__=='__main__':main()
