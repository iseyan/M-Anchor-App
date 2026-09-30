"""Local prototype: raw proposals -> unchanged Stage 3 gate -> SQLite."""
from __future__ import annotations
import argparse
import hmac
import json
import os
from pathlib import Path
import secrets
import sqlite3
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote
from gate import Store, GateError, canonical_json, _validate_authority
from client import AnchorClient
from model_bridge import run_model, ModelError

ROOT = Path(__file__).resolve().parent
MAX_BODY = 65536
APP_VERSION = '0.3'


class LaunchTicket:
    """A single-use, short-lived capability created only by the local launcher."""
    def __init__(self, token=None, lifetime=120):
        self.token = token
        self.expires = time.monotonic() + lifetime
        self.lock = threading.Lock()

    def consume(self, supplied):
        with self.lock:
            if not self.token or time.monotonic() >= self.expires:
                return False
            if not hmac.compare_digest(self.token.encode(), supplied.encode()):
                return False
            self.token = None
            return True

def init_data(directory: Path, authority_path: Path):
    directory.mkdir(parents=True, exist_ok=True)
    # Creation is explicit and never resets an existing store or credentials.
    if (directory / 'state.sqlite3').exists() or (directory / 'credentials.json').exists():
        raise ValueError('Existing data found. Use another data directory; initialization never overwrites it.')
    authority = _validate_authority(json.loads(authority_path.read_text(encoding='utf-8')))
    with Store(directory / 'state.sqlite3') as store:
        store.initialize(authority)
    credentials = {'agent_token': secrets.token_urlsafe(32), 'admin_token': secrets.token_urlsafe(32)}
    path = directory / 'credentials.json'
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as out:
        json.dump(credentials, out, indent=2)
    return credentials

