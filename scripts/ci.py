"""Run the offline checks and preserve per-command logs on either OS."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / '_ci')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    checks = [
        ('app-tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'app', '-v']),
        ('release-tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'scripts', '-p', 'test_release.py', '-v']),
        ('ui-logic', [sys.executable, 'scripts/check_ui.py']),
        ('source-checksums', [sys.executable, '-c', 'import sys;sys.path.insert(0,"scripts");from build_release import release_files;v,f=release_files();print(v,len(f),"files verified")']),
    ]
    report = {'schema':'m-anchor-app-ci/v1', 'source_commit':os.getenv('GITHUB_SHA'),
        'run_id':os.getenv('GITHUB_RUN_ID'), 'run_attempt':os.getenv('GITHUB_RUN_ATTEMPT'),
        'started_at_utc':datetime.now(timezone.utc).isoformat(), 'platform':platform.platform(),
        'python':sys.version, 'scope':'Offline tests with a mock model provider; no real model API calls.', 'checks':[]}
    for name, command in checks:
        start = time.monotonic()
        try:
            result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=180,
                env={**os.environ, 'PYTHONUTF8':'1', 'PYTHONIOENCODING':'utf-8'})
            raw = result.stdout + result.stderr
            code = result.returncode
        except subprocess.TimeoutExpired as error:
            raw = (error.stdout or b'') + (error.stderr or b'') + b'\nCheck timed out.\n'
            code = 124
        (output / (name+'.log')).write_bytes(raw)
        report['checks'].append({'name':name, 'returncode':code, 'seconds':round(time.monotonic()-start,3), 'log':name+'.log'})
        print(name + ': ' + ('PASS' if code == 0 else 'FAIL'), flush=True)
        if code:
            print(raw.decode('utf-8', errors='replace'), flush=True)
    report['passed'] = all(row['returncode'] == 0 for row in report['checks'])
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'ci-report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    summary = '## M-Anchor App checks\n\n| Check | Result | Seconds |\n| --- | --- | --- |\n'
    summary += ''.join('| '+row['name']+' | '+('PASS' if row['returncode']==0 else 'FAIL')+' | '+str(row['seconds'])+' |\n' for row in report['checks'])
    (output / 'summary.md').write_text(summary, encoding='utf-8')
    if os.getenv('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as handle:
            handle.write(summary)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
