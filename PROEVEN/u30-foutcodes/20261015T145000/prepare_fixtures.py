"""Narrow reuse of existing C2 owned-memory compiled fixture, no live host."""
from pathlib import Path
import difflib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];OLD=ROOT/'PROEVEN/uitbreiding-30-40/20261012T181500/c2';DEST=OUT/'c2';DEST.mkdir(exist_ok=True)
(DEST/'helper').mkdir(exist_ok=True)
for p in (OLD/'helper').iterdir():
 if p.suffix in ('.bin','.json'):(DEST/'helper'/p.name).write_bytes(p.read_bytes())
s=(OLD/'NativeU40.cs').read_text('utf-8')
start=s.index(' static void ChangedCases(){');end=s.index(' static void IntegratedChain(){',start)
s=s[:start]+''' static void ChangedCases(){
  byte[] guard=Read(Entry("bind_inputs"),5);
  byte[] changed=Read(Entry("bind_host"),labels["bind_inputs"]-labels["bind_host"]);
  byte[] finalize=Read(Entry("finalize_pass"),labels["start_hook"]-labels["finalize_pass"]);
  ResetPlan();W(plan,36,0);Test("early scope remains44",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,4)==44&&R(plan,0)==0);
  ResetPlan();W(plan,8,0);Test("early read_policy remains44",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,4)==44&&R(plan,0)==0);
  ResetPlan();W(planner,0xa28,0);Test("host actual guard30 survives finalize",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,4)==30&&R(plan,0)==0&&R(plan,212)==0);W(planner,0xa28,ai.ToInt32());
  Patch(Entry("bind_inputs"),5);Marshal.Copy(guard,0,Entry("bind_inputs"),5);
  ResetPlan();Test("actual bind_inputs36 survives host",Call("bind_host",0,true,plan.ToInt32())==0&&R(plan,4)==36&&R(plan,0)==0);
  ResetPlan();Test("actual bind_inputs36 survives host and finalize",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,4)==36&&R(plan,0)==0&&R(plan,212)==0);
  Dependency("bind_inputs","true4");
  ResetPlan();W(state,52,0);Test("resolve_type actual guard10 survives finalize",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,4)==10&&R(plan,0)==0&&R(plan,212)==0);W(state,52,3);
  ResetPlan();W(Aip(),0x7b0,-1);Test("preview actual guard11 survives finalize",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,4)==11&&R(plan,0)==0&&R(plan,212)==0);W(Aip(),0x7b0,4);
  IntPtr classes=new IntPtr(R(new IntPtr(R(Aip(),0x7bc)),0));IntPtr first=new IntPtr(R(new IntPtr(R(classes,12)),0));D(first,0,2);PolicyState(2147483647,0,0);
  ResetPlan();Test("original_demand actual guard40 survives finalize",Call("finalize_pass",0,false,plan.ToInt32())==0&&R(plan,4)==40&&R(plan,0)==0&&R(plan,212)==0);D(first,0,-2);PolicyState(1,0,0);
  PolicyState(1,0,0);W(city,0x1f0,1);Pipeline(6,true);Test("existing success Dorig2 Gcert6 desired6 context1 status5",R(plan,184)==2&&R(plan,188)==6&&Wanted()==6&&R(Priority(1),0)==6&&R(ActualArray(),4)==2&&R(plan,64)==6&&R(plan,212)==1&&R(plan,0)==5&&R(plan,8)==0&&R(plan,36)==0);
  Test("changed host bytes intact",Same(changed,Read(Entry("bind_host"),changed.Length)));
  Test("changed finalize bytes intact",Same(finalize,Read(Entry("finalize_pass"),finalize.Length)));
 }
'''+s[end:]
s=s.replace('RX(image,labels["pass_state"]);Dependency("bind_inputs","true4");','RX(image,labels["pass_state"]);')
s=s.replace('   IntegratedChain();\n   Test("all actual changed emitted functions byte-intact"','   ChangedCases();\n   Test("all actual changed emitted functions byte-intact"')
(DEST/'NativeU40.cs').write_text(s,'utf-8')
ps=(OLD/'native-policy.ps1').read_text('utf-8');(DEST/'native-policy.ps1').write_text(ps.replace("'r3'","'r4'"),'utf-8')
run=(OLD/'run-policy.py').read_text('utf-8').replace('f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810',json.loads((OUT/'candidate-manifest.json').read_text())['candidate_sha256'])
(DEST/'run-policy.py').write_text(run.replace('-r3','-r4'),'utf-8')
for n in ['NativeU40.cs','native-policy.ps1','run-policy.py']:
 (DEST/(n+'.source-diff.txt')).write_text(''.join(difflib.unified_diff((OLD/n).read_text('utf-8').splitlines(True),(DEST/n).read_text('utf-8').splitlines(True),fromfile='existing-C2/'+n,tofile='own-limited-C2/'+n)),'utf-8')
print('Reused C2 fixture; 8 fault calls + existing success pipeline only; no host/game.')
