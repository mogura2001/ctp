"""Pure finite reader/control admission; no process or memory access."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
CANDIDATE='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
MANIFEST='5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152'
def admit(args,output,gate):
 if gate.get('allowed') is not True:raise ValueError('Separate duration root reader gate required')
 if args.variant!='U30-40' or gate['variant']!='U30-40' or not 0<=args.turn<=26:raise ValueError('Exact candidate T0..T26 only')
 if (args.pid,args.creation_filetime,args.run_id)!=(gate['pid'],gate['creation_filetime'],gate['run_id']) or args.pid<=0 or args.creation_filetime<=0:raise ValueError('Exact PID/creation/run binding')
 if gate['candidate_sha256']!=CANDIDATE or gate['manifest_sha256']!=MANIFEST or gate['turn_min']!=0 or gate['turn_max']!=26:raise ValueError('Exact duration binary/range')
 folder=Path(gate['output_directory']).resolve()
 if folder!=HERE/'variant' or not folder.is_dir() or output.parent!=folder or output.suffix!='.json' or output.exists():raise ValueError('Fresh exact own duration output required')
 if not args.snapshot_label or '/' in args.snapshot_label or '\\' in args.snapshot_label or output.stem!=args.snapshot_label:raise ValueError('Output label mismatch')
 if args.manifest.resolve()!=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json':raise ValueError('Pinned participants only')
 return True
def verify_pins(gate):
 path=HERE/'SOURCE-PINS.json'
 if hashlib.sha256(path.read_bytes()).hexdigest()!=gate['source_pins_sha256']:raise ValueError('Duration source pins changed')
 for row in json.loads(path.read_text('utf-8'))['sources']:
  if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Duration used source changed: '+row['path'])
