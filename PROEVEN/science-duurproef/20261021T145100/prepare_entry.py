"""One-time exact entry adapter; old modules/data remain read-only."""
from pathlib import Path
import hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
old=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/Lees-Uitbreiding.py'
assert hashlib.sha256(old.read_bytes()).hexdigest()=='db164c59641d58487cb35226da4e7485a1e3a891b912abc5b8c6c6772006810c'
target=HERE/'Lees-Duur.py';assert not target.exists()
source=old.read_text('utf-8')
source=source.replace('from original_core import *',"from pathlib import Path\nimport sys\nsys.dont_write_bytecode=True\nOUTPUT_FOLDER=Path(__file__).resolve().parent\nOLD_READER=OUTPUT_FOLDER.parents[1]/'selectie-pad-diagnose/20261020T192500/reader'\nsys.path[:0]=[str(OUTPUT_FOLDER),str(OLD_READER)]\nfrom scope import admit,verify_pins\nfrom original_core import *")
source=source.replace("parser.add_argument('--pid',type=int,required=True)","parser.add_argument('--pid',type=int,required=True)\n    parser.add_argument('--creation-filetime',type=int,required=True)")
source=source.replace("if not output.is_relative_to(FOLDER) or output.suffix!='.json' or output.exists():raise ValueError('Output outside own package or already exists')","gate=json.loads((OUTPUT_FOLDER/'ROOT-READER.json').read_text('utf-8-sig'))\n    admit(args,output,gate);verify_pins(gate)")
start=source.index("    gate=json.loads((FOLDER/'SCIENCE-FOODREADER-ROOT-VRIJGAVE.json')")
end=source.index('    handle=k.OpenProcess',start)
source=source[:start]+source[end:]
needle="if times[1].dwLowDateTime or times[1].dwHighDateTime:raise ValueError('Process exited during snapshot')"
source=source.replace(needle,needle+"\n        if (times[0].dwHighDateTime<<32)|times[0].dwLowDateTime != args.creation_filetime:raise ValueError('Exact duration process creation mismatch')")
target.write_text(source,'utf-8')
