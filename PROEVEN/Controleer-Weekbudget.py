"""Read the current thread's reported weekly and five-hour usage-limit event.

No credentials or conversation contents are printed. This is a sampled guard,
not a server-side hard cap or background monitor. Exit 10 means weekly stop,
5 five-hour stop, 25 weekly warning, 2 unknown/stale, 0 above thresholds.
Account limits are not goal tokens.
"""
import argparse, datetime, json, math
from pathlib import Path

def classify(event, now, max_age):
    if event is None:
        return {'state':'unknown','reason':'no usage event found'}, 2
    timestamp = datetime.datetime.fromisoformat(event['timestamp'].replace('Z','+00:00'))
    age = (now-timestamp).total_seconds()
    if age > max_age or age < -60:
        return {'state':'unknown','reason':'usage event is stale or clock differs',
                'reported_at_utc':event['timestamp'],'age_seconds':round(age,1)}, 2
    limits = event.get('rate_limits') or {}
    windows = {}
    for name in ('primary','secondary'):
        limit = limits.get(name)
        if not isinstance(limit,dict) or limit.get('window_minutes') not in (300,10080):
            continue
        used = limit.get('used_percent')
        if not isinstance(used,(int,float)) or not math.isfinite(used) or not 0 <= used <= 100:
            continue
        key = 'weekly' if limit['window_minutes'] == 10080 else 'five_hour'
        windows[key] = {'remaining_percent':100-used,'used_percent':used,
                        'window_minutes':limit['window_minutes'],
                        'reset_at_unix':limit.get('resets_at')}
    result = {'reported_at_utc':event['timestamp'],'checked_at_utc':now.isoformat(),
              'age_seconds':round(age,1),'windows':windows,'stop_reasons':[]}
    for key,stop in [('weekly',10),('five_hour',5)]:
        if key in windows:
            result[key+'_remaining_percent'] = windows[key]['remaining_percent']
            if windows[key]['remaining_percent'] <= stop:
                result['stop_reasons'].append(key)
    # Any known stop overrides incomplete information about the other window.
    if result['stop_reasons']:
        result['state'] = 'stop'
        return result,10 if 'weekly' in result['stop_reasons'] else 5
    if len(windows) != 2:
        result.update(state='unknown',reason='both weekly and five-hour windows required')
        return result,2
    warning = windows['weekly']['remaining_percent'] <= 25
    result['state'] = 'warn' if warning else 'ok'
    return result,25 if warning else 0

def read_latest(path):
    # Limit reading to the tail of this large local log; skip partial JSON lines.
    with path.open('rb') as f:
        f.seek(0,2)
        length = f.tell()
        f.seek(max(0,length-2*1024*1024))
        lines = f.read().splitlines()
    for line in reversed(lines):
        if b'"token_count"' not in line:
            continue
        try: obj = json.loads(line)
        except (json.JSONDecodeError,UnicodeDecodeError): continue
        payload = obj.get('payload',{})
        if payload.get('type') == 'token_count' and payload.get('rate_limits') is not None:
            return {'timestamp':obj['timestamp'],'rate_limits':payload['rate_limits']}
    return None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--thread',required=True)
    parser.add_argument('--sessions-root',type=Path,default=Path.home()/'.codex/sessions')
    parser.add_argument('--max-age-seconds',type=int,default=120)
    args = parser.parse_args()
    # Restrict the search to this thread; don't accidentally use another account/run.
    paths = list(args.sessions_root.glob('**/rollout-*'+args.thread+'.jsonl'))
    if len(paths) != 1:
        result,code = {'state':'unknown','reason':'expected exactly one log for requested thread'},2
    else:
        try:
            result,code = classify(read_latest(paths[0]),datetime.datetime.now(datetime.timezone.utc),args.max_age_seconds)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            result,code = {'state':'unknown','reason':type(exc).__name__},2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return code

if __name__ == '__main__': raise SystemExit(main())
