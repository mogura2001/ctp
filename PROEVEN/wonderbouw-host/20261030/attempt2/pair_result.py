"""Finite report from the two frozen C3 snapshots; no process access."""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SRC = ROOT/'PROEVEN/wonderbouw-kans/20261029'
paths = [SRC/'inspection-20261030-attempt2.json', SRC/'after-n1-20261030-attempt2.json']
before, after = [json.loads(p.read_text('utf-8')) for p in paths]
assert before['stable_twice'] and after['stable_twice']
assert before['instance'] == after['instance']
assert before['binding'] == after['binding']

def cities(row):
    return row['wonder_build_evidence']['cities']

def nodes(city):
    return [(n['build_class'], n['type']) for n in city['real_queue']['nodes']]

rows = []
for b, a in zip(before['state']['civilizations'], after['state']['civilizations']):
    assert b['civ_id'] == a['civ_id']
    assert a['processed_round'] == b['processed_round'] + 1
    old = {c['full_engine_handle']: c for c in cities(b)}
    new = {c['full_engine_handle']: c for c in cities(a)}
    assert old.keys() <= new.keys()
    candidates = []
    changes = []
    for handle, c in old.items():
        d = new[handle]
        assert c['owner'] == d['owner'] == b['civ_id']
        assert c['ai_city_id'] == d['ai_city_id']
        item = {'handle': handle, 'ai_city_id': c['ai_city_id'], 'owner': c['owner'],
                'before_queue': nodes(c), 'after_queue': nodes(d),
                'before': c['wonder_build_chance'], 'after': d['wonder_build_chance']}
        if c['wonder_build_chance']['production_rank_buildtime_possible_after_normal_queue'] is True:
            candidates.append(item)
        if nodes(c) != nodes(d):
            changes.append(item)
    rows.append({'civ_id': b['civ_id'], 'civ_name': b['civ_name'],
                 'native_rounds': [b['processed_round'], a['processed_round']],
                 'city_counts': [len(old), len(new)],
                 'before_labyrinth': sum((9, 2) in nodes(c) for c in old.values()),
                 'after_labyrinth': sum((9, 2) in nodes(c) for c in new.values()),
                 'all_old_handles_preserved': True,
                 'chance_before': b['wonder_build_chance'],
                 'chance_after': a['wonder_build_chance'],
                 'future_candidates': candidates, 'changed_queue_types': changes})

result = {'sources': [{'path': str(p.relative_to(ROOT)).replace('\\', '/'),
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
          'instance_equal': True, 'binding_equal': True, 'stable_twice_both': True,
          'native_plus_one_all': True, 'actual_input_count': 1,
          'gui_dates': ['2700 BC', '2650 BC'], 'civilizations': rows,
          'new_labyrinth_queue_proven': any(r['after_labyrinth'] > r['before_labyrinth'] for r in rows),
          'city_status_corroboration': 'NOT_APPLICABLE_NO_NEW_LABYRINTH',
          'scheduler_timing_competition_admission_distinguished': False,
          'full_doel4_complete': False}
(HERE/'PAIR-RESULT.json').write_text(json.dumps(result, indent=2)+'\n', 'utf-8')
print(json.dumps({'native_plus_one_all': True,
                  'labyrinth_counts': [[r['civ_id'], r['before_labyrinth'], r['after_labyrinth']] for r in rows],
                  'candidate_count': sum(len(r['future_candidates']) for r in rows),
                  'queue_type_changes': sum(len(r['changed_queue_types']) for r in rows)}, indent=2))
