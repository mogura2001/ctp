"""Finite saved-byte evaluation of the completed candidate T100; no GUI/RPM."""
from pathlib import Path
import json,hashlib,datetime,subprocess
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
BASE=ROOT/'PROEVEN/uitbreiding-lang/20261022T122400';ARM=BASE/'U30-40';HOST=HERE/'U30-40'
FIN=ROOT/'PROEVEN/uitbreiding-lang/20261022T171500-afronding';OLD=ROOT/'PROEVEN/uitbreiding-lang/20261022T170400-herstel85'
AI='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
HELPER='8490f93842d4117222f5d850c6467799591c478482d32d2490c248f919957e47'
F9='f9b6099e7ef664581a25dcf1682c01657586b7c7bd1b2b2f815dcc49be1b0aa8'
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def relative(p):return Path(p).relative_to(ROOT).as_posix()
def binding(record,t,instance,run):
    return record['stable_twice'] is True and record['instance']==instance and record['run_id']==run and record['turn']==t and record['variant']=='U30-40' and record['binding']['ai_sha256']==AI and record['binding']['engine_sha256']=='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79' and record['binding']['manifest_sha256']=='5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152' and set(record['loaded_checks'])=={'headers_sections_sizes','all_three_scorecalls','payload_and_original_ranges','only_original_HIGHLOW_relocation_adjustment','all_five_B2_hooks','N30_payload_bound','new_payload_and_all_nine_windows_bound'} and all(x is True for x in record['loaded_checks'].values()) and [c['civ_id'] for c in record['state']['civilizations']]==list(range(2,9)) and all(c['processed_round']==t-1 for c in record['state']['civilizations'])
