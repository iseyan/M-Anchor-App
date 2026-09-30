"""Application observations. These never authorize a state transition."""
import base64
from datetime import datetime, timezone
import hashlib
import json
import secrets
import threading
import time


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def model_metadata(value):
    """Allow only non-secret provider fields, never an arbitrary request object."""
    if not isinstance(value, dict):
        return {}
    result = {}
    for key in ('model', 'response_id'):
        item = value.get(key)
        if isinstance(item, str) and len(item) <= 200:
            result[key] = item
    for key in ('input_tokens', 'output_tokens'):
        item = value.get(key)
        if type(item) is int and item >= 0:
            result[key] = item
    return result


class ExecutionTickets:
    """Bind server-observed model metadata to one exact loopback submission."""
    def __init__(self):
        self.pending = {}
        self.lock = threading.Lock()

    def issue(self, case_id, raw, metadata, *, exercise=None):
        token = secrets.token_urlsafe(32)
        with self.lock:
            self.pending[token] = (case_id, hashlib.sha256(raw).hexdigest(),
                model_metadata(metadata), time.monotonic() + 60,
                json.loads(json.dumps(exercise)) if exercise is not None else None)
        return token

    def consume(self, token, case_id, raw, *, include_exercise=False):
        with self.lock:
            entry = self.pending.pop(token, None)
        if entry is None or entry[3] <= time.monotonic():
            raise ValueError('invalid_execution_ticket')
        if entry[:2] != (case_id, hashlib.sha256(raw).hexdigest()):
            raise ValueError('invalid_execution_ticket')
        return (entry[2], entry[4]) if include_exercise else entry[2]

    def discard(self, token):
        with self.lock:
            self.pending.pop(token, None)


def history(connection, *, limit=None, audit_id=None, details=False):
    sql = '''SELECT a.*, e.execution_json, e.readback_json
             FROM audit a LEFT JOIN executions e ON a.id=e.audit_id'''
    args = []
    if audit_id is not None:
        sql += ' WHERE a.id=?'
        args.append(audit_id)
    sql += ' ORDER BY a.id DESC'
    if limit is not None:
        sql += ' LIMIT ?'
        args.append(limit)
    entries = []
    for row in connection.execute(sql, args):
        entry = {'id': row['id'], **json.loads(row['decision_json']),
            'execution': json.loads(row['execution_json']) if row['execution_json'] else None,
            'readback': json.loads(row['readback_json']) if row['readback_json'] else None}
        if details:
            raw = row['raw']
            entry['proposal_base64'] = base64.b64encode(raw).decode('ascii')
            try:
                entry['proposal_text'] = raw.decode('utf-8')
            except UnicodeDecodeError:
                entry['proposal_text'] = None
        entries.append(entry)
    return entries
