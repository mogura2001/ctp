"""Apply/verify/restore only the approved eight AIP record moves, with byte backups."""
import argparse
import collections
import datetime
import difflib
import hashlib
import json
import pathlib
import re
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
NAMES = ('default', 'cleric', 'milmany', 'milfew', 'scimany', 'scifew', 'slaver', 'citywall_science')
REL = pathlib.Path('ctp_data/default/aidata/AIPs')
EXPECTED = ((7,97),(2,1),(7,97),(12,98),(15,96),(7,97),(13,19),(7,97))
DESIGN = '64DA8067A92D83A32B4234DE1D55B3A80DBCEE838E4585B5AF8066170F4DC19E'
TECHS = (b'ADVANCE_RELIGION', b'ADVANCE_THEOCRACY')
SHA = lambda data: hashlib.sha256(data).hexdigest().upper()

def stamp():
    return datetime.datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat()

def write_json(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def inventory():
    """All AI/rule files, executable/DLL/map files, profiles and existing saves in three copies."""
    found = {}
    for copy in ('CTP-proef','CTP-og','CTP-AAIP'):
        base = ROOT / copy
        files = set()
        for folder in ('ctp_data/default/aidata','ctp_data/default/gamedata','ctp_program/ctp/save'):
            files.update(p for p in (base/folder).rglob('*') if p.is_file())
        program = base/'ctp_program'
        files.update(p for p in program.rglob('*') if p.is_file() and
                     (p.suffix.lower() in ('.dll','.exe','.map') or p.name.lower()=='userprofile.txt'))
        for p in sorted(files):
            found[p.relative_to(ROOT).as_posix()] = SHA(p.read_bytes())
    return found

def parts(data):
    blocks = list(re.finditer(rb'Advancement_Element\s+Advancements_List\[MAX_ELEMENTS\];[^\r\n]*\r\n#DATA[^\r\n]*\r\n(.*?)#END_DATA', data, re.S))
    assert len(blocks)==1, 'Expected exactly one advance block'
    block = blocks[0]
    body = block.group(1)
    records = list(re.finditer(rb'^[ \t]*"(ADVANCE_[A-Z0-9_]+)";[^\r\n]*\r\n', body, re.M))
    assert records and all(body[a.end():b.start()]==b'' for a,b in zip(records,records[1:])), 'Non-contiguous records need review'
    tokens = [m.group(1) for m in records]
    assert all(tokens.count(t)==1 for t in TECHS), 'Research token count differs'
    return block, body, records, tokens

def transform(data):
    block,body,records,tokens = parts(data)
    lines = {m.group(1):m.group(0) for m in records if m.group(1) in TECHS}
    moved = b''.join(lines[t] for t in TECHS) + b''.join(m.group(0) for m in records if m.group(1) not in TECHS)
    new_body = body[:records[0].start()] + moved + body[records[-1].end():]
    result = data[:block.start(1)] + new_body + data[block.end(1):]
    _,_,_,new_tokens=parts(result)
    assert new_tokens[:2]==list(TECHS)
    assert new_tokens[2:]==[t for t in tokens if t not in TECHS]
    assert collections.Counter(tokens)==collections.Counter(new_tokens)
    assert len(result)==len(data)
    assert result.count(b'\r\n')==data.count(b'\r\n')
    return result

def targets():
    return [(ROOT/'CTP-proef'/REL/(n+'.aip'),OUT/'backup'/(n+'.aip')) for n in NAMES]

def prepare():
    assert not (OUT/'manifest.json').exists(), 'Existing B1 manifest: do not overwrite'
    assert SHA((ROOT/'ONTWERP/EERSTE-WIJZIGING.md').read_bytes())==DESIGN
    before=inventory()
    items=[]
    for (p,backup),positions in zip(targets(),EXPECTED):
        data=p.read_bytes()
        og=(ROOT/'CTP-og'/REL/p.name).read_bytes()
        assert data==og, 'Baseline differs from OG; review required: '+p.name
        _,_,_,tokens=parts(data)
        actual=tuple(tokens.index(t)+1 for t in TECHS)
        assert actual==positions, (p.name,actual,positions)
        changed=transform(data)
        backup.parent.mkdir(parents=True,exist_ok=True)
        assert not backup.exists(), 'Never overwrite backup'
        backup.write_bytes(data)
        items.append({'path':p.relative_to(ROOT).as_posix(),'backup':backup.relative_to(ROOT).as_posix(),
                      'before_sha256':SHA(data),'after_sha256':SHA(changed),'records':len(tokens),
                      'positions_before':actual,'positions_after':[1,2],
                      'encoding':'bytes preserved; ASCII record lines moved','crlf_before':data.count(b'\r\n')})
        diff=''.join(difflib.unified_diff(data.decode('latin1').splitlines(keepends=True),changed.decode('latin1').splitlines(keepends=True),fromfile='baseline/'+p.name,tofile='B1/'+p.name))
        (OUT/(p.stem+'.diff')).write_bytes(diff.encode('latin1'))
    write_json('manifest.json',{'prepared_at':stamp(),'design_sha256':DESIGN,'files':items,'scope':'Only record order inside Advancements_List #DATA'})
    write_json('inventory-before.json',before)
    print(json.dumps({'stage':'prepared','files':len(items),'inventory_files':len(before),'positions_verified':True}))

def apply():
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    for (p,backup),item in zip(targets(),manifest['files']):
        assert SHA(p.read_bytes())==item['before_sha256'], 'Concurrent edit; abort before any write'
        assert SHA(backup.read_bytes())==item['before_sha256']
    for p,backup in targets():
        p.write_bytes(transform(backup.read_bytes()))
    verify()

def verify():
    before=json.loads((OUT/'inventory-before.json').read_text(encoding='utf-8'))
    after=inventory()
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    assert before.keys()==after.keys(), 'Inventory file set changed'
    changed=sorted(k for k in before if before[k]!=after[k])
    assert changed==sorted(item['path'] for item in manifest['files']), 'Changes outside B1 scope'
    for (p,backup),item in zip(targets(),manifest['files']):
        original=backup.read_bytes()
        actual=p.read_bytes()
        assert SHA(original)==item['before_sha256']
        assert actual==transform(original), 'Unexpected byte edits: '+p.name
        assert SHA(actual)==item['after_sha256']
    write_json('inventory-after.json',after)
    result={'checked_at':stamp(),'stage':'applied and offline verified','changed_files':changed,
            'protected_files_unchanged':len(before)-len(changed),'all_eight_exact_moves':True,
            'record_counts_multisets_rest_order_bytes_crlf_preserved':True,
            'runtime_parser_activation':'not demonstrated','gameplay_improvement':'not measured'}
    write_json('offline-results.json',result)
    print(json.dumps(result))

def restore():
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    for (p,backup),item in zip(targets(),manifest['files']):
        assert SHA(p.read_bytes())==item['after_sha256'], 'Concurrent edit: do not overwrite'
        assert SHA(backup.read_bytes())==item['before_sha256']
    for p,backup in targets():
        p.write_bytes(backup.read_bytes())
    print(json.dumps({'restored_at':stamp(),'restored_files':8,'restart_required':True,'use_original_T0':True}))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=('prepare','apply','verify','restore'))
    globals()[parser.parse_args().action]()
