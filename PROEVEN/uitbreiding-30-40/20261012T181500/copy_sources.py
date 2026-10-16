"""One-time owned source copy, no emission/runtime. Existing sources read-only."""
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
for source,target in [('native.py','native.py'),('integration.py','integration_base.py'),('input-pins.py','input-pins.py')]:
 dest=OUT/target
 assert not dest.exists(),dest
 dest.write_bytes((ROOT/'PROEVEN/settler-b4'/source).read_bytes())
print('Copied 3 owned sources, originals untouched')
