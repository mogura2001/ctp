"""Pure finite reader/control admission; no process or memory access."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
CANDIDATE='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'
RELEASE='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
ARMS={'local4':CANDIDATE}
MANIFEST='0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d'
def admit(args,output,gate):
 if gate.get('allowed') is not True:raise ValueError('Separate duration root reader gate required')
 if args.variant not in ARMS or gate['variant']!=args.variant or type(args.turn) is not int or not 0<=args.turn<=100:raise ValueError('Exact two-arm integer T0..T100 only')
 if (args.pid,args.creation_filetime,args.run_id)!=(gate['pid'],gate['creation_filetime'],gate['run_id']) or args.pid<=0 or args.creation_filetime<=0:raise ValueError('Exact PID/creation/run binding')
 if gate['ai_sha256']!=ARMS[args.variant] or gate['manifest_sha256']!=MANIFEST or gate['turn_min']!=0 or gate['turn_max']!=100:raise ValueError('Exact duration binary/range')
 folder=Path(gate['output_directory']).resolve()
 if folder!=HERE/args.variant or not folder.is_dir() or output.parent!=folder or output.suffix!='.json' or output.exists():raise ValueError('Fresh exact own duration output required')
 if not args.snapshot_label or '/' in args.snapshot_label or '\\' in args.snapshot_label or output.stem!=args.snapshot_label:raise ValueError('Output label mismatch')
 if args.manifest.resolve()!=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json':raise ValueError('Pinned participants only')
 return True
def verify_pins(gate):
 path=HERE/'SOURCE-PINS.json'
 if hashlib.sha256(path.read_bytes()).hexdigest()!=gate['source_pins_sha256']:raise ValueError('Duration source pins changed')
 for row in json.loads(path.read_text('utf-8'))['sources']:
  if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Duration used source changed: '+row['path'])
