"""Small read-only projection of the pinned release reader. No native callbacks."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import re
import struct
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RELEASE = ROOT / 'PROEVEN/doel3/20261012-release-v1'
WONDERS = ROOT / 'VERSIES/wonders-2026-10-28'
CORE_NAME = '_ctp_wonder_20261029_release_core'
READER_NAME = '_ctp_wonder_20261029_release_reader'


def verify_pins():
    pins = json.loads((HERE/'pins.json').read_text('utf-8'))
    for item in pins['files']:
        path = ROOT/item['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Pinned source changed: '+item['path'])
    return hashlib.sha256((HERE/'pins.json').read_bytes()).hexdigest()


def load_reader():
    # Absolute paths + unique names avoid both cwd imports and preloaded
    # original_core/doel3original_core aliases used by unrelated observers.
    if CORE_NAME in sys.modules or READER_NAME in sys.modules:
        raise ValueError('Wonder projection module name already occupied')
    spec = importlib.util.spec_from_file_location(CORE_NAME, RELEASE/'original_core.py')
    core = importlib.util.module_from_spec(spec)
    sys.modules[CORE_NAME] = core
    spec.loader.exec_module(core)
    source = (RELEASE/'Lees-Doel3.py').read_text('utf-8')
    substitutions = [
        ('from original_core import *', 'from '+CORE_NAME+' import *'),
        ("    parser.add_argument('--pid',type=int,required=True)",
         "    parser.add_argument('--pid',type=int,required=True)\n"
         "    parser.add_argument('--creation-filetime',type=int,required=True)\n"
         "    parser.add_argument('--wonder-arm',choices=('control','candidate'),required=True)"),
        ("        if times[1].dwLowDateTime or times[1].dwHighDateTime:raise ValueError('Process exited during snapshot')",
         "        if times[1].dwLowDateTime or times[1].dwHighDateTime:raise ValueError('Process exited during snapshot')\n"
         "        wonder_creationtime(times,args.creation_filetime)"),
    ]
    for before, after in substitutions:
        if source.count(before) != 1:
            raise ValueError('Release projection anchor changed')
        source = source.replace(before, after)
    spec = importlib.util.spec_from_file_location(READER_NAME, RELEASE/'Lees-Doel3.py')
    reader = importlib.util.module_from_spec(spec)
    sys.modules[READER_NAME] = reader
    exec(compile(source, str(RELEASE/'Lees-Doel3.py'), 'exec'), reader.__dict__)
    reader.FOLDER = HERE
    reader.wonder_creationtime = creationtime_exact
    return reader, source


def creationtime_exact(times, expected):
    actual = (times[0].dwHighDateTime << 32) | times[0].dwLowDateTime
    if not 0 < expected < (1 << 64) or actual != expected:
        raise ValueError('Exact authorized process creationtime mismatch')


def text_expectations(arm):
    manifest = json.loads((WONDERS/'manifest.json').read_text('utf-8'))
    baseline = json.loads((WONDERS/'live-baseline.json').read_text('utf-8'))
    expected = {x['path']: (x['size'], x['sha256']) for x in baseline['aidata']}
    if len(expected) != 118 or len(manifest['files']) != 15:
        raise ValueError('Unexpected pinned wonder text inventory')
    # Check both staged candidate bytes and the exact effective disk arm.
    for item in manifest['files']:
        blob = (WONDERS/item['candidate_package_rel']).read_bytes()
        if (len(blob), hashlib.sha256(blob).hexdigest()) != (item['after_size'], item['after_sha256']):
            raise ValueError('Staged wonder candidate changed')
        if arm == 'candidate':
            expected['CTP-proef/'+item['target_rel']] = (item['after_size'], item['after_sha256'])
    aidata = ROOT/'CTP-proef/ctp_data/default/aidata'
    actual = {p.relative_to(ROOT).as_posix(): (p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
              for p in aidata.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError('Effective wonder arm disk text inventory mismatch')
    source_categories = {}
    for item in manifest['sources']:
        personality = Path(item['source_rel']).stem
        partial = WONDERS/'candidate/ctp_data/default/aidata/AIPs'/('opening_restore_wonders_'+personality+'.aip')
        active = re.sub(rb'//[^\r\n]*|/\*[\s\S]*?\*/', b'', partial.read_bytes())
        weights = [float(x) for x in re.findall(rb'"WONDER_[A-Z_]+"\s*,\s*([0-9.]+);', active)]
        if len(weights) <= 1:
            raise ValueError('Pinned control category is not a multiple-entry list')
        source_categories[personality] = dict(count=len(weights), weights=weights,
            category_sha256=item['category_sha256']['Wonder_List'])
    return dict(arm=arm, aidata_files=len(actual), candidate_files=15, source_categories=source_categories,
                text_manifest_sha256=hashlib.sha256((WONDERS/'manifest.json').read_bytes()).hexdigest())


def wonder_state(raw_read, actor, core):
    read = core.bounded(raw_read)
    def at(address, offset=0):
        return core.checked(address, offset)
    def u32(address):
        return struct.unpack('<I', read(at(address), 4))[0]
    def i32(address):
        return struct.unpack('<i', read(at(address), 4))[0]
    aip = at(u32(at(actor, 0x94)), 0x20)
    if u32(at(aip, 0x800)) != actor:
        raise ValueError('Wonder AIP owner mismatch')
    container = u32(at(aip, 0x7d0))
    entries, data, count = [], 0, None
    if container:
        data, count = u32(container), i32(at(container, 4))
        if not 0 <= count <= 200:
            raise ValueError('Invalid wonder count')
        if count:
            records = read(at(data), 32*count)
            for offset in range(0, len(records), 32):
                weight = struct.unpack_from('<d', records, offset)[0]
                index = struct.unpack_from('<i', records, offset+8)[0]
                category = struct.unpack_from('<i', records, offset+0x18)[0]
                if not math.isfinite(weight) or index < 0 or category != -1:
                    raise ValueError('Invalid wonder record')
                entries.append(dict(weight=weight, native_index=index, category=category))
        elif data:
            at(data)  # Validate nonnull empty storage, without reading it.
    engine = u32(at(actor, 0xc4))
    table = u32(engine)
    buckets, bucket_count = u32(at(table, 4)), i32(at(table, 8))
    if not 0 < bucket_count <= 4096:
        raise ValueError('Invalid bounded symbol bucket count')
    bucket_bytes = b''.join(read(at(buckets, off), min(8192, bucket_count*4-off))
                            for off in range(0, bucket_count*4, 8192))
    visited, found = set(), {}
    for (node,) in struct.iter_unpack('<I', bucket_bytes):
        while node:
            if node in visited or len(visited) >= 4096:
                raise ValueError('Cyclic/reused/overlong symbol chain')
            visited.add(node)
            nameptr, symbol, node = struct.unpack('<III', read(at(node), 12))
            name = bytearray()
            for offset in range(128):
                char = read(at(nameptr, offset), 1)
                if char == b'\0':
                    break
                name.extend(char)
            else:
                raise ValueError('Unterminated bounded symbol name')
            if name not in (b'opening_required', b'opening_completed'):
                continue
            key = name.decode('ascii')
            if key in found:
                raise ValueError('Duplicate exact opening symbol')
            external = u32(symbol)
            value_bytes = read(at(symbol, 8), 8)
            value = struct.unpack('<d', value_bytes)[0]
            inputmask = struct.unpack('<H', read(at(symbol, 0xc2), 2))[0]
            flags = struct.unpack('<H', read(at(symbol, 0x68), 2))[0]
            special = read(at(symbol, 0x6a), 1)[0]
            if external or not inputmask & 4 or flags & 4 or special & 1:
                raise ValueError('Invalid opening input symbol binding')
            if value_bytes not in (struct.pack('<d', 0.0), struct.pack('<d', 1.0)):
                raise ValueError('Opening symbol is not exact double zero/one')
            found[key] = value
    if set(found) != {'opening_required', 'opening_completed'} or sum(found.values()) != 1:
        raise ValueError('Missing/noncomplementary opening symbols')
    return dict(effective_wonder_list=dict(status='NULL' if not container else 'EMPTY' if not count else 'PRESENT',
                container=hex(container), data=hex(data), count=count, records=entries,
                record_size=32, native_token_binding='UNKNOWN'),
                opening_symbols=found, symbol_scan=dict(buckets=bucket_count, visited_nodes=len(visited)))


def main():
    options = argparse.ArgumentParser(add_help=False)
    options.add_argument('--wonder-arm', choices=('control', 'candidate'), required=True)
    options.add_argument('--creation-filetime', type=int, required=True)
    options.add_argument('--manifest', type=Path, required=True)
    if '-h' in sys.argv or '--help' in sys.argv:
        reader, _ = load_reader()
        reader.main()
        return
    args, _ = options.parse_known_args()
    package_sha = verify_pins()
    if args.manifest.read_bytes() != (HERE/'participants.json').read_bytes():
        raise ValueError('Fixed-c6ba-T0 participants manifest differs from pinned LAND copy')
    disk = text_expectations(args.wonder_arm)
    reader, _ = load_reader()
    original_observe = reader.observe_goal3
    def observe(read, eb, ab, participants):
        # Keep original seven actors/scalars and their owner/vtable validation.
        if text_expectations(args.wonder_arm) != disk:
            raise ValueError('Text arm changed during observation')
        state = original_observe(read, eb, ab, participants)
        for row in state['civilizations']:
            row.update(wonder_state(read, int(row['ai_actor'], 16), reader))
            active = row['opening_symbols']['opening_required'] == 1
            listing = row['effective_wonder_list']
            matches = (listing['count'] == 1 and listing['records'][0]['weight'] == 9100.0
                       if args.wonder_arm == 'candidate' else
                       listing['count'] is not None and listing['count'] > 1)
            row['opening_list_expectation'] = dict(
                status=('PASS' if matches else 'FAIL') if active else 'NOT_APPLICABLE',
                expected='one entry, weight 9100, category -1' if args.wonder_arm == 'candidate' else 'multiple source entries',
                native_token_binding='UNKNOWN')
            row['source_weight_sequence_matches'] = [name for name, source in disk['source_categories'].items()
                if [r['weight'] for r in listing['records']] == source['weights']]
        state['wonder_projection'] = dict(package_pins_sha256=package_sha, text=disk,
            native_token_binding='UNKNOWN', queue_production_proven=False)
        return state
    reader.observe_goal3 = observe
    reader.main()


if __name__ == '__main__':
    main()
