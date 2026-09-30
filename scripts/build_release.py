"""Build a source ZIP from the reviewed SHA256 manifest. No application data."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def release_files(root=ROOT):
    tree = ast.parse((root / 'app/server.py').read_text(encoding='utf-8'))
    version = next(ast.literal_eval(n.value) for n in tree.body
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'APP_VERSION' for t in n.targets))
    if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+(?:\.\d+)?', version):
        raise ValueError('Invalid release version')
    manifest = (root / 'SHA256SUMS.txt').read_bytes()
    files = {'SHA256SUMS.txt': manifest}
    for line in manifest.decode('utf-8').splitlines():
        expected, name = line.split('  ', 1)
        path = Path(name)
        if (path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or name in files
                or any(part in ('data', 'demo-runs', '__pycache__') for part in path.parts)
                or path.name == 'credentials.json' or '.sqlite3' in path.name or path.name.startswith('.env')
                or not (root / path).resolve().is_relative_to(root.resolve())):
            raise ValueError('Unsafe release path: ' + name)
        raw = (root / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Checksum mismatch: ' + name)
        files[name] = raw
    return version, files


def build(destination, *, root=ROOT, source_commit=None):
    version, files = release_files(root)
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f'm-anchor-app-local-v{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as output:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo('m-anchor-app/' + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(archive) as check:
        expected = {'m-anchor-app/' + name: raw for name, raw in files.items()}
        if check.testzip() is not None or set(check.namelist()) != set(expected):
            raise ValueError('Archive contents mismatch')
        if any(check.read(name) != raw for name, raw in expected.items()):
            raise ValueError('Archive byte mismatch')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / (archive.name + '.sha256')).write_text(digest + '  ' + archive.name + '\n', encoding='utf-8')
    (destination / 'build-info.json').write_text(json.dumps({
        'schema':'m-anchor-app-build/v1', 'app_version':version,
        'source_commit':source_commit, 'archive':archive.name, 'archive_sha256':digest,
        'source_manifest_sha256':hashlib.sha256(files['SHA256SUMS.txt']).hexdigest(),
        'file_count':len(files), 'archive_verified':True,
    }, indent=2) + '\n', encoding='utf-8')
    print(str(archive.resolve()))
    print(f'{len(files)} files; SHA256 {digest}')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT.parent)
    parser.add_argument('--source-commit')
    args = parser.parse_args()
    build(args.output, source_commit=args.source_commit)
