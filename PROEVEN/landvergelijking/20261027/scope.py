"""Pure finite reader/control admission; no process or memory access."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
CANDIDATE='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
RELEASE='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
ARMS={'release-v1':RELEASE,'U30-40':CANDIDATE}
MANIFEST='5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152'
def admit(args,output,gate):
 if gate.get('allowed') is not True:raise ValueError('Separate duration root reader gate required')
 if args.variant not in ARMS or gate['variant']!=args.variant or type(args.turn) is not int or not 0<=args.turn<=100:raise ValueError('Exact two-arm integer T0..T100 only')
 if (args.pid,args.creation_filetime,args.run_id)!=(gate['pid'],gate['creation_filetime'],gate['run_id']) or args.pid<=0 or args.creation_filetime<=0:raise ValueError('Exact PID/creation/run binding')
 if gate['ai_sha256']!=ARMS[args.variant] or gate['manifest_sha256']!=MANIFEST or gate['turn_min']!=0 or gate['turn_max']!=100:raise ValueError('Exact duration binary/range')
 folder=Path(gate['output_directory']).resolve()
 if folder!=HERE/args.variant or not folder.is_dir() or output.parent!=folder or output.suffix!='.json' or output.exists():raise ValueError('Fresh exact own duration output required')
 if not args.snapshot_label or '/' in args.snapshot_label or '\\' in args.snapshot_label or output.stem!=args.snapshot_label:raise ValueError('Output label mismatch')
 if args.manifest.resolve()!=ROOT/'PROEVEN/landbenchmark/20261027/participants.json':raise ValueError('Pinned participants only')
 return True
def verify_pins(gate):
 path=HERE/'SOURCE-PINS.json'
 if hashlib.sha256(path.read_bytes()).hexdigest()!=gate['source_pins_sha256']:raise ValueError('Duration source pins changed')
 for row in json.loads(path.read_text('utf-8'))['sources']:
  if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Duration used source changed: '+row['path'])
