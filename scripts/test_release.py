"""Check release integrity failure paths using temporary, synthetic sources."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from build_release import build


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'source'
        (self.root / 'app').mkdir(parents=True)
        (self.root / 'app/server.py').write_bytes(b"APP_VERSION = '0.5'\n")
        (self.root / 'start.cmd').write_bytes(b'@echo off\r\nrem synthetic launcher\r\n')
        self.output = Path(self.temp.name) / 'output'
        self.manifest()

    def tearDown(self):
        self.temp.cleanup()

    def manifest(self):
        names = ['app/server.py', 'start.cmd']
        (self.root / 'SHA256SUMS.txt').write_text(''.join(
            hashlib.sha256((self.root / name).read_bytes()).hexdigest()+'  '+name+'\n'
            for name in names), encoding='utf-8')

    def test_modified_source_blocks_packaging(self):
        (self.root / 'start.cmd').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
            build(self.output, root=self.root)
        self.assertFalse(self.output.exists())

    def test_archive_preserves_bytes_and_excludes_unlisted_credentials(self):
        (self.root / 'credentials.json').write_text('synthetic-secret', encoding='utf-8')
        archive = build(self.output, root=self.root, source_commit='test-commit')
        with zipfile.ZipFile(archive) as z:
            self.assertEqual(z.read('m-anchor-app/start.cmd'), (self.root / 'start.cmd').read_bytes())
            self.assertEqual(len(z.namelist()), 3)
        first = archive.read_bytes()
        build(self.output, root=self.root)
        self.assertEqual(archive.read_bytes(), first)
        info = json.loads((self.output / 'build-info.json').read_text())
        self.assertEqual(info['archive_sha256'], hashlib.sha256(first).hexdigest())

    def test_unsafe_and_duplicate_manifest_entries_rejected(self):
        for name in ['../outside', 'data/state.sqlite3', 'credentials.json', 'app\\server.py', 'C:/outside', 'SHA256SUMS.txt']:
            with self.subTest(name=name):
                (self.root / 'SHA256SUMS.txt').write_text('0'*64+'  '+name+'\n', encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'Unsafe release path'):
                    build(self.output, root=self.root)


if __name__ == '__main__':
    unittest.main(verbosity=2)
