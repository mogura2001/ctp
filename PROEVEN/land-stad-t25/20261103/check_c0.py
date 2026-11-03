"""Focused offline checks of the reused finite sequence; no game process or UI."""
from pathlib import Path
import copy
import json
import sys
import tempfile
sys.dont_write_bytecode = True
import guard as g

checks = []


def reject(name, action):
    try:
        action()
    except (ValueError, FileExistsError):
        checks.append(name)
    else:
        raise AssertionError('Accepted invalid case: '+name)


def run():
    ref = g.read(g.DATA/'after-n1.json')
    for arm in ('control', 'candidate'):
        start = dict(pid=12345, creation_filetime=134378368351978027,
                     path=str(g.ROOT/'CTP-proef/ctp_program/ctp/civctp.exe'), arm=arm)
        def sample(native, active=1):
            value = copy.deepcopy(ref)
            value['instance'].update(pid=start['pid'], creationtime_filetime=start['creation_filetime'], executable=start['path'])
            value['run_id'] = g.RUN_ID
            for row in value['state']['civilizations']:
                row['processed_round'] = native
                row['opening_symbols']['opening_required'] = active
                row['weight_30000_expectation']['status'] = ('PASS' if arm == 'candidate' else 'FAIL') if active else 'NOT_APPLICABLE'
            return value
        g.validate(sample(-1), start, 1, ref)
        g.validate(sample(24), start, 25, ref, after=True)
        g.validate(sample(24, 0), start, 25, ref, after=True)
        checks.append(arm+': initial -1 / N25 native24 / opening0 NOT_APPLICABLE')
        reject(arm+': N26', lambda: g.validate(sample(25), start, 26, ref))
        reject(arm+': wrong native', lambda: g.validate(sample(25), start, 25, ref, after=True))
        for name, mutate in [
            ('full FILETIME low bit', lambda s: s['instance'].update(creationtime_filetime=start['creation_filetime']-1)),
            ('PID', lambda s: s['instance'].update(pid=12346)),
            ('binding', lambda s: s['binding'].update(ai_sha256='0'*64)),
            ('loaded check', lambda s: s['loaded_checks'].update(N30_bound=False)),
            ('unstable', lambda s: s.update(stable_twice=False)),
            ('missing AI', lambda s: s['state']['civilizations'].pop()),
            ('wrong arm metadata', lambda s: s['state']['civilizations'][0]['weight_30000_expectation'].update(status='FAIL' if arm == 'candidate' else 'PASS')),
            ('opening0 must be NA', lambda s: s['state']['civilizations'][0]['opening_symbols'].update(opening_required=0)),
        ]:
            value = sample(0)
            mutate(value)
            reject(arm+': '+name, lambda: g.validate(value, start, 1, ref, after=True))
        with tempfile.TemporaryDirectory(prefix='ctp-land-t25-c0-') as tmp:
            folder = Path(tmp)
            data = folder/'outputs'
            data.mkdir()
            start_path = folder/'start.json'
            g.write_new(start_path, start)
            def output(native):
                path = data/f'land-t25-{arm}-native{native}.json'
                g.write_new(path, sample(native))
                return path
            before = output(-1)
            g.consume(start_path, before, 1, ref, data)
            reject(arm+': duplicate consume', lambda: g.consume(start_path, before, 1, ref, data))
            after = output(0)
            reject(arm+': pending prevents next N', lambda: g.consume(start_path, after, 2, ref, data))
            g.complete(start_path, after, 1, ref, data)
            reject(arm+': duplicate complete', lambda: g.complete(start_path, after, 1, ref, data))
            before = after
            for index in range(2, 26):
                g.consume(start_path, before, index, ref, data)
                after = output(index-1)
                g.complete(start_path, after, index, ref, data)
                before = after
            assert g.read(folder/'N25-completed.json')['native_round'] == 24
            reject(arm+': no N26 after full chain', lambda: g.consume(start_path, before, 26, ref, data))
            g.history(folder, start_path, 25, ref, data)
            content = before.read_bytes()
            before.write_bytes(content+b' ')
            reject(arm+': snapshot hash changed', lambda: g.history(folder, start_path, 25, ref, data))
            checks.append(arm+': full 25-input hash chain to native24')
    g.verify_sources()
    checks.append('all own/frozen dependency pins exact')
    baseline = g.read(g.ROOT/'VERSIES/wondergewicht-2026-10-30/live-baseline.json')
    pins = baseline['aidata']+baseline['saves']+baseline['dll']+baseline['extra_pins']
    assert len(pins) == 162 and len(baseline['aidata']) == 118 and len(baseline['saves']) == 38
    assert all(g.sha(g.ROOT/p['path']) == p['sha256'] for p in pins)
    for group, base in [('aidata', 'CTP-proef/ctp_data/default/aidata'), ('saves', 'CTP-proef/ctp_program/ctp/save')]:
        actual = {p.relative_to(g.ROOT).as_posix() for p in (g.ROOT/base).rglob('*') if p.is_file()}
        assert actual == {p['path'] for p in baseline[group]}
    checks.append('live baseline162 / full aidata118 / full saves38 unchanged')
    source = g.ROOT/'CTP-proef/ctp_program/ctp/save/games/Julius/UITBREIDING-LAND-STAD-T0'
    assert source.stat().st_size == 350409 and g.sha(source) == 'c6bab2909d9f5739005e5f24678cf0a5818b17821031ca171c454e2cc40f4327'
    old = g.read(g.ROOT/'PROEVEN/mensprotocol-ok/20261102/pins.json')['files']
    own = {r['path']: r['sha256'] for r in g.read(g.HERE/'pins.json')['files']}
    assert len(old) == 117 and all(own.get(r['path']) == r['sha256'] for r in old)
    checks.append('old117 and transitive107 preserved / Rome T0 exact')
    assert not any(g.HERE.glob('*/before.json'))
    assert not any(g.HERE.glob('*/start.json'))
    assert not list(g.DATA.glob('land-t25-*.json'))
    checks.append('no Prepare/start/C4 sample performed')
    print(json.dumps(dict(status='PASS', offline_only=True, checks=checks,
                         source_pins=len(own), no_gameplay_measurement=True), indent=2))


if __name__ == '__main__':
    run()
