"""Finite C4 snapshot/sequence guard. No game access, native calls or UI."""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT/'PROEVEN/wondergewicht/20261030'
RUN_ID = 'LAND-STAD-T25-20261103'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key: '+key)
            result[key] = value
        return result
    return json.loads(path.read_text('utf-8-sig'), object_pairs_hook=unique)


def verify_sources(root=ROOT, manifest=HERE/'pins.json'):
    rows = read(manifest)['files']
    own = {r['path']: r['sha256'] for r in rows}
    if len(own) != len(rows):
        raise ValueError('Duplicate source pin')
    required = {'PROEVEN/land-stad-t25/20261103/'+name for name in
                ('README.md', 'Beheer-Proef.ps1', 'Stap-Proef.ps1', 'guard.py', 'check_c0.py')}
    required.update(('PROEVEN/wondergewicht/20261030/pins.json',
                     'PROEVEN/wondergewicht/20261030/after-n1.json',
                     'PROEVEN/Bedien-CTP.ps1', 'PROEVEN/Controleer-Weekbudget.py'))
    if not required.issubset(own):
        raise ValueError('Required completion/source/helper pin omitted')
    old = read(root/'PROEVEN/wondergewicht/20261030/pins.json')['files']
    if len(old) != 107 or any(own.get(r['path']) != r['sha256'] for r in old):
        raise ValueError('Frozen C4 pins omitted/changed')
    old_human = read(root/'PROEVEN/mensprotocol-ok/20261102/pins.json')['files']
    if len(old_human) != 117 or any(own.get(r['path']) != r['sha256'] for r in old_human):
        raise ValueError('Frozen human protocol pins omitted/changed')
    for path, expected in own.items():
        target = (root/path).resolve()
        if not target.is_relative_to(root.resolve()) or sha(target) != expected:
            raise ValueError('Source pin mismatch: '+path)


def validate(snapshot, start, index, reference, after=False):
    if start.get('arm') not in ('control', 'candidate'):
        raise ValueError('Unexpected arm')
    if type(index) is not int or not 1 <= index <= 25:
        raise ValueError('N index outside 1..25')
    actual = snapshot['instance']
    if (actual['pid'], actual['creationtime_filetime'], actual['executable']) != (start['pid'], start['creation_filetime'], start['path']):
        raise ValueError('Snapshot process binding mismatch')
    if start['path'] != str(ROOT/'CTP-proef/ctp_program/ctp/civctp.exe'):
        raise ValueError('Unexpected executable')
    if (snapshot['stable_twice'] is not True or snapshot['loaded_checks'] != reference['loaded_checks']
            or not all(v is True for v in snapshot['loaded_checks'].values())
            or snapshot['binding'] != reference['binding']
            or snapshot['variant'] != reference['variant'] or snapshot['run_id'] != RUN_ID):
        raise ValueError('Incomplete/unbound C4 snapshot')
    rows = snapshot['state']['civilizations']
    if [r['civ_id'] for r in rows] != list(range(2, 9)) or any(type(r['processed_round']) is not int or r['processed_round'] != -1+index-1+int(after) for r in rows):
        raise ValueError('Snapshot native round/participants mismatch')
    # Before the first pass AIP caches may still reflect the serialized T0.
    # Thereafter arm-specific 30000 metadata is authoritative only during opening.
    if index > 1 or after:
        for row in rows:
            status = row['weight_30000_expectation']['status']
            active = row['opening_symbols']['opening_required']
            expected = ('PASS' if start['arm'] == 'candidate' else 'FAIL') if active == 1 else 'NOT_APPLICABLE'
            if active not in (0, 1) or status != expected:
                raise ValueError('Arm/opening weight metadata mismatch')



def snapshot(path, start, index, reference, after=False, data=DATA):
    path = path.resolve()
    if path.parent != data.resolve() or not path.name.startswith('land-t25-'+start['arm']+'-') or path.suffix != '.json':
        raise ValueError('Expected unique arm-prefixed C4 output')
    validate(read(path), start, index, reference, after)
    return dict(path=str(path), sha256=sha(path))