def main():
    py='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
    def limit():return json.loads(subprocess.run([py,str(ROOT/'PROEVEN/Controleer-Weekbudget.py'),'--thread','01a0f7b4-4751-7513-b510-3835ce43f47d'],capture_output=True,text=True).stdout)
    budget=limit()
    if budget['state']=='unknown':budget=limit()
    assert budget['state'] in ('ok','warn'),budget
    D=[read(ARM/f'T{t}.json') for t in range(101)];C0=read(BASE/'release-v1/T0.json');C100=read(BASE/'release-v1/T100.json');post=read(ARM/'T100-postsave.json')
    inst=D[0]['instance'];run=D[0]['run_id'];assert inst['pid']==40488 and inst['creationtime_filetime']==134371535950250712
    checks=[];steps=[];cities=[];native=[];shared=[];now=[]
    for t,d in enumerate(D):
        p=ARM/f'T{t}.json';assert binding(d,t,inst,run)
        checks.append(dict(turn=t,sha256=sha(p),exact=True))
        civs=d['state']['civilizations'];cities.append(dict(turn=t,per_civ=[c['city_count'] for c in civs],total=sum(c['city_count'] for c in civs)))
        native.append(dict(turn=t,per_civ=[dict(civ=c['civ_id'],desired=c.get('native_desired'),actual=c.get('native_actual'),deficit=c.get('native_supplemental_deficit'),type=c.get('loaded_settler_type'),type_binding=c.get('type_identity_source')) for c in civs]))
        if not t:continue
        tokpath=ARM/f'T{t}-consumed.json' if t<=84 else FIN/f'AFRONDING-T{t}-consumed.json'
        passpath=ARM/f'T{t}-pass.json' if t<=84 else FIN/f'AFRONDING-T{t}-pass.json'
        tok=read(tokpath);passed=read(passpath);log=ARM/f'T{t}-n.txt'
        assert passed['turn']==t and passed['one_n'] is True and passed['native_all_round_plus_one'] is True
        assert tok['turn']==t and tok['pid']==inst['pid'] and tok['creation_filetime']==inst['creationtime_filetime'] and tok['run_id']==run
        assert log.read_text('utf-8-sig').strip()=='Sent keys to probe game: n'
        assert all(c['processed_round']==p['processed_round']+1 for c,p in zip(civs,D[t-1]['state']['civilizations']))
        if t<=84:assert tok['previous_sha256']==sha(ARM/f'T{t-1}.json')
        else:
            assert passed['success'] is True and passed['pid']==inst['pid'] and passed['creation_filetime']==inst['creationtime_filetime'] and passed['run_id']==run
            assert passed['accepted_snapshot_sha256']==sha(p) and passed['token_sha256']==sha(tokpath) and passed['helper_sha256']==tok['helper_sha256']==HELPER
            assert tok['previous_snapshot_sha256']==sha(ARM/f'T{t-1}.json')
            if t>85:assert tok['previous_completion_pass_sha256']==sha(FIN/f'AFRONDING-T{t-1}-pass.json') and tok['previous_completion_token_sha256']==sha(FIN/f'AFRONDING-T{t-1}-consumed.json')
            else:assert tok['immediate85_recheck_sha256']==sha(ARM/'T84-afronding85-immediate.json')
        steps.append(dict(turn=t,token_path=relative(tokpath),token_sha256=sha(tokpath),pass_path=relative(passpath),pass_sha256=sha(passpath),n_log_sha256=sha(log),exact=True))
        s=d['state']['shared_last_pass'];e=s['selected_evidence']
        bound=e.get('status')=='CONSISTENT_LAST_PASS_SELECTION' and e.get('only_last_bound_civ_pass') is True and e.get('other_civs_certified') is False and e.get('civ')==s['civ'] and e.get('generation')==s['generation'] and s['civ'] in range(2,9) and s['context']==1 and s['context_error']==0
        selected=[]
        if bound:
            for q in e.get('selected',[]):
                sci=q.get('science',{});m=[x['margin_x2'] for x in sci.get('current_steps',[])]
                if sci.get('location')=='NOW' and len(m)==3 and all(x>0 for x in m):selected.append(dict(center=sci['center'],margins_x2=m,future_food_credit=sci['future_food_credit']))
        x={k:s[k] for k in ['civ','generation','status','reason','context','context_error','Dorig','Gcert','desired','remaining','classified','slots','path_queries','path_points','cutoff']}
        x.update(turn=t,selection_status=e.get('status'),selection_binding=bound,NOW=selected);shared.append(x)
        if selected:now.append(dict(turn=t,civ=s['civ'],generation=s['generation'],plans=selected))
    diff=[dict(civ=c['civ_id'],field=k) for a,c in zip(D[0]['state']['civilizations'],C0['state']['civilizations']) for k,v in c.items() if k not in ('ai_actor','effective_aip') and a.get(k)!=v]
    assert not diff and D[0]['state']['advance_count']==C0['state']['advance_count']
    assert binding(post,100,inst,run) and post['state']==D[-1]['state'] and post['binding']==D[-1]['binding']
    prechecks=[]
    for name in ['T84-preinput-recheck.json','T84-herstel85-immediate.json','T84-after-registration-helper-error.json','T84-afronding85-immediate.json']:
        p=ARM/name;x=read(p);assert binding(x,84,inst,run) and x['state']==D[84]['state'] and x['instance']==D[84]['instance']
        prechecks.append(dict(path=relative(p),sha256=sha(p),state_instance_round83_exact=True))
    failed=[ARM/'T85-consumed.json',OLD/'T85-recovery-consumed.json']
    assert read(failed[0])['previous_sha256']==sha(ARM/'T84.json')
    assert read(failed[1])['original_failed_token_sha256']==sha(failed[0])
    assert read(failed[1])['previous_sha256']==sha(ARM/'T84.json')
    incidents=[read(HOST/'INCIDENT-T85.json'),read(HOST/'INCIDENT-T85-REGISTRATION-HELPER.json')]
    assert incidents[1]['exception_type']=='System.ArgumentException' and incidents[1]['key_not_reached'] is True
    assert sha(HOST/'start.json')==F9 and read(HOST/'start.json')['n_consumed']==84
    markers=len(list(ARM.glob('T*-consumed.json')))+len(list(FIN.glob('AFRONDING-T*-consumed.json')))+len(list(OLD.glob('T85-recovery-consumed.json')))
    assert markers==102 and len(list(ARM.glob('T*-n.txt')))==100 and len(steps)==100
    pins=read(FIN/'SOURCE-PINS.json');bad=[x['path'] for x in pins['sources'] if sha(ROOT/x['path'])!=x['sha256']]
    assert len(pins['sources'])==217 and not bad and sha(FIN/'Afronding-85-100.ps1')==HELPER
    parent=(BASE/'Pass-Duur.ps1').read_text('utf-8');fin=(FIN/'Afronding-85-100.ps1').read_text('utf-8')
    def body(s,n):
        start=s.index('function '+n);return s[start:s.index('\n}',start)+2]
    guard_checks={n:body(parent,n)==body(fin,n) for n in ['Budget','OwnState','CheckSnapshot']}
    guard_checks['Key_poll']=parent[parent.index('$inputResult=& $tool -Action Key -Keys n'):parent.index('@{turn=$Turn;one_n=')]==fin[fin.index('$inputResult=& $tool -Action Key -Keys n'):fin.index('$pass=[ordered]@')]
    assert all(guard_checks.values())
    per=[]
    for i,z in enumerate(D[-1]['state']['civilizations']):
        values=[d['state']['civilizations'][i]['city_count'] for d in D];cc=C100['state']['civilizations'][i]
        per.append(dict(civ=i+2,name=z['civ_name'],control_T100=cc['city_count'],candidate_T100=z['city_count'],delta=z['city_count']-cc['city_count'],percent_delta=100*(z['city_count']/cc['city_count']-1),max_candidate_cities=max(values),first_observed_25_30_40={str(n):next((t for t,v in enumerate(values) if v>=n),None) for n in [25,30,40]},decreases=[dict(turn=t,before=values[t-1],after=values[t]) for t in range(1,101) if values[t]<values[t-1]],Religion=z['known']['Religion']['known'],Theocracy=z['known']['Theocracy']['known'],active_government=z['active_government'],requested_government=z['government_requested'],current_research=z['engine_current'],first_active_Theocracy=next((t for t,d in enumerate(D) if d['state']['civilizations'][i]['active_government']==3),None)))
    before=read(HOST/'before.json');close=read(HOST/'close.json');restore=read(HOST/'restore.json');restorechecks=[]
    for group in ['protected','extra_preserved_files']:
        for row in before[group]:
            p=ROOT/row['path'];backup=HOST/'backup'/row['path'];assert sha(p)==sha(backup)==row['sha256']
            restorechecks.append(dict(group=group,path=row['path'],sha256=row['sha256'],current_and_backup_exact=True))
    assert len(before['protected'])==29 and len(before['extra_preserved_files'])==14
    named=[]
    for label,folder,h in [('CONTROLE','release-v1','daf39c45af52e20f933da9a2f243110803d4662fd18594438141cea0cc176ea7'),('KANDIDAAT','U30-40','39e03b31e238d3ac9ad9e3b4463e3e8564583ba3f35d6871005a75f0ae04da61')]:
        p=ROOT/'CTP-proef/ctp_program/ctp/save/games/Julius'/('UITBREIDING-'+label+'-T100');copy=HERE/folder/p.name;assert sha(p)==sha(copy)==h
        named.append(dict(label=label,path=relative(p),hostcopy=relative(copy),sha256=h,both_exact=True))
    assert sha(ROOT/restore['autosave_archive'])==sha(HOST/'AUTOSAVE-after')=='35837f6542aa144ce05d5d46433f84e722bda72a6824c4d0f31f35eebf306cd0'
    gates=[]
    for p in [BASE/a/'ROOT-READER.json' for a in ['release-v1','U30-40']]+[HERE/a/'gate.json' for a in ['release-v1','U30-40']]+[OLD/'ROOT-RECOVERY.json',FIN/'ROOT-AFRONDING.json']:
        g=read(p);assert g['allowed'] is False and g.get('control_allowed',False) is False;gates.append(dict(path=relative(p),closed=True))
    assert close['all_civctp_count']==0 and close['exited'] is True and close['elapsed_seconds']<4500
    assert sha(ROOT/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll')=='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
    alias_removed=not (ROOT/'CTP-proef/ctp_program/ctp/save/games/Julius/000-U30-40-START-T0').exists();assert alias_removed
    earlier=ROOT/'PROEVEN/science-duurproef/20261022T114700/variant'
    early_equal=all(cities[t]['per_civ']==[c['city_count'] for c in read(earlier/f'T{t}.json')['state']['civilizations']] for t in range(27))
    exceptions=[dict(turn=x['turn'],**c) for x in native for c in x['per_civ'] if isinstance(c['desired'],(int,float)) and c['desired']!=5]
    report=dict(at_Europe_Amsterdam=datetime.datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(),status='COMPLETED_CANDIDATE_TRACE_POSITIVE_PAIRED_ENDPOINT_SIGNAL',budget=budget,instance=inst,run_id=run,snapshots101=checks,steps100=steps,control_T0_scalar_differences_excluding_two_pointers=diff,postsave_full_state_and_binding_equal=True,postsave_sha256=sha(ARM/'T100-postsave.json'),T84_preinput_rechecks=prechecks,incidents=incidents,failed_preinput_tokens=[dict(path=relative(p),sha256=sha(p)) for p in failed],actual_n_logs100=True,original_successful_tokens_passes84=True,completion_successful_tokens_passes16=True,markers=102,plain100_token_protocol=False,legacy_start_hash=F9,legacy_start_counter=84,completion_source_count217=True,completion_source_hash=sha(FIN/'SOURCE-PINS.json'),completion_helper_hash=HELPER,completion_source_deviations=bad,preserved_parent_guards=guard_checks,root_completion_review=read(FIN/'ROOT-REVIEW.json'),per_civ=per,candidate_trajectories101=cities,candidate_first27_cities_match_confirmation=early_equal,control_only_manual_T0_T100=True,control_total=86,candidate_total=121,delta=35,percent_delta=100*35/86,candidate_T26_all7_active3=all(c['active_government']==3 for c in D[26]['state']['civilizations']),T100_all7_Religion_Theocracy_active3=all(x['Religion'] and x['Theocracy'] and x['active_government']==3 for x in per),native_per_civ=native,native_desired_not5_when_numeric=exceptions,shared_last_passes=shared,positive_bound_NOW=now,positive_NOW_passes=len(now),positive_NOW_plans=sum(len(x['plans']) for x in now),observed_shared_desired_above_Dorig=any(x['desired']>x['Dorig'] for x in shared),shared_unknown_civ_or_context_turns=[x['turn'] for x in shared if x['civ'] not in range(2,9) or x['context']!=1],generation_never_assumed_7_times_T=True,named_saves=named,save_dialog=dict(path=relative(HOST/'save-dialog.png'),sha256=sha(HOST/'save-dialog.png'),graph_turn100_visually_observed=True),restoration43=restorechecks,close=close,restore=restore,relevant_gates=gates,alias_removed=alias_removed,new14th_autosave_sha256=restore['autosave_after_sha256'],release_DLL_hash=restore['release_dll_sha256'],ENDPOINT_first30_not_reached_claim_independently_confirmed=all(x['max_candidate_cities']<30 for x in per),limits=['Control has endpoints only: no historical T26 splice, pairedT25/T50, exactfirst30/40, or never30>100 inference.','Citypossession is not own or useful founding; no fullqueues/laborer proof.','Gcert/Dorig only actual boundlastciv/generation; civ4native6 has no per-civGcert/Dorig attribution. UNKNOWNtype is not numeric demand.','T46..63 civ0/context0/reason35 zeroheaders are UNKNOWN, not measured settlerbraking.','One fixedmap/combination comparison, no general or direct causal driver proved.','Two provenpreinputstops retained; legacy84 counter stale; no flawless100token claim.','Reader save_identity_proven and atomic_snapshot_proven remainFalse; autosave not exactT100 by claim.'],acceptance=dict(endpoint_expansion=True,all7_T100_better=True,candidate_complete_trace=True,original_plain100_protocol=False,goal1=False,goal1a=False,goal5=False),next_finite_A_question='Could equal TOTAL desired allocate priorities differently because the quota adapter gives D-W to the first t-class and0 to later classes? Locate existing nativeDesired entries/consumer priorities. Hypothesis only; no new long run or proven driver.')
    assert [x['candidate_T100'] for x in per]==[17,20,17,12,20,21,14] and [x['control_T100'] for x in per]==[14,14,15,4,13,14,12]
    assert all(x['delta']>0 for x in per) and report['T100_all7_Religion_Theocracy_active3'] and report['ENDPOINT_first30_not_reached_claim_independently_confirmed']
    reportpath=HERE/'VERGELIJKING.json';assert not reportpath.exists();reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    proof=dict(status='T100_CANDIDATE_COMPLETE_TWO_PREINPUT_STOPS_CLOSED_RESTORED',comparison_path=relative(reportpath),comparison_sha256=sha(reportpath),at_Europe_Amsterdam=report['at_Europe_Amsterdam'],instance=inst,snapshots=101,postsave_full_state_equal=True,natural_steps=100,actual_successful_n_logs=100,original_successful_tokens_passes=84,completion_tokens_passes=16,failed_preinput_tokens=report['failed_preinput_tokens'],markers=102,plain100_token_protocol=False,legacy_counter84=True,legacy_hash=F9,all_four_T84_rechecks_exact=True,old_nonIO_failure_beforeKey=True,completion_source217_exact=True,helper_hash=HELPER,candidate_cities=[x['candidate_T100'] for x in per],control_cities=[x['control_T100'] for x in per],candidate_total=121,control_total=86,delta=35,percent_delta=100*35/86,all7_Theocracy=True,named_saves=named,postsave_sha256=report['postsave_sha256'],save_dialog_sha256=sha(HOST/'save-dialog.png'),close=close,restore=restore,restored29_and14extra_exact=True,new14th_autosave_double_exact=True,relevant_gates_closed=True,alias_removed=True,current_release_DLL=restore['release_dll_sha256'],goal1_1a_full5_complete=False,pc_shutdown=False)
    proofpath=HOST/'HOST-PROOF.json';assert not proofpath.exists();proofpath.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(dict(report_sha256=sha(reportpath),proof_sha256=sha(proofpath),per_civ=per,NOW_passes=len(now),NOW_plans=report['positive_NOW_plans'],native_exceptions=exceptions,budget=budget,at=report['at_Europe_Amsterdam']),ensure_ascii=True))
if __name__=='__main__':main()
