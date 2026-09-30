"""Initialize or reuse local data, wait for HTTP readiness, then open the UI."""
from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import secrets
import threading
from urllib.request import build_opener, ProxyHandler
import webbrowser
from server import APP_VERSION, ROOT, init_data, make_server


def prepare_data(root: Path, *, fresh=False, directory=None):
    if fresh:
        parent = root / 'demo-runs'
        parent.mkdir(parents=True, exist_ok=True)
        target = parent / (datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + secrets.token_hex(3))
        target.mkdir()  # Never reuse a previous demo directory.
    else:
        target = Path(directory) if directory is not None else root / 'data'
    database, credentials = target / 'state.sqlite3', target / 'credentials.json'
    if not database.exists() and not credentials.exists():
        init_data(target, ROOT / 'demo-authority.json')
    elif not database.is_file() or not credentials.is_file():
        raise ValueError('Incomplete data directory. Restore the complete data folder or choose a new one.')
    return target


def open_when_ready(server, ticket, opener=webbrowser.open):
    base = f'http://127.0.0.1:{server.server_port}'
    with build_opener(ProxyHandler({})).open(base + '/', timeout=5) as response:
        if response.status != 200:
            raise RuntimeError('Local server did not become ready.')
    # The fragment is not sent in HTTP requests; the UI removes it immediately.
    # It holds a one-use launch ticket, never a persistent admin/API key.
    return opener(base + '/#launch=' + ticket)


def main():
    parser = argparse.ArgumentParser(description='Start M-Anchor App and connect the local browser.')
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument('--fresh-demo', action='store_true')
    choice.add_argument('--data', type=Path)
    parser.add_argument('--port', type=int, default=0, help='0 chooses an available loopback port.')
    args = parser.parse_args()
    directory = prepare_data(ROOT.parent, fresh=args.fresh_demo, directory=args.data)
    ticket = secrets.token_urlsafe(32)
    server = make_server(directory, args.port, launch_ticket=ticket)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    print(f'M-Anchor App v{APP_VERSION}', flush=True)
    print(f'Data: {directory.resolve()}', flush=True)
    print(f'Address: http://127.0.0.1:{server.server_port}', flush=True)
    print('Keep this window open. Press Ctrl+C to stop.', flush=True)
    try:
        try:
            opened = open_when_ready(server, ticket)
        except Exception:
            opened = False
        if not opened:
            print('Open the address above and enter the keys from credentials.json in the data folder.', flush=True)
        while worker.is_alive():
            worker.join(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
        worker.join()


if __name__ == '__main__':
    main()
