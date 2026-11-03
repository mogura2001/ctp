"""Finite read-only token and real-queue projection; composes the frozen reader."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import struct
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT/'PROEVEN/wonderlijst-meting/20261029'
TOKEN = b'WONDER_LABRYINTH_OF_THE_MINOTAUR'
LIMIT = 4096


def verify_pins():
    pins = json.loads((HERE/'pins.json').read_text('utf-8'))
    for item in pins['files']:
        if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Wonderbewijs pin changed: '+item['path'])
    return hashlib.sha256((HERE/'pins.json').read_bytes()).hexdigest()


def load_base():
    name = '_ctp_wonderbewijs_20261029_frozen_base'
    if name in sys.modules:
        raise ValueError('Wonderbewijs base module name occupied')
    spec = importlib.util.spec_from_file_location(name, BASE/'Lees-Wonderlijst.py')
    base = importlib.util.module_from_spec(spec)
    sys.modules[name] = base
    spec.loader.exec_module(base)
    return base


def token_hash(token):
    if not token or b'\0' in token or len(token) >= 128:
        raise ValueError('Invalid exact identifier token')
    value = 0
    for byte in token+b'\0':
        value = (value+byte) & 0xffff
        value = ((value << 1) | (value >> 15)) & 0xffff
    return value, value % 547


class View:
    """Only checked reads and the two finite tree layouts supplied in A."""
    def __init__(self, read, core):
        self.read = core.bounded(read)
        self.at = core.checked

    def u32(self, address):
        return struct.unpack('<I', self.read(self.at(address), 4))[0]

    def i32(self, address):
        return struct.unpack('<i', self.read(self.at(address), 4))[0]

    def name(self, pointer):
        name = bytearray()
        for offset in range(128):
            byte = self.read(self.at(pointer, offset), 1)
            if byte == b'\0':
                return bytes(name)
            name.extend(byte)
        raise ValueError('Unterminated exact token name')

    def tree(self, root, key_offset, children, payload_offset):
        todo, seen, keys, rows = [root], set(), set(), []
        while todo:
            node = todo.pop()
            if not node:
                continue
            if node in seen or len(seen) >= LIMIT:
                raise ValueError('Cyclic/reused/overlong city or pool tree')
            seen.add(node)
            key = self.u32(self.at(node, key_offset))
            if key in keys:
                raise ValueError('Duplicate exact city or pool key')
            keys.add(key)
            rows.append((key, self.u32(self.at(node, payload_offset)), node))
            todo.extend(self.u32(self.at(node, off)) for off in children)
        return rows


def native_identity(view, eb):
    strings = view.u32(eb+0x67dcfc)
    hash16, bucket = token_hash(TOKEN)
    node = view.u32(view.at(view.u32(view.at(strings, 8)), 4*bucket))
    seen, sid = set(), None
    while node:
        if node in seen or len(seen) >= LIMIT:
            raise ValueError('Cyclic/overlong exact StringDB token search')
        seen.add(node)
        name = view.name(view.u32(view.at(node, 4)))
        if name == TOKEN:
            sid = view.u32(node)
            break
        node = view.u32(view.at(node, 0xc if TOKEN < name else 0x10))
    if sid is None:
        raise ValueError('Exact Labyrinth token SID absent')
    database = view.u32(eb+0x67dd5c)
    count, records = view.i32(database), view.u32(view.at(database, 8))
    if not 3 <= count <= 200:
        raise ValueError('WonderDB count out of bounds')
    matches = [i for i in range(count) if view.u32(view.at(records, i*0xd0+4)) == sid]
    if matches != [2]:
        raise ValueError('Exact token SID is not uniquely WonderDB index 2: '+repr(matches))
    record = view.at(records, 2*0xd0)
    return dict(token=TOKEN.decode('ascii'), hash16=hash16, bucket=bucket, string_sid=sid,
                unique_native_index=2, wonder_count=count, wonder_record=hex(record),
                binding='EXACT_STRINGDB_TOKEN_AND_UNIQUE_WONDERDB_SID'), record


def real_queue(view, citydata):
    queue = view.at(citydata, 0x450)
    count, head, tail = view.i32(queue), view.u32(view.at(queue, 8)), view.u32(view.at(queue, 12))
    if not 0 <= count <= LIMIT or (count == 0) != (head == 0 and tail == 0):
        raise ValueError('Queue count/head/tail inconsistent')
    if count and (not head or not tail):
        raise ValueError('Nonempty queue has a null endpoint')
    node, seen, rows = head, set(), []
    while node:
        if node in seen or len(seen) >= count:
            raise ValueError('Cyclic/overlong queue')
        seen.add(node)
        kind, category = view.i32(view.at(node, 4)), view.i32(view.at(node, 8))
        rows.append(dict(node=hex(node), type=kind, build_class=category,
                         is_exact_labyrinth=(category == 9 and kind == 2)))
        nextnode = view.u32(view.at(node, 0x10))
        if not nextnode and node != tail:
            raise ValueError('Queue tail does not match final node')
        node = nextnode
    if len(rows) != count:
        raise ValueError('Queue count differs from linked node count')
    return dict(queue=hex(queue), count=count, head=hex(head), tail=hex(tail), nodes=rows,
                new_enqueue_proven=False)


def actor_cities(view, eb, player, actor, civ):
    container = view.u32(view.at(actor, 0x8c))
    count = view.i32(container)
    if not 0 <= count <= LIMIT:
        raise ValueError('AI cityset count out of bounds')
    cities = view.tree(view.u32(view.at(container, 8)), 0, (4, 8), 12)
    if len(cities) != count:
        raise ValueError('AI cityset count mismatch')
    for ident, agent, _ in cities:
        if view.u32(view.at(agent, 12)) != ident or view.i32(view.at(agent, 4)) != 2:
            raise ValueError('AI cityset/CityAgent identity mismatch')
    mapping = view.u32(view.at(player, 0x12c8))
    slot_by_id = {key: payload for key, payload, _ in view.tree(view.u32(view.at(mapping, 8)), 0, (4, 8), 12)}
    array = view.u32(view.at(player, 0x12c0))
    slots, handles = view.i32(view.at(array, 8)), view.u32(view.at(array, 12))
    if not 0 <= slots <= LIMIT:
        raise ValueError('Player city array length out of bounds')
    pool = view.u32(eb+0x67dd74)
    result, used_handles, used_slots = [], set(), set()
    for ident, agent, _ in cities:
        if ident not in slot_by_id:
            raise ValueError('AI city ID absent from exact player slot map')
        slot = view.i32(slot_by_id[ident])
        if not 0 <= slot < slots or slot in used_slots:
            raise ValueError('Invalid/reused player city slot')
        used_slots.add(slot)
        handle = view.u32(view.at(handles, 4*slot))
        if not handle or handle in used_handles:
            raise ValueError('Null/reused full engine city handle')
        used_handles.add(handle)
        bucket = view.u32(view.at(pool, 0xc+4*(handle & 1023)))
        nodes = view.tree(bucket, 0xc, (4, 8), 0x58)
        matches = [(payload, node) for key, payload, node in nodes if key == handle]
        if len(matches) != 1:
            raise ValueError('Full engine city handle absent/ambiguous in typed pool')
        citydata, node = matches[0]
        if view.u32(view.at(node, 0xc)) != handle or view.i32(view.at(node, 0x18)) != civ:
            raise ValueError('Full city handle or pool owner mismatch')
        if view.i32(view.at(citydata, 4)) != civ:
            raise ValueError('Engine CityData owner mismatch')
        result.append(dict(ai_city_id=ident, ai_city_agent=hex(agent), player_slot=slot,
            full_engine_handle=handle, pool_node=hex(node), city_data=hex(citydata), owner=civ,
            identity='AI_CITY_ID_TO_PLAYER_SLOT_TO_FULL_HANDLE_TO_OWNED_CITYDATA',
            real_queue=real_queue(view, citydata), production='UNKNOWN_NOT_PROJECTED',
            stored_production='UNKNOWN_NOT_PROJECTED', exact_rank='UNKNOWN',
            build_time='UNKNOWN', admission='UNKNOWN', storage_exception='UNKNOWN'))
    return result


def evidence(read, eb, state, core):
    view = View(read, core)
    identity, record = native_identity(view, eb)  # Exactly once per complete sample.
    players = view.u32(eb+0x67dd80)
    advance_count = state['advance_count']
    if not 0 < advance_count <= 512:
        raise ValueError('Advance count out of bounds')
    prerequisite, obsolete_count = view.i32(view.at(record, 8)), view.i32(view.at(record, 0x2c))
    if prerequisite != -1 and not 0 <= prerequisite < advance_count:
        raise ValueError('Wonder prerequisite outside loaded advance database')
    if not 0 <= obsolete_count <= 8:
        raise ValueError('Wonder obsolete advance count outside record bounds')
    obsolete = [view.i32(view.at(record, 0xc+4*i)) for i in range(obsolete_count)]
    if any(not 0 <= i < advance_count for i in obsolete) or len(set(obsolete)) != len(obsolete):
        raise ValueError('Invalid/duplicate obsolete advance index')
    def known(player, index):
        science = view.u32(view.at(player, 0x12ec))
        data = view.u32(view.at(science, 0x1c))
        raw = view.read(view.at(data, index), 1)[0]
        return dict(index=index, raw_byte=raw, known=raw != 0)
    obsolete_players = []
    for civ in range(32):
        player = view.u32(view.at(players, 4*civ))
        if player:
            obsolete_players.append(dict(civ_id=civ, advances=[known(player, i) for i in obsolete]))
    built_array = view.u32(view.at(view.u32(eb+0x67a69c), 0x14))
    built_raw = view.u32(view.at(built_array, 4*2))
    state['wonder_native_identity'] = identity
    state['wonder_global_evidence'] = dict(global_built_raw=built_raw,
        global_built='UNKNOWN_RAW_FIELD_SEMANTICS_NOT_PROVEN',
        raw_source='u32(u32(u32(A7A69C)+0x14)+4*index)',
        engine_built_gate='UNKNOWN_A7AB08_TO_4F0330_NOT_PROJECTED',
        obsolete_advances=obsolete, existing_player_obsolete=obsolete_players,
        obsolete_at_any_existing_player=any(a['known'] for p in obsolete_players for a in p['advances']),
        engine_admission='UNKNOWN')
    for row in state['civilizations']:
        civ, actor = row['civ_id'], int(row['ai_actor'], 16)
        player = view.u32(view.at(players, 4*civ))
        aip = view.at(view.u32(view.at(actor, 0x94)), 0x20)
        if view.u32(view.at(aip, 0x800)) != actor:
            raise ValueError('Wonderbewijs AIP owner mismatch')
        threshold = struct.unpack('<d', view.read(view.at(aip, 0x250), 8))[0]
        if not math.isfinite(threshold):
            raise ValueError('Nonfinite wonder threshold')
        row['wonder_build_evidence'] = dict(prerequisite=(known(player, prerequisite) if prerequisite >= 0 else None),
            threshold=threshold, native_identity=identity['binding'],
            cities=actor_cities(view, eb, player, actor, civ), engine_admission='UNKNOWN')
    return state


def compose_reader(original_load):
    reader, source = original_load()
    reader.FOLDER = HERE
    old_binding, old_observe = reader.trusted_binding, reader.observe_goal3
    def binding(variant):
        result = old_binding(variant)
        extra = json.loads((HERE/'binding-windows.json').read_text('utf-8'))
        if extra['engine_sha256'] != result['engine']['sha256']:
            raise ValueError('Wonderbewijs engine identity mismatch')
        result['ranges'].extend(extra['ranges'])
        return result
    reader.trusted_binding = binding
    reader.observe_goal3 = lambda read, eb, ab, participants: evidence(
        read, eb, old_observe(read, eb, ab, participants), reader)
    return reader, source


def main():
    options = argparse.ArgumentParser(add_help=False)
    options.add_argument('--manifest', type=Path, required=True)
    if not any(x in sys.argv for x in ('-h', '--help')):
        args, _ = options.parse_known_args()
        verify_pins()
        if args.manifest.read_bytes() != (HERE/'participants.json').read_bytes():
            raise ValueError('Expected pinned c6ba LAND participants')
    base = load_base()
    original_load = base.load_reader
    base.load_reader = lambda: compose_reader(original_load)
    base.main()  # Frozen full stable samples, PID/path/modules/creationtime and VM_READ.


if __name__ == '__main__':
    main()
