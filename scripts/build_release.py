"""Build a source ZIP from the reviewed SHA256 manifest. No application data."""
import argparse
import ast
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(destination):
    tree = ast.parse((ROOT / 'app/server.py').read_text(encoding='utf-8'))
    version = next(ast.literal_eval(n.value) for n in tree.body
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'APP_VERSION' for t in n.targets))
    manifest = (ROOT / 'SHA256SUMS.txt').read_bytes()
    files = {'SHA256SUMS.txt': manifest}
    for line in manifest.decode('utf-8').splitlines():
        expected, name = line.split('  ', 1)
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or any(part in ('data', 'demo-runs', '__pycache__') for part in path.parts):
            raise ValueError('Unsafe release path: ' + name)
        raw = (ROOT / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Checksum mismatch: ' + name)
        files[name] = raw
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f'm-anchor-app-local-v{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as output:
        for name, raw in sorted(files.items()):
            output.writestr('m-anchor-app/' + name, raw)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    print(str(archive.resolve()))
    print(f'{len(files)} files; SHA256 {digest}')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT.parent)
    build(parser.parse_args().output)
