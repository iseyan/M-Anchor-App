"""Run offline UI logic checks. Requires Node.js; no browser or real model call."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import threading
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from server import ROOT, init_data, make_server
from model_bridge import run_model, ModelError


def fake_run(job, client, **kwargs):
    if job['message'] == '__mock_failure__':
        raise ModelError('api_connection_or_timeout')
    def provider(key, model, context, message):
        state=context['state']
        proposal={
            'case_id':state['case_id'],'referenced_version':state['version'],
            'referenced_hash':state['state_hash'],'retained_candidates':state['candidates'],
            'cause_status':state['cause_status'],'evidence_used':[],
            'proposed_version_advance':False,'future_bypass_authorized':False,
        }
        return json.dumps(proposal), {'model':'mock-test-only','response_id':'mock-only'}
    return run_model(job,client,provider,**kwargs)


with tempfile.TemporaryDirectory() as directory:
    data=Path(directory)
    init_data(data,ROOT/'demo-authority.json')
    server=make_server(data,0,launch_ticket='ui-test-ticket')
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        with patch('server.run_model',side_effect=fake_run):
            result=subprocess.run(['node',str(Path(__file__).with_suffix('.cjs')),
                f'http://127.0.0.1:{server.server_port}'],check=False,timeout=30)
    finally:
        server.shutdown();server.server_close();thread.join()
    sys.exit(result.returncode)
