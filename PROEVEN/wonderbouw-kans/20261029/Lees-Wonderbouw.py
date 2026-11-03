"""Small read-only composition of the frozen wonderbewijs reader."""
from pathlib import Path
import hashlib, importlib.util, json, math, struct, sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT/'PROEVEN/wonderbewijs/20261029'

def pins():
    manifest = json.loads((HERE/'pins.json').read_text('utf-8'))
    for item in manifest['files']:
        if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Wonderbouw source pin changed: '+item['path'])

def predicates(city, keys, cost, threshold, maxrounds):
    production, stock, key = city['production'], city['stock'], city['key']
    low = sum(k < key for k in keys)
    high = sum(k <= key for k in keys)-1
    if not keys or key not in keys:
        raise ValueError('City absent from complete own key set')
    rank = True if low/len(keys) >= threshold else False if high/len(keys) < threshold else 'UNKNOWN_TIE_AT_THRESHOLD'
    stored = stock >= 500 and production >= 30 and math.trunc(stock/production) >= 5
    rounds = math.trunc((cost+0.5-stock)/production) if production >= 1 else math.trunc(cost+0.5)
    if not -(1<<31) <= rounds < (1<<31):
        raise ValueError('AI build-time truncation outside signed32 domain')
    time_ok = rounds <= maxrounds
    rank_gate = True if stored else rank
    cache_free = city['incumbent'] < 0 and city['flag'] == 0
    possible = False if rank_gate is False or not time_ok else True if rank_gate is True else 'UNKNOWN_TIE_AT_THRESHOLD'
    now = False if not cache_free else possible
    return dict(rank_min=low, rank_max=high, own_city_count=len(keys), rank_denominator='N',
        rank_threshold_pass=rank, stored_production_exception=stored,
        ai_build_rounds=rounds, build_rounds_pass=time_ok, cache_free_now=cache_free,
        ai_predicates_now=now, production_rank_buildtime_possible_after_normal_queue=possible,
        future_cache_release='UNKNOWN', engine_admission='UNKNOWN')

def chances(read, state, reader):
    read = reader.bounded(read)
    def u(p): return struct.unpack('<I',read(reader.checked(p),4))[0]
    def i(p): return struct.unpack('<i',read(reader.checked(p),4))[0]
    def d(p):
        value = struct.unpack('<d',read(reader.checked(p),8))[0]
        if not math.isfinite(value): raise ValueError('Nonfinite AI cost/threshold')
        return value
    engine_cost = i(int(state['wonder_native_identity']['wonder_record'],16)+0x38)
    for row in state['civilizations']:
        actor = int(row['ai_actor'],16)
        aip = reader.checked(u(actor+0x94),0x20)
        if u(aip+0x800) != actor: raise ValueError('Wonderbouw AIP owner mismatch')
        threshold, maxrounds = d(aip+0x250), i(aip+0x734)
        table = u(actor+0x124)
        record = reader.checked(u(table+8),72*2)
        cost, wonder_state = d(record+8), i(record+0x20)
        cities = row['wonder_build_evidence']['cities']
        decoded = []
        for city in cities:
            agent = int(city['ai_city_agent'],16)
            raw = dict(production=i(agent+0x38),stock=i(agent+0x28),key=i(agent+0x2c),
                       incumbent=i(agent+0x1f0),flag=i(agent+0x1f8))
            decoded.append((city,raw))
        keys = [raw['key'] for city,raw in decoded]
        for city,raw in decoded:
            city['wonder_build_chance'] = dict(raw, **predicates(raw,keys,cost,threshold,maxrounds),
                real_queue_empty_now=city['real_queue']['count']==0,
                native_owner_handle_reused=True)
        row['wonder_build_chance'] = dict(ai_cost_double=cost,ai_wonder_state=wonder_state,
            ai_wonder_record=hex(record),threshold=threshold,maxrounds=maxrounds,
            engine_wonder_record_cost_raw=engine_cost,deity_queue_cost='UNKNOWN',
            admission='UNKNOWN', one_builder_guaranteed=False)
    return state

def load_base():
    name='_ctp_wonderbouw_20261029_frozen_c2'
    if name in sys.modules: raise ValueError('Wonderbouw module name occupied')
    spec=importlib.util.spec_from_file_location(name,BASE/'Lees-Wonderbewijs.py')
    base=importlib.util.module_from_spec(spec);sys.modules[name]=base;spec.loader.exec_module(base)
    return base

def main():
    if not any(a in sys.argv for a in ('-h','--help')): pins()
    base=load_base()
    original_compose=base.compose_reader
    def compose(load):
        reader,source=original_compose(load)
        reader.FOLDER=HERE
        old_observe,old_binding=reader.observe_goal3,reader.trusted_binding
        reader.observe_goal3=lambda read,eb,ab,participants: chances(read,old_observe(read,eb,ab,participants),reader)
        def binding(variant):
            result=old_binding(variant)
            extra=json.loads((HERE/'binding-windows.json').read_text('utf-8'))
            result['ranges'].extend(extra['ranges'])
            return result
        reader.trusted_binding=binding
        return reader,source
    base.compose_reader=compose
    base.main()

if __name__=='__main__': main()
