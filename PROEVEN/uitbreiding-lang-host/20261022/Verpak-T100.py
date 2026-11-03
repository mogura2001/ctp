"""Copy the already tested candidate and accepted evidence; no installation."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / 'VERSIES/uitbreiding-2026-10-22'
OUT = ROOT / 'VERSIES/uitbreiding-2026-10-22-T100'
HOST = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def copy_exact(source, target, expected=None):
    data = source.read_bytes()
    digest = sha(data)
    if expected is not None and digest != expected:
        raise ValueError(f'Source hash mismatch: {source}')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != data:
            raise ValueError(f'Refuse to overwrite differing file: {target}')
    else:
        target.write_bytes(data)
    assert sha(target.read_bytes()) == digest
    return digest

def main():
    previous = json.loads((OLD / 'manifest.json').read_text(encoding='utf-8-sig'))
    comparison = json.loads((HOST / 'VERGELIJKING.json').read_text(encoding='utf-8-sig'))
    # Root review is a separate prerequisite, not inferred from city counts.
    review = json.loads((HOST / 'ROOT-T100-REVIEW.json').read_text(encoding='utf-8-sig'))
    if review.get('accepted_fixed_start_endpoint_comparison') is not True:
        raise ValueError('Root acceptance missing')
    files = previous['files']
    if len(files) != 19:
        raise ValueError('Unexpected candidate file count')
    for entry in files:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Invalid package path')
        copy_exact(OLD / 'files' / relative, OUT / 'files' / relative, entry['sha256'])
    sources = {
        'vergelijking.json': HOST / 'VERGELIJKING.json',
        'controle.json': HOST / 'release-v1/CONTROL-REVIEW.json',
        'kandidaat-host.json': HOST / 'U30-40/HOST-PROOF.json',
        'rootreview.json': HOST / 'ROOT-T100-REVIEW.json',
        'resultaat.md': ROOT / 'ANALYSE/UITBREIDING-T100-RESULTAAT-2026-10-22.md',
    }
    proofs = {name: {'source': str(path.relative_to(ROOT)),
                     'sha256': copy_exact(path, OUT / 'bewijs' / name)}
              for name, path in sources.items()}
    manifest = {
        'stage': 'EXPERIMENTAL_FIXED_START_T100_ENDPOINT_COMPARISON',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'game': 'CTP I', 'difficulty': 'Deity',
        'candidate_sha256': previous['candidate_sha256'],
        'files': files, 'proofs': proofs,
        'control_T100_cities': [14, 14, 15, 4, 13, 14, 12],
        'candidate_T100_cities': [17, 20, 17, 12, 20, 21, 14],
        'active_Theocracy_at_T100': {'control': 7, 'candidate': 7},
        'full_goal1_1a_complete': False,
        'production_install_performed': False,
        'limitations': [
            'One fixed start, one long control and one long candidate.',
            'Manual control has T0/T100 only; no intermediate threshold times.',
            'Candidate has 101 snapshots, 100 natural steps, two proven preinput stops.',
            'No candidate reaches25/30/40; useful founding and adaptive stop/resume remain open.',
            'City possession counts do not prove individual foundings or causal mechanism.',
        ],
    }
    target = OUT / 'manifest.json'
    if target.exists():
        raise ValueError('Package manifest already exists; no overwrite')
    target.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(files), 'proofs': len(proofs),
                      'manifest_sha256': sha(target.read_bytes()),
                      'path': str(OUT)}, indent=2))

if __name__ == '__main__':
    main()