def make_server(directory: Path, port: int, *, launch_ticket=None):
    credentials = json.loads((directory / 'credentials.json').read_text(encoding='utf-8'))
    database = directory / 'state.sqlite3'
    model_lock = threading.Lock()
    ticket = LaunchTicket(launch_ticket)
    # Fail before listening if the core or trusted store cannot be verified.
    with Store(database) as store:
        store.authority_snapshot()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Tokens and raw proposals are never printed to the console.

        def reply(self, status, value, *, html=False):
            payload = value.encode('utf-8') if html else canonical_json(value).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'text/html; charset=utf-8' if html else 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(payload)

        def boundary(self):
            expected = f'127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host') != expected:
                self.reply(403, {'error': 'invalid_host'})
                return False
            origin = self.headers.get('Origin')
            if origin is not None and origin != 'http://' + expected:
                self.reply(403, {'error': 'invalid_origin'})
                return False
            return True

        def authorized(self, role):
            actual = self.headers.get('Authorization', '')
            expected = 'Bearer ' + credentials[role + '_token']
            if not hmac.compare_digest(actual.encode('utf-8'), expected.encode('utf-8')):
                self.reply(401, {'error': 'unauthorized'})
                return False
            return True

        def do_GET(self):
            if not self.boundary():
                return
            path = urlsplit(self.path).path
            if path == '/':
                self.reply(200, (ROOT / 'ui.html').read_text(encoding='utf-8'), html=True)
                return
            role = 'admin' if path.startswith('/admin/') else 'agent'
            if not self.authorized(role):
                return
            try:
                with Store(database) as store:
                    if path == '/admin/cases':
                        self.reply(200, store.authority_snapshot())
                    elif path == '/admin/history':
                        rows = store.connection.execute('SELECT id,decision_json FROM audit ORDER BY id DESC LIMIT 100').fetchall()
                        self.reply(200, [{'id': row[0], **json.loads(row[1])} for row in rows])
                    elif path == '/admin/info':
                        self.reply(200, {'app_version': APP_VERSION, 'data_label': directory.name})
                    elif path == '/admin/report':
                        # SQLite backup gives an internally consistent, immutable copy.
                        # The original Gate owns its transactions and stays unchanged.
                        with Store(':memory:') as frozen:
                            store.connection.backup(frozen.connection)
                            authority = frozen.authority_snapshot()
                            rows = frozen.connection.execute('SELECT id,decision_json FROM audit ORDER BY id DESC LIMIT 100').fetchall()
                        self.reply(200, {
                            'schema': 'm-anchor-app-observation/v1', 'app_version': APP_VERSION,
                            'generated_at_utc': datetime.now(timezone.utc).isoformat(),
                            'data_label': directory.name,
                            'scope': 'Local case records; not evidence-truth verification or external tool control.',
                            'authority': authority,
                            'history_limit': 100,
                            'history': [{'id': row[0], **json.loads(row[1])} for row in rows],
                            'history_source_note': 'Audit entries alone do not identify whether a proposal came from a model or a fixed demo.',
                        })
                    elif path.startswith('/v1/cases/') and len(path.split('/')) == 4:
                        case_id = unquote(path.split('/')[3])
                        authority = store.authority_snapshot()
                        state = next((s for s in authority['cases'] if s['case_id'] == case_id), None)
                        if state is None:
                            self.reply(404, {'error': 'unknown_case'})
                            return
                        admitted = {a['evidence_id'] for a in authority['admissions'] if a['case_id'] == case_id}
                        self.reply(200, {'state': state,
                            'evidence': [e for e in authority['evidence'] if e['evidence_id'] in admitted],
                            'interpretations': [i for i in authority['interpretations'] if i['case_id'] == case_id]})
                    else:
                        self.reply(404, {'error': 'unknown_route'})
            except (GateError, sqlite3.Error):
                self.reply(503, {'error': 'store_unavailable', 'decision': 'undetermined'})

        def do_POST(self):
            if not self.boundary():
                return
            path = urlsplit(self.path).path
            model_job = path == '/admin/model-run'
            session_job = path == '/launch-session'
            if session_job and self.headers.get('Origin') != f'http://127.0.0.1:{self.server.server_port}':
                self.reply(403, {'error': 'invalid_origin'})
                return
            if not session_job and not self.authorized('admin' if model_job else 'agent'):
                return
            parts = path.split('/')
            if not (model_job or session_job) and (len(parts) != 5 or parts[:3] != ['', 'v1', 'cases'] or parts[4] != 'proposals'):
                self.reply(404, {'error': 'unknown_route'})
                return
            if self.headers.get('Transfer-Encoding'):
                self.close_connection = True
                self.reply(400, {'error': 'transfer_encoding_not_supported'})
                return
            try:
                length = int(self.headers.get('Content-Length', '-1'))
            except ValueError:
                length = -1
            if not 0 < length <= MAX_BODY:
                self.close_connection = True
                self.reply(413, {'error': 'body_size', 'max_bytes': MAX_BODY})
                return
            if self.headers.get('Content-Type', '').split(';')[0].strip() != 'application/json':
                self.reply(415, {'error': 'json_required'})
                return
            self.connection.settimeout(10)
            try:
                raw = self.rfile.read(length)
                if len(raw) != length:
                    self.reply(400, {'error': 'incomplete_body'})
                    return
                if session_job:
                    if raw != b'{}':
                        self.reply(400, {'error': 'invalid_launch_request'})
                    elif ticket.consume(self.headers.get('X-Launch-Ticket', '')):
                        self.reply(200, credentials)
                    else:
                        self.reply(401, {'error': 'launch_expired'})
                    return
                if model_job:
                    if not model_lock.acquire(blocking=False):
                        self.reply(409, {'error':'model_busy'})
                        return
                    try:
                        job = json.loads(raw.decode('utf-8'))
                        client = AnchorClient(credentials['agent_token'],
                            f'http://127.0.0.1:{self.server.server_port}')
                        result = run_model(job, client)
                        self.reply(200, result)
                    except ModelError as exc:
                        self.reply(502, {'error':exc.code,'decision':'undetermined'})
                    except (ValueError,UnicodeError,TypeError):
                        self.reply(400, {'error':'invalid_model_request'})
                    finally:
                        model_lock.release()
                    return
                with Store(database) as store:
                    decision = store.apply(raw, expected_case_id=unquote(parts[3]))
                # Independent readback, rather than trusting only apply's return.
                if decision['after'] is not None:
                    with Store(database) as store:
                        persisted = store.snapshot(decision['case_id'])
                    if persisted != decision['after']:
                        self.reply(503, {'decision': 'undetermined', 'error': 'readback_mismatch'})
                        return
                self.reply(200, {**decision, 'state_changed': decision['decision'] == 'commit',
                    'readback_verified': decision['after'] is not None})
            except (GateError, sqlite3.Error, TimeoutError):
                self.reply(503, {'decision': 'undetermined', 'error': 'store_or_request_unavailable'})

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    return server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=ROOT.parent / 'data')
    sub = parser.add_subparsers(dest='command', required=True)
    initialize = sub.add_parser('init')
    initialize.add_argument('--authority', type=Path, default=ROOT / 'demo-authority.json')
    serve = sub.add_parser('serve')
    serve.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if args.command == 'init':
        init_data(args.data, args.authority)
        print('Initialized. Credentials are in the data directory. No model is connected.')
    else:
        server = make_server(args.data, args.port)
        print(f'M-Anchor App v{APP_VERSION}: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)')
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()

if __name__ == '__main__':
    main()
