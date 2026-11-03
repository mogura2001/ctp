"""Pure owned-byte evidence cases; never open or write any game process."""
from pathlib import Path
import copy, hashlib, json, struct, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / 'PROEVEN/u30-science-filter/20261017T124500'
sys.path[:0] = [str(PACK), str(PACK / 'reader')]
from plan_layout import COUNTERS, STATE_SIZE
from positive_reader import selected_evidence

def fixture():
    raw = bytearray(STATE_SIZE)
    def put(off, fmt, *values): struct.pack_into(fmt, raw, off, *values)
    def key(off, x): put(off, '<hhhH', x, 2, 0, 0)
    put(0x78800, '<II', 0x1234, 7)
    put(0x52600, '<I', 0)
    slot = 0x40600
    for off, value in ((28, 4), (72, 2), (76, 0), (80, 1)):
        put(slot + off, '<i', value)
    key(slot + 8, 2)
    for n in range(4): key(slot + 32 + n * 8, 2 + n)
    sci = 0x54800
    for off, value in ((0, 2), (4, 0), (8, 1), (12, 3), (16, 3),
                       (28, 0), (32, 1), (36, 2), (56, 0), (112, 1)):
        put(sci + off, '<i', value)
    put(sci + 64, '<d', 1.0)
    for off, value in ((72, 10), (80, 40), (88, 20), (96, 20), (104, 80)):
        put(sci + off, '<q', value)
    key(sci + 116, 2)
    for n in range(3):
        tile = sci + 128 + n * 96
        key(tile, n + 3)
        for off, value in ((16, 10), (20, 24), (24, 1)):
            put(tile + off, '<i', value)
    shared = dict(civ=8, generation=7, context=1, reason=0, status=5,
                  context_error=0, owner=0, prefix_count=1, known_count=1,
                  candidates=1, gate_queries=1, gate_false=0,
                  science_budget_exhausted=0, Gcert=1, slots=1)
    shared.update({'SCI_' + name: 0 for name in COUNTERS})
    return raw, shared

cases = []
def check(name, mutate=None, accepted=False):
    raw, shared = fixture()
    if mutate: mutate(raw, shared)
    reads = []
    def read(off, size):
        assert 0 <= off < off + size <= STATE_SIZE and size <= 8192
        reads.append([off, size])
        return bytes(raw[off:off + size])
    result = selected_evidence(read, shared, [2, 3, 4, 5, 6, 7, 8])
    good = result['status'] == 'CONSISTENT_LAST_PASS_SELECTION'
    assert good == accepted, (name, result)
    if accepted and shared['Gcert']:
        assert result['science_selected'] == 1
        assert result['selected'][0]['science']['future_food_credit'] is False
    cases.append(dict(name=name, accepted=good, status=result['status'],
                      reason=result.get('reason'), bounded_reads=reads))

def word(off, value, fmt='<i'):
    return lambda raw, shared: struct.pack_into(fmt, raw, off, value)
check('current NOW science, three real foodkeys, positive n1/2/3', accepted=True)
check('prefix cutoff does not invalidate completed science evidence',
      lambda r, s: s.update(science_budget_exhausted=1, cutoff=1), accepted=True)
check('empty certified selection is no positive science claim',
      lambda r, s: s.update(Gcert=0, slots=0), accepted=True)
check('selected slot outside bounded slots', word(0x52600, 1))
check('result index is slot76, never alternative index80', word(0x40600 + 76, 1))
check('alternative index must equal role minus one', word(0x40600 + 80, 0))
check('duplicate mandatory key', word(0x40600 + 48, 3, '<h'))
check('coverage incomplete', word(0x54800 + 112, 0))
check('future-only food flags cannot certify NOW', word(0x54800 + 128 + 20, 16))
check('raw spatial false cannot certify foodkey', word(0x54800 + 128 + 24, 0))
check('unbound model', word(0x54800 + 8, 0))
check('current negative food', word(0x54800 + 128 + 16, -1))
check('raw current summary mismatch', word(0x54800 + 88, 21, '<q'))
check('nonfinite actual rations', word(0x54800 + 64, float('nan'), '<d'))
check('generation mismatch', word(0x78804, 6, '<I'))
check('callback context error', lambda r, s: s.update(context_error=1))
check('prefix accounting mismatch', lambda r, s: s.update(gate_false=1))
check('Gcert cannot exceed available slots', lambda r, s: s.update(Gcert=2))
result = dict(scope='PURE_OWN_BYTES_NO_EMITTER_NATIVE_RPM_GAME',
              reader_sha256=hashlib.sha256((PACK / 'reader/positive_reader.py').read_bytes()).hexdigest(),
              cases=cases, count=len(cases), passed=True,
              native_cases_tested=False, gameplay_acceptance=False)
out = ROOT / 'PROEVEN/u30-science-filter/reader-evidence-checks.json'
out.write_text(json.dumps(result, indent=2) + '\n', 'utf-8')
print(json.dumps(dict(cases=len(cases), passed=True, native=False, gameplay=False)))
