"""Weight-only composition of the frozen C3 reader; read-only samples unchanged."""
from pathlib import Path
import hashlib, importlib.util, json, sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE = ROOT/'VERSIES/wondergewicht-2026-10-30'
FROZEN = ROOT/'PROEVEN/wonderbouw-kans/20261029'

def verify_pins():
    manifest = json.loads((HERE/'pins.json').read_text('utf-8'))
    for item in manifest['files']:
        if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Wondergewicht pin changed: '+item['path'])

def weight_expectation(result):
    listing = result['effective_wonder_list']
    active = result['opening_symbols']['opening_required'] == 1
    match = (listing['count'] == 1 and
             listing['records'][0] == dict(weight=30000.0, native_index=2, category=-1))
    return dict(status=('PASS' if match else 'FAIL') if active else 'NOT_APPLICABLE',
        expected='one exact Labyrinth index2/category-1 entry, weight30000',
        package_manifest_sha256=hashlib.sha256((PACKAGE/'manifest.json').read_bytes()).hexdigest(),
        package_pins_sha256=hashlib.sha256((HERE/'pins.json').read_bytes()).hexdigest(),
        legacy_9100_expectation='PRESERVED_HISTORICAL_METADATA_MAY_FAIL')

def load_c3():
    name = '_ctp_wondergewicht_20261030_frozen_c3'
    if name in sys.modules:
        raise ValueError('Wondergewicht composition name occupied')
    spec = importlib.util.spec_from_file_location(name, FROZEN/'Lees-Wonderbouw.py')
    c3 = importlib.util.module_from_spec(spec)
    sys.modules[name] = c3
    spec.loader.exec_module(c3)
    c3.HERE = HERE
    original_c3_load = c3.load_base
    def load_c2():
        c2 = original_c3_load()
        original_c2_load = c2.load_base
        def load_c1():
            c1 = original_c2_load()
            c1.WONDERS = PACKAGE
            original_state = c1.wonder_state
            def weighted_state(read, actor, core):
                result = original_state(read, actor, core)
                result['weight_30000_expectation'] = weight_expectation(result)
                return result
            c1.wonder_state = weighted_state
            return c1
        c2.load_base = load_c1
        return c2
    c3.load_base = load_c2
    return c3

def main():
    if not any(a in sys.argv for a in ('-h', '--help')):
        verify_pins()
    load_c3().main()

if __name__ == '__main__':
    main()
