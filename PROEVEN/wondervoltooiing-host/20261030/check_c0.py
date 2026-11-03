"""Small offline checks: no reader invocation, process handle or UI."""
from pathlib import Path
import copy
import json
import tempfile
import sys
sys.dont_write_bytecode = True
import guard as g

checks = []

def ok(name, callback):
    callback()
    checks.append(name)


def reject(name, callback):
    try:
        callback()
    except (ValueError, FileExistsError):
        checks.append(name)
    else:
        raise AssertionError('Accepted invalid case: '+name)


def run():
    ref = g.read(g.DATA/'after-n1.json')
    start = dict(pid=12345, creation_filetime=134378368351978027,
                 path=str(g.ROOT/'CTP-proef/ctp_program/ctp/civctp.exe'))
    def sample(round_number):
        return dict(instance=dict(pid=start['pid'], creationtime_filetime=start['creation_filetime'], executable=start['path']),
                    stable_twice=True, loaded_checks=copy.deepcopy(ref['loaded_checks']), binding=copy.deepcopy(ref['binding']),
                    variant=ref['variant'], run_id=g.RUN_ID,
                    state=dict(civilizations=[dict(civ_id=r['civ_id'], processed_round=round_number,
                         weight_30000_expectation=copy.deepcopy(r['weight_30000_expectation'])) for r in ref['state']['civilizations']]))
    ok('before-N21/native45', lambda: g.validate(sample(45), start, 21, ref))
    ok('after-N21/native46', lambda: g.validate(sample(46), start, 21, ref, after=True))
    reject('N22 forbidden', lambda: g.validate(sample(46), start, 22, ref))
    for name, mutate in [
        ('PID', lambda s: s['instance'].update(pid=12346)),
        ('full FILETIME low bit', lambda s: s['instance'].update(creationtime_filetime=start['creation_filetime']-1)),
        ('executable', lambda s: s['instance'].update(executable='other.exe')),
        ('binding', lambda s: s['binding'].update(ai_sha256='0'*64)),
        ('code check', lambda s: s['loaded_checks'].update(N30_bound=False)),
        ('unstable', lambda s: s.update(stable_twice=False)),
        ('round counter', lambda s: s['state']['civilizations'][3].update(processed_round=27)),
        ('missing AI', lambda s: s['state']['civilizations'].pop()),
        ('duplicate AI', lambda s: s['state']['civilizations'][1].update(civ_id=2)),
        ('weight FAIL', lambda s: s['state']['civilizations'][0]['weight_30000_expectation'].update(status='FAIL')),
    ]:
        value = sample(26)
        mutate(value)
        reject(name, lambda: g.validate(value, start, 2, ref))
    with tempfile.TemporaryDirectory(prefix='ctp-completion-c0-') as temporary:
        folder = Path(temporary)
        data = folder/'outputs'
        data.mkdir()
        start_path = folder/'start.json'
        g.write_new(start_path, start)
        def output(round_number):
            path = data/f'completion-native{round_number}.json'
            g.write_new(path, sample(round_number))
            return path
        before = output(25)
        g.consume(start_path, before, 1, ref, data)
        reject('duplicate N1', lambda: g.consume(start_path, before, 1, ref, data))
        after = output(26)
        reject('pending N prevents N2', lambda: g.consume(start_path, after, 2, ref, data))
        g.complete(start_path, after, 1, ref, data)
        reject('duplicate completion', lambda: g.complete(start_path, after, 1, ref, data))
        copied = data/'completion-copy.json'
        copied.write_bytes(after.read_bytes())
        reject('same bytes different before path', lambda: g.consume(start_path, copied, 2, ref, data))
        marker = folder/'N01-completed.json'
        original = marker.read_bytes()
        marker.write_bytes(original+b' ')
        # N2 records the actual completed hash; altering it later breaks N3 history.
        g.consume(start_path, after, 2, ref, data)
        marker.write_bytes(original)
        after2 = output(27)
        reject('previous completed hash altered', lambda: g.complete(start_path, after2, 2, ref, data))
        marker.write_bytes(original+b' ')
        g.complete(start_path, after2, 2, ref, data)
        before = after2
        for index in range(3, 22):
            g.consume(start_path, before, index, ref, data)
            after = output(25+index)
            g.complete(start_path, after, index, ref, data)
            before = after
        assert g.read(folder/'N21-completed.json')['native_round'] == 46
        reject('no N22 after completed N21', lambda: g.consume(start_path, before, 22, ref, data))
        assert len(list(folder.glob('N*-consumed.json'))) == 21
        assert len(list(folder.glob('N*-completed.json'))) == 21
        checks.append('21-input complete chain to native46')
        source = before.read_bytes()
        before.write_bytes(source+b' ')
        reject('after snapshot hash altered', lambda: g.history(folder, start_path, 21, ref, data))
        before.write_bytes(source)
        token = folder/'N21-consumed.json'
        original_token = token.read_bytes()
        changed = g.read(token)
        changed['n_index'] = 20
        token.write_text(json.dumps(changed))
        reject('consumed row counter altered', lambda: g.history(folder, start_path, 21, ref, data))
        token.write_bytes(original_token)
        manifest = g.read(g.HERE/'pins.json')
        damaged = copy.deepcopy(manifest)
        damaged['files'][0]['sha256'] = '0'*64
        bad = folder/'badpins.json'
        g.write_new(bad, damaged)
        reject('source pin corruption', lambda: g.verify_sources(manifest=bad))
        damaged = copy.deepcopy(manifest)
        damaged['files'].pop(0)
        bad.write_text(json.dumps(damaged))
        reject('source pin omitted', lambda: g.verify_sources(manifest=bad))
        duplicate = folder/'duplicate.json'
        duplicate.write_text('{"x":1,"x":2}')
        reject('duplicate JSON keys', lambda: g.read(duplicate))
    ok('full source pins', g.verify_sources)
    baseline = g.read(g.ROOT/'VERSIES/wondergewicht-2026-10-30/live-baseline.json')
    pins = baseline['aidata']+baseline['saves']+baseline['dll']+baseline['extra_pins']
    assert len(pins) == 162 and len(baseline['aidata']) == 118 and len(baseline['saves']) == 38
    backup = g.ROOT/'PROEVEN/wondergewicht-host/20261030/candidate/backup'
    assert all(g.sha(backup/p['path']) == p['sha256'] for p in pins)
    checks.append('C4 exact 162 backup pins / 118 aidata / 38 saves')
    print(json.dumps(dict(status='PASS', offline_only=True, no_reader_process_or_ui=True,
                         checks=checks, source_pins=len(g.read(g.HERE/'pins.json')['files'])), indent=2))


if __name__ == '__main__':
    run()
