"""Supplemental read-only file/block/binary audit; never a real parser/game test."""
import datetime
import hashlib
import json
import pathlib
import re
import struct
from zoneinfo import ZoneInfo

root = pathlib.Path(__file__).resolve().parents[2]
out = pathlib.Path(__file__).resolve().parent
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest().upper()
versions = []
for rel, expected in (
    ('ctp_program/ctp/civctp.exe', 'B1B5256FB0FB1A844548EB62E7B13D79A8B4F81B4499CFBE93E614BD5268AC79'),
    ('ctp_program/ctp/dll/ai/robotcom.dll', '3025070D66FBA516E4CDD70AE332055E1E4EF5162BF1B14C163B9BD128A35D44'),
):
    p = root / 'CTP-proef' / rel
    data = p.read_bytes()
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    assert digest(p) == expected
    assert data == (root / 'CTP-og' / rel).read_bytes()
    versions.append({'path': p.relative_to(root).as_posix(), 'sha256': digest(p),
                     'timestamp': hex(struct.unpack_from('<I', data, pe+8)[0]),
                     'imagebase': hex(struct.unpack_from('<I', data, pe+52)[0]),
                     'equal_OG_and_analyzed_binary': True})
saves = []
for rel in ('PROEVEN/settlerquota/vaste-start/QUOTA-START-T0.sav',
            'CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0'):
    p = root / rel
    assert digest(p) == '8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26'
    saves.append({'path': rel, 'sha256': digest(p)})
known = set(re.findall(rb'(?m)^\s*(ADVANCE_[A-Z0-9_]+)\s*\{',
                      (root / 'CTP-proef/ctp_data/default/gamedata/advance.txt').read_bytes()))
checks = []
for name in ('default', 'cleric', 'milmany', 'milfew', 'scimany', 'scifew', 'slaver', 'citywall_science'):
    before = (out / 'backup' / (name+'.aip')).read_bytes()
    after = (root / 'CTP-proef/ctp_data/default/aidata/AIPs' / (name+'.aip')).read_bytes()
    def split(data):
        # Earlier commented syntax examples precede the final real declaration.
        marker = data.rindex(b'Advancement_Element Advancements_List[MAX_ELEMENTS]')
        start = data.index(b'#DATA', marker)
        end = data.index(b'#END_DATA', start)
        return data[:start], data[start:end], data[end:]
    a, b, c = split(before)
    x, y, z = split(after)
    assert a == x and c == z
    old = re.findall(rb'"(ADVANCE_[A-Z0-9_]+)";', b)
    new = re.findall(rb'"(ADVANCE_[A-Z0-9_]+)";', y)
    assert len(old) == len(new) == 98
    assert new[:2] == [b'ADVANCE_RELIGION', b'ADVANCE_THEOCRACY']
    assert sorted(old) == sorted(new)
    assert [t for t in old if t not in new[:2]] == new[2:]
    assert set(new) <= known
    checks.append({'file': name+'.aip', 'outside_block_byte_equal': True,
                   'count_multiset_order_valid': True, 'all_tokens_resolve': True})
script = (root / 'CTP-proef/ctp_data/default/gamedata/script.slc').read_text(encoding='latin1')
assert not re.search(r'(?m)^\s*#include\s+["<]ai_queue_probe', script)
result = {'checked_at': datetime.datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(),
          'versions': versions, 'saves': saves, 'independent_block_checks': checks,
          'queue_probe_include_absent': True, 'actual_parser_test': False,
          'actual_runtime_activation': False,
          'audit_correction': 'Initial supplemental substring split selected a commented syntax example; final actual declaration used instead. An inline audit also had a native-shell quoting error; this file avoids command-line source quoting.'}
(out / 'version-save-audit.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'binaries': versions, 'T0_copies_verified': len(saves),
                  'independent_block_checks': len(checks), 'actual_parser_test': False,
                  'actual_runtime_activation': False}))
