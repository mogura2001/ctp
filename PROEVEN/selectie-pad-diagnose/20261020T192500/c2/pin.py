"""Separate C2/static/native source pins. Historical C1 pins never rewritten."""
from pathlib import Path
from zoneinfo import ZoneInfo
import ast,datetime,difflib,hashlib,json
OUT=Path(__file__).resolve().parent.parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n','utf-8')
def pin(path):return dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path),size=path.stat().st_size)
def main():
 c1=OUT/'SOURCE-PINS.json';assert sha(c1)=='75244d1e104095f12204c3b67c03ad42ecf329c088fc795391b6880cf7394c37'
 previous=json.loads(c1.read_text('utf-8'))['sources']
 for row in previous:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 for path in OUT.rglob('*.py'):ast.parse(path.read_text('utf-8'))
 a=(OUT/'native/NativePathLoggerCaller.cs').read_text('utf-8');b=(OUT/'native-v2/NativePathLoggerCaller.cs').read_text('utf-8')
 expected=a.replace('[DllImport("kernel32.dll")]static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint f,out uint old);','[DllImport("kernel32.dll")]static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint f,out uint old);\n [DllImport("kernel32.dll")]static extern bool FlushInstructionCache(IntPtr process,IntPtr address,UIntPtr size);').replace('Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"own RX");','Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"own RX");Check(FlushInstructionCache(new IntPtr(-1),p,(UIntPtr)n),"flush exact own RX range");')
 assert expected==b,'native-v2 differs beyond exact ownrange cacheflush'
 (OUT/'diffs/native-v2-C2.diff').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='C1/native/NativePathLoggerCaller.cs',tofile='C2/native-v2/NativePathLoggerCaller.cs')),'utf-8')
 manifest=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'))
 paths={ROOT/row['path'] for row in previous}|{c1}
 paths|={OUT/name for name in ['U30-40.prepared.dll','U30-40.payload.bin','candidate-manifest.json','reader/runtime-pins.json','reader/READER-PINS.json','C2-OVERDRACHT.md','diffs/native-v2-C2.diff']}
 paths|={path for path in (OUT/'c2').iterdir() if path.is_file()}
 paths|={path for path in (OUT/'fixture').iterdir() if path.is_file()}
 paths|={OUT/'native-v2'/name for name in ['NativePathLoggerCaller.cs','compile-helper.ps1','native-caller.ps1']}
 paths|={OUT/'reader/candidate'/arm/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll' for arm in ('variant','baseline')}
 paths.add(ROOT/'PROEVEN/science-bezet-centrum-host/20261020/host1/variant/T1.json')
 data=dict(stage='C2_STATIC_CANDIDATE_NO_NATIVE_NO_HOST',time_amsterdam=datetime.datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(),candidate_sha256=sha(OUT/'U30-40.prepared.dll'),manifest_sha256=sha(OUT/'candidate-manifest.json'),C1_source_pins_sha256=sha(c1),sources=[pin(path) for path in sorted(paths)],native_compiled=False,native_run=False,installed=False)
 write(OUT/'BUILD-PINS.C2.json',data)
 native=dict(data);native.update(stage='C2_NATIVE_LOGGER_SOURCE_ONLY_AWAIT_SEPARATE_REVIEW',sources=data['sources']+[pin(OUT/'BUILD-PINS.C2.json')])
 write(OUT/'native-v2/NATIVE-SOURCE-PINS.json',native)
 write(OUT/'native-v2/NATIVE-ROOT-REVIEW.json',dict(stage='SOURCE_ONLY_NO_COMPILE_RUN_RELEASE',compilation_allowed=False,native_allowed=False,host_allowed=False,candidate_sha256=data['candidate_sha256'],manifest_sha256=data['manifest_sha256'],fixture_sha256=sha(OUT/'fixture/logger.bin'),fixture_recipe_sha256=sha(OUT/'fixture/logger.recipe.json'),source_pins_sha256=sha(OUT/'native-v2/NATIVE-SOURCE-PINS.json'),compiled_assembly_sha256=None))
 print(json.dumps(dict(candidate=data['candidate_sha256'],manifest=data['manifest_sha256'],C2_build_pins=sha(OUT/'BUILD-PINS.C2.json'),C2_build_files=len(data['sources']),native_source_pins=sha(OUT/'native-v2/NATIVE-SOURCE-PINS.json'),native_files=len(native['sources']),fixture_sha256=sha(OUT/'fixture/logger.bin'),fixture_recipe_sha256=sha(OUT/'fixture/logger.recipe.json'))))
if __name__=='__main__':main()