def write_new(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def names(folder, suffix, count):
    if {p.name for p in folder.glob('N*-'+suffix+'.json')} != {f'N{i:02d}-{suffix}.json' for i in range(1, count+1)}:
        raise ValueError('N sequence incomplete/already consumed')


def history(folder, start_path, count, reference, data):
    start = read(start_path)
    previous = None
    last_after = None
    for i in range(1, count+1):
        consumed_path = folder/f'N{i:02d}-consumed.json'
        c = read(consumed_path)
        before = snapshot(Path(c['before_snapshot']['path']), start, i, reference, data=data)
        wanted = dict(n_index=i, maximum_inputs=25, start_sha256=sha(start_path),
                      before_snapshot=before, previous_completed_sha256=previous)
        if c != wanted or (i > 1 and before != last_after):
            raise ValueError('Consumed marker/before snapshot chain mismatch')
        completed_path = folder/f'N{i:02d}-completed.json'
        d = read(completed_path)
        last_after = snapshot(Path(d['after_snapshot']['path']), start, i, reference, after=True, data=data)
        if d != dict(n_index=i, native_round=-1+i, consumed_sha256=sha(consumed_path), after_snapshot=last_after):
            raise ValueError('Completed marker/snapshot chain mismatch')
        previous = sha(completed_path)
    return previous, last_after


def consume(start_path, before_path, index, reference, data=DATA):
    start, folder = read(start_path), start_path.parent
    before = snapshot(before_path, start, index, reference, data=data)
    names(folder, 'consumed', index-1)
    names(folder, 'completed', index-1)
    previous, last_after = history(folder, start_path, index-1, reference, data)
    if index > 1 and before != last_after:
        raise ValueError('Before snapshot is not previous completed snapshot')
    write_new(folder/f'N{index:02d}-consumed.json', dict(n_index=index, maximum_inputs=25,
              start_sha256=sha(start_path), before_snapshot=before, previous_completed_sha256=previous))


def complete(start_path, after_path, index, reference, data=DATA):
    start, folder = read(start_path), start_path.parent
    after = snapshot(after_path, start, index, reference, after=True, data=data)
    names(folder, 'consumed', index)
    names(folder, 'completed', index-1)
    previous, last_after = history(folder, start_path, index-1, reference, data)
    token = folder/f'N{index:02d}-consumed.json'
    c = read(token)
    before = snapshot(Path(c['before_snapshot']['path']), start, index, reference, data=data)
    if c != dict(n_index=index, maximum_inputs=25, start_sha256=sha(start_path),
                 before_snapshot=before, previous_completed_sha256=previous) or (index > 1 and before != last_after):
        raise ValueError('Current consumed marker/before snapshot mismatch')
    if after['path'] == before['path']:
        raise ValueError('After snapshot reuses before output')
    write_new(folder/f'N{index:02d}-completed.json', dict(n_index=index, native_round=-1+index,
              consumed_sha256=sha(token), after_snapshot=after))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('pins', 'consume', 'complete'), required=True)
    parser.add_argument('--start', type=Path)
    parser.add_argument('--snapshot', type=Path)
    parser.add_argument('--index', type=int)
    args = parser.parse_args()
    verify_sources()
    if args.mode != 'pins':
        if args.start is None or args.snapshot is None or args.index is None:
            parser.error('start, snapshot and index required')
        if args.start.resolve() not in (HERE/'control/start.json', HERE/'candidate/start.json'):
            raise ValueError('Expected own arm start record')
        if read(args.start)['arm'] != args.start.parent.name:
            raise ValueError('Start arm mismatch')
        reference = read(DATA/'after-n1.json')
        (consume if args.mode == 'consume' else complete)(args.start.resolve(), args.snapshot, args.index, reference)
    print('PASS '+args.mode)


if __name__ == '__main__':
    main()
