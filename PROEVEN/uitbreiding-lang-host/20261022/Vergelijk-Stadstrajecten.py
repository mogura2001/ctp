"""Offline samenvatting van het vooraf ontworpen T100-paar; geen speltoegang.

Dit rekent alleen opgeslagen scalars uit. Volledige token-, host- en
herstelacceptatie blijft een afzonderlijke rootreview, ook bij 101 snapshots.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / 'PROEVEN/uitbreiding-lang/20261022T122400'
EXPECTED = {
    'release-v1': 'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890',
    'U30-40': 'df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e',
}
CIVS = tuple(range(2, 9))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_arm(arm):
    rows = []
    identity = None
    sources = []
    for turn in range(101):
        path = PACKAGE / arm / f'T{turn}.json'
        value = json.loads(path.read_text('utf-8-sig'))
        if value.get('stable_twice') is not True or value['variant'] != arm or value['turn'] != turn:
            raise ValueError(f'Unaccepted snapshot {path}')
        if value['binding']['ai_sha256'] != EXPECTED[arm]:
            raise ValueError(f'Wrong DLL {path}')
        current = (value['run_id'], value['instance']['pid'], value['instance']['creationtime_filetime'])
        if identity is None:
            identity = current
        if current != identity:
            raise ValueError(f'Changed process/run {path}')
        civs = sorted(value['state']['civilizations'], key=lambda x: x['civ_id'])
        if tuple(c['civ_id'] for c in civs) != CIVS:
            raise ValueError(f'Wrong participants {path}')
        if any(c['processed_round'] != turn - 1 for c in civs):
            raise ValueError(f'Wrong native round {path}')
        rows.append(civs)
        sources.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)})
    return rows, sources


def summarize(rows):
    result = {}
    for index, civ_id in enumerate(CIVS):
        trajectory = [row[index]['city_count'] for row in rows]
        if any(type(c) is not int or c < 0 for c in trajectory):
            raise ValueError('Invalid city count')
        first = lambda threshold: next((t for t, c in enumerate(trajectory) if c >= threshold), None)
        result[str(civ_id)] = {
            'city_trajectory': trajectory,
            'checkpoints': {str(t): trajectory[t] for t in (25, 26, 50, 100) if t < len(rows)},
            'first_possession_25': first(25),
            'first_possession_30': first(30),
            'first_possession_40': first(40),
            'first_possession_30_and_active_theocracy': next(
                (t for t, c in enumerate(trajectory) if c >= 30 and rows[t][index]['active_government'] == 3), None),
            'active_theocracy_T26': rows[26][index]['active_government'] == 3,
        }
    return result


def main():
    # Exacte veldnamen bevestigd in bestaande echte readeruitvoer.
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.parent != Path(__file__).resolve().parent or output.exists():
        raise ValueError('Fresh own host output required')
    raw = {arm: read_arm(arm) for arm in EXPECTED}
    before = [{k: v for k, v in c.items() if k not in ('ai_actor', 'effective_aip')} for c in raw['release-v1'][0][0]]
    after = [{k: v for k, v in c.items() if k not in ('ai_actor', 'effective_aip')} for c in raw['U30-40'][0][0]]
    # Kandidaat-only stock/producerinformatie is niet gepaard met release.
    if any(any(c[k] != d[k] for k in c) for c, d in zip(before, after)):
        raise ValueError('Shared T0 scalars differ')
    result = {'status': 'OFFLINE_SCALARS_ONLY_FULL_HOST_REVIEW_REQUIRED',
              'full_goal1_complete': False, 'full_goal1a_complete': False,
              'first_threshold_is_possession_not_proven_founding': True,
              'missing_threshold_means_not_reached_within_T100': True,
              'arms': {arm: summarize(data[0]) for arm, data in raw.items()},
              'sources': {arm: data[1] for arm, data in raw.items()}}
    result['T100_delta_per_civ'] = {
        str(c): result['arms']['U30-40'][str(c)]['checkpoints']['100'] - result['arms']['release-v1'][str(c)]['checkpoints']['100'] for c in CIVS}
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
