"""Read-only C0 byte/category/routing checks; this is not the CTP parser."""
import argparse, datetime as dt, difflib, hashlib, json, re
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
LIVE = ROOT / 'CTP-proef'
AID = 'ctp_data/default/aidata/'
ROUTES = {'beginturn.fli':'default', 'beginturnCleric.fli':'cleric',
          'beginturnSlaver.fli':'slaver', 'beginturnSciFew.fli':'scifew',
          'beginturnSciMany.fli':'scimany', 'beginturnWarFew.fli':'milfew',
          'beginturnWarMany.fli':'milmany'}
HEADER = b'#include "aipdef.h"\r\n'
OPENING = HEADER + (b'Building_Build_List_Element Wonder_List[MAX_ELEMENTS];\r\n'
                     b'#DATA\r\n"WONDER_LABRYINTH_OF_THE_MINOTAUR", 9100.0;\r\n#END_DATA\r\n')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def record(path, base):
    data = path.read_bytes()
    return dict(path=path.relative_to(base).as_posix(), size=len(data), sha256=sha(data))

def mask_comments(data):
    # Keep offsets/newlines and quoted strings; exclude both comment forms.
    return re.sub(rb'"(?:\\.|[^"\\])*"|//[^\r\n]*|/\*[\s\S]*?\*/',
                  lambda m: re.sub(rb'[^\r\n]', b' ', m[0]) if m[0].startswith((b'//', b'/*')) else m[0], data)

def blocks(data):
    active = mask_comments(data)
    pattern = rb'(?m)^[ \t]*(\w+)[ \t]+(\w+)\[MAX_ELEMENTS\];[ \t]*\r?\n[ \t]*#DATA\b[\s\S]*?^[ \t]*#END_DATA[^\r\n]*(?:\r?\n|$)'
    found = {}
    for match in re.finditer(pattern, active):
        name = match[2].decode('ascii')
        assert name not in found, f'duplicate active category {name}'
        found[name] = data[match.start():match.end()]
    return found

def actions(personality, eol):
    return (f'action load("opening_restore_wonders_{personality}.aip") when (opening_required < 0.5)'.encode() + eol
            + b'action load("opening_wonders.aip") when (opening_required > 0.5)' + eol)

def routed(before, personality):
    active = mask_comments(before)
    assert active.count(b'{') == active.count(b'}') == 1
    close = active.rfind(b'}')
    assert not active[close+1:].strip()
    eol = b'\r\n' if b'\r\n' in before else b'\n'
    assert before[:close].endswith(eol)
    return before[:close] + actions(personality, eol) + before[close:]

def inventory(folder):
    return [record(p, ROOT) for p in sorted(folder.rglob('*')) if p.is_file()]

def check():
    manifest = json.loads((PACKAGE/'manifest.json').read_text('utf-8'))
    baseline = json.loads((PACKAGE/'live-baseline.json').read_text('utf-8'))
    assert manifest['target_path_base'] == 'CTP-proef'
    assert manifest['routes'] == ROUTES
    assert manifest['header'] == record(LIVE/AID/'AIPs/Aipdef.h', LIVE)
    assert inventory(LIVE/AID) == baseline['aidata']
    assert inventory(LIVE/'ctp_program/ctp/save') == baseline['saves']
    assert len(baseline['saves']) == 38
    for group in ('dll', 'extra_pins'):
        for pin in baseline[group]:
            assert record(ROOT/pin['path'], ROOT) == pin, pin['path']
    assert sha((PACKAGE/'live-baseline.json').read_bytes()) == manifest['live_baseline_sha256']
    assert len(manifest['files']) == 15
    expected, diff, route_results, restored = {}, [], [], []
    expected[AID+'AIPs/opening_wonders.aip'] = OPENING
    for route, personality in ROUTES.items():
        rel = AID+route
        before = (PACKAGE/'backups'/rel).read_bytes()
        assert before == (LIVE/rel).read_bytes(), rel
        after = routed(before, personality)
        active_before = mask_comments(before)
        loader = rb'(?m)^[ \t]*#include[ \t]+"aiploader\.fli"'
        assert len(re.findall(loader, active_before)) == (0 if personality == 'default' else 1)
        expected[rel] = after
        source_rel = AID+'AIPs/'+personality+'.aip'
        source = (LIVE/source_rel).read_bytes()
        categories = blocks(source)
        block = categories['Wonder_List']
        source_pin = next(x for x in manifest['sources'] if x['source_rel'] == source_rel)
        assert source_pin['source_sha256'] == sha(source)
        assert source_pin['category_sha256'] == {k:sha(v) for k,v in categories.items()}
        assert source_pin['wonder_block_size'] == len(block)
        partial = HEADER + block
        assert set(blocks(partial)) == {'Wonder_List'}
        assert blocks(partial)['Wonder_List'] == block
        restore_rel = AID+'AIPs/opening_restore_wonders_'+personality+'.aip'
        expected[restore_rel] = partial
        restored.append(dict(personality=personality, wonder_block_sha256=sha(block), categories_pinned=len(categories)))
        eol = b'\r\n' if b'\r\n' in before else b'\n'
        assert mask_comments(after).rstrip().endswith(actions(personality, eol)+b'}')
        route_results.append(dict(route=route, personality=personality, unchanged_prefix_and_suffix=True, active_loader_preserved=True, final_action_pair=True))
    assert set(blocks(OPENING)) == {'Wonder_List'}
    assert re.findall(rb'"(WONDER_[A-Z_]+)"\s*,\s*([0-9.]+);', mask_comments(OPENING)) == [(b'WONDER_LABRYINTH_OF_THE_MINOTAUR',b'9100.0')]
    header = (LIVE/AID/'AIPs/Aipdef.h').read_bytes()
    assert re.search(rb'struct\s+Building_Build_List_Element\b', mask_comments(header))
    assert re.search(rb'#define\s+MAX_ELEMENTS\s+200\b', mask_comments(header))
    assert re.search(rb'(?m)^WONDER_LABRYINTH_OF_THE_MINOTAUR\s*\{', (LIVE/'ctp_data/default/gamedata/Wonder.txt').read_bytes())
    actual = {p.relative_to(PACKAGE/'candidate').as_posix() for p in (PACKAGE/'candidate').rglob('*') if p.is_file()}
    assert actual == set(expected) == {x['target_rel'] for x in manifest['files']}
    backup_paths = {p.relative_to(PACKAGE/'backups').as_posix() for p in (PACKAGE/'backups').rglob('*') if p.is_file()}
    assert backup_paths == {AID+r for r in ROUTES}
    for item in manifest['files']:
        rel, after = item['target_rel'], expected[item['target_rel']]
        assert (PACKAGE/item['candidate_package_rel']).read_bytes() == after
        assert item['after_sha256'] == sha(after) and item['after_size'] == len(after)
        if item['before_existed']:
            before = (PACKAGE/item['backup_package_rel']).read_bytes()
            assert not item['new_absent'] and item['before_sha256'] == sha(before) and item['before_size'] == len(before)
        else:
            before = b''
            assert item['new_absent'] and not (LIVE/rel).exists()
            assert item['before_sha256'] is None and item['before_size'] is None and item['backup_package_rel'] is None
        diff.extend(difflib.unified_diff(before.decode('cp1252').splitlines(True), after.decode('cp1252').splitlines(True), fromfile='before/'+rel, tofile='candidate/'+rel))
    assert (PACKAGE/'wijzigingen.diff').read_bytes() == ''.join(diff).encode('utf-8')
    return dict(stage='C0_STATIC_PASS_NOT_INSTALLED', at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                manifest_sha256=sha((PACKAGE/'manifest.json').read_bytes()), checker_sha256=sha(Path(__file__).read_bytes()),
                diff_sha256=sha((PACKAGE/'wijzigingen.diff').read_bytes()), candidate_files=15, backups=7,
                live_aidata_files=len(baseline['aidata']), unchanged_saves=38, live_baseline_exact=True,
                opening_entries=1, opening_weight=9100, wonder_only_partials=8, restored_categories=restored,
                routes=route_results, header_and_token_verified=True, full_diff_verified=True,
                engine_parser='NOT_TESTED', effective_list='NOT_MEASURED', city_queue='NOT_MEASURED', gameplay='NOT_MEASURED')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', action='store_true', help='write only package/resultaat.json')
    args = parser.parse_args()
    result = check()
    text = json.dumps(result, indent=2, ensure_ascii=False)+'\n'
    if args.output:
        (PACKAGE/'resultaat.json').write_text(text, encoding='utf-8', newline='')
    print(text)
