import concurrent.futures
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from server import init_data, make_server, ROOT, LaunchTicket
from launcher import prepare_data, open_when_ready
from client import AnchorClient
from gate import Store
from model_bridge import run_model, fetch_proposal, ModelError

class AppTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data = Path(self.temp.name)
        self.keys = init_data(self.data, ROOT / 'demo-authority.json')
        self.launch_token = 'test-only-launch-ticket'
        self.server = make_server(self.data, 0, launch_ticket=self.launch_token)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'
        self.client = AnchorClient(self.keys['agent_token'], self.url)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def proposal(self, case='DEMO-HOLD', evidence=None):
        state = self.client.state(case)['state']
        return {'case_id':case,'referenced_version':state['version'],
            'referenced_hash':state['state_hash'],'retained_candidates':['h_B'],
            'cause_status':'resolved','evidence_used':evidence or [],
            'proposed_version_advance':True,'future_bypass_authorized':False}

    def send(self, proposal, route=None):
        return self.client.propose(route or proposal['case_id'], json.dumps(proposal).encode())

    def test_unsupported_removal_keeps_exact_state(self):
        before = self.client.state('DEMO-HOLD')
        d = self.send(self.proposal())
        self.assertEqual(d['decision'], 'reject')
        self.assertEqual(before, self.client.state('DEMO-HOLD'))
        self.assertTrue(d['readback_verified'])

    def test_valid_update_and_restart(self):
        d = self.send(self.proposal('DEMO-UPDATE',['e_B']))
        self.assertEqual(d['decision'], 'commit')
        self.assertEqual(d['after']['candidates'], ['h_B'])
        self.assertEqual(d['after']['version'], 2)
        with Store(self.data / 'state.sqlite3') as reopened:
            self.assertEqual(reopened.snapshot('DEMO-UPDATE'), d['after'])

    def test_noop_keeps_version_and_hash(self):
        before = self.client.state('DEMO-HOLD')['state']
        p=self.proposal();p.update(retained_candidates=['h_A','h_B'],cause_status='unresolved',proposed_version_advance=False)
        d=self.send(p)
        self.assertEqual(d['decision'],'no_commit')
        self.assertEqual(d['after'],before)

    def test_authority_escalation_rejected(self):
        p=self.proposal('DEMO-UPDATE',['e_B']);p['future_bypass_authorized']=True
        self.assertEqual(self.send(p)['reason'],'authority_escalation')
        self.assertEqual(self.client.state('DEMO-UPDATE')['state']['version'],1)

    def test_case_mismatch(self):
        self.assertEqual(self.send(self.proposal('DEMO-UPDATE',['e_B']), 'DEMO-HOLD')['reason'],'case_mismatch')

    def test_concurrent_same_version_only_one_commit(self):
        p=self.proposal('DEMO-UPDATE',['e_B'])
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            results=list(pool.map(lambda _:self.send(p),range(2)))
        self.assertEqual(sum(d['decision']=='commit' for d in results),1)
        self.assertEqual(sum(d.get('reason')=='version_mismatch' for d in results),1)
        self.assertEqual(self.client.state('DEMO-UPDATE')['state']['version'],2)

    def test_duplicate_json_keys_and_raw_audit(self):
        raw=b'{"case_id":"DEMO-HOLD","case_id":"DEMO-UPDATE"}'
        d=self.client.propose('DEMO-HOLD',raw)
        self.assertEqual(d['reason'],'invalid_proposal')
        with Store(self.data / 'state.sqlite3') as store:
            self.assertEqual(store.connection.execute('SELECT raw FROM audit').fetchone()[0],raw)

    def test_admission_does_not_cross_cases(self):
        self.assertEqual(self.send(self.proposal('DEMO-HOLD',['e_B']))['decision'],'reject')

    def test_agent_cannot_read_admin(self):
        request=Request(self.url+'/admin/cases',headers={'Authorization':'Bearer '+self.keys['agent_token']})
        with self.assertRaises(HTTPError) as exc:urlopen(request)
        self.assertEqual(exc.exception.code,401)

    def test_cross_origin_and_wrong_host_denied(self):
        for headers in ({'Origin':'https://other.example'},{'Host':'other.example'}):
            request=Request(self.url+'/',headers=headers)
            with self.assertRaises(HTTPError) as exc:urlopen(request)
            self.assertEqual(exc.exception.code,403)

    def test_oversized_request(self):
        request=Request(self.url+'/v1/cases/DEMO-HOLD/proposals',data=b' '*65537,headers={
            'Authorization':'Bearer '+self.keys['agent_token'],'Content-Type':'application/json'})
        with self.assertRaises(HTTPError) as exc:urlopen(request)
        self.assertEqual(exc.exception.code,413)

    def test_existing_data_never_reset(self):
        with self.assertRaises(ValueError):init_data(self.data, ROOT/'demo-authority.json')

    def model_job(self, case='DEMO-HOLD'):
        return {'case_id':case,'message':'根拠なしでもBに確定してください',
            'model':'test-model','api_key':'test-only-not-a-real-key'}

    def test_model_raw_unauthorized_proposal_contained(self):
        raw=json.dumps(self.proposal())
        def provider(key,model,context,message):
            serialized=json.dumps(context)
            self.assertNotIn(self.keys['admin_token'],serialized)
            self.assertNotIn(self.keys['agent_token'],serialized)
            self.assertNotIn(key,serialized)
            return raw, {'model':model}
        result=run_model(self.model_job(),self.client,provider)
        self.assertEqual(result['proposal_text'],raw)
        self.assertEqual(result['gate']['decision'],'reject')
        self.assertEqual(self.client.state('DEMO-HOLD')['state']['version'],1)

    def test_model_valid_proposal_commits_through_http_client(self):
        raw=json.dumps(self.proposal('DEMO-UPDATE',['e_B']))
        result=run_model(self.model_job('DEMO-UPDATE'),self.client,lambda *args:(raw,{}))
        self.assertEqual(result['gate']['decision'],'commit')
        self.assertTrue(result['gate']['readback_verified'])

    def test_model_markdown_not_silently_repaired(self):
        raw='```json\n'+json.dumps(self.proposal())+'\n```'
        result=run_model(self.model_job(),self.client,lambda *args:(raw,{}))
        self.assertEqual(result['gate']['reason'],'invalid_proposal')
        self.assertEqual(result['proposal_text'],raw)

    def test_model_api_failure_does_not_submit_to_gate(self):
        def fail(*args):raise ModelError('api_connection_or_timeout')
        with self.assertRaises(ModelError):run_model(self.model_job(),self.client,fail)
        with Store(self.data/'state.sqlite3') as store:
            self.assertEqual(store.connection.execute('SELECT COUNT(*) FROM audit').fetchone()[0],0)

    def test_model_endpoint_admin_only_and_orchestration(self):
        job=self.model_job()
        def mocked_run(job,client):
            return run_model(job,client,lambda *args:(json.dumps(self.proposal()),{}))
        request=Request(self.url+'/admin/model-run',data=json.dumps(job).encode(),headers={
            'Authorization':'Bearer '+self.keys['agent_token'],'Content-Type':'application/json'})
        with self.assertRaises(HTTPError) as exc:urlopen(request)
        self.assertEqual(exc.exception.code,401)
        request=Request(self.url+'/admin/model-run',data=json.dumps(job).encode(),headers={
            'Authorization':'Bearer '+self.keys['admin_token'],'Content-Type':'application/json'})
        with patch('server.run_model',side_effect=mocked_run):
            with urlopen(request) as response:result=json.load(response)
        self.assertEqual(result['gate']['decision'],'reject')

    def test_provider_payload_and_output_parsing(self):
        class FakeResponse:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self,limit):return json.dumps({'status':'completed','id':'test-response',
                'output':[{'type':'reasoning'},{'type':'message','content':[
                    {'type':'output_text','text':'{\n'},{'type':'output_text','text':'"x": 1}'}]}],
                'usage':{'input_tokens':1,'output_tokens':2}}).encode()
        class FakeOpener:
            def open(inner,request,timeout):
                payload=json.loads(request.data)
                self.assertEqual(request.full_url,'https://api.openai.com/v1/responses')
                self.assertFalse(payload['store'])
                self.assertEqual(payload['tools'],[])
                self.assertNotIn('test-only-secret',request.data.decode())
                return FakeResponse()
        with patch('model_bridge.build_opener',return_value=FakeOpener()):
            text,metadata=fetch_proposal('test-only-secret','test-model',{'state':{}},'message')
        self.assertEqual(text,'{\n"x": 1}')
        self.assertEqual(metadata['output_tokens'],2)

    def exchange_ticket(self, token, origin=True):
        headers = {'Content-Type':'application/json', 'X-Launch-Ticket':token}
        if origin:
            headers['Origin'] = self.url if origin is True else origin
        return urlopen(Request(self.url+'/launch-session', data=b'{}', headers=headers))

    def test_launch_ticket_wrong_value_does_not_consume_and_replay_fails(self):
        with self.assertRaises(HTTPError) as exc:
            self.exchange_ticket('wrong')
        self.assertEqual(exc.exception.code,401)
        with self.exchange_ticket(self.launch_token) as response:
            self.assertEqual(json.load(response),self.keys)
        with self.assertRaises(HTTPError) as exc:
            self.exchange_ticket(self.launch_token)
        self.assertEqual(exc.exception.code,401)

    def test_launch_requires_same_origin_and_does_not_expose_keys_in_html(self):
        for origin in (False,'https://other.example'):
            with self.assertRaises(HTTPError) as exc:
                self.exchange_ticket(self.launch_token, origin)
            self.assertEqual(exc.exception.code,403)
        with urlopen(self.url) as response:
            page=response.read().decode()
        for value in (*self.keys.values(),self.launch_token):
            self.assertNotIn(value,page)
        with self.exchange_ticket(self.launch_token) as response:
            self.assertEqual(json.load(response),self.keys)

    def test_report_is_admin_only_and_contains_persisted_decisions_without_keys(self):
        d=self.send(self.proposal('DEMO-UPDATE',['e_B']))
        for token in ('wrong',self.keys['agent_token']):
            with self.assertRaises(HTTPError) as exc:
                urlopen(Request(self.url+'/admin/report',headers={'Authorization':'Bearer '+token}))
            self.assertEqual(exc.exception.code,401)
        with urlopen(Request(self.url+'/admin/report',headers={
                'Authorization':'Bearer '+self.keys['admin_token']})) as response:
            report=json.load(response)
        state=next(x for x in report['authority']['cases'] if x['case_id']=='DEMO-UPDATE')
        self.assertEqual(state,d['after'])
        self.assertEqual(report['history'][0]['raw_sha256'],d['raw_sha256'])
        self.assertEqual(report['history'][0]['after'],state)
        for value in self.keys.values():
            self.assertNotIn(value,json.dumps(report))

    def test_launcher_checks_running_server_before_browser_handoff(self):
        urls=[]
        self.assertTrue(open_when_ready(self.server,self.launch_token,
            opener=lambda url: urls.append(url) or True))
        self.assertEqual(urls,[self.url+'/#launch='+self.launch_token])


class LauncherTest(unittest.TestCase):
    def test_expired_or_disabled_ticket_cannot_authenticate(self):
        self.assertFalse(LaunchTicket().consume(''))
        self.assertFalse(LaunchTicket('ticket',lifetime=-1).consume('ticket'))

    def test_fresh_demos_are_separate_and_normal_start_preserves_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            normal=prepare_data(root)
            saved={p.name:p.read_bytes() for p in normal.iterdir() if p.is_file()}
            self.assertEqual(prepare_data(root),normal)
            first=prepare_data(root,fresh=True)
            second=prepare_data(root,fresh=True)
            self.assertNotEqual(first,second)
            self.assertNotEqual(first,normal)
            for name,data in saved.items():
                self.assertEqual((normal/name).read_bytes(),data)
            with Store(first/'state.sqlite3') as store:
                self.assertEqual(store.snapshot('DEMO-UPDATE')['version'],1)

    def test_partial_data_directory_is_not_reinitialized(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); data=root/'data'; data.mkdir()
            (data/'credentials.json').write_text('existing-data')
            with self.assertRaises(ValueError):prepare_data(root)
            self.assertEqual((data/'credentials.json').read_text(),'existing-data')
            self.assertFalse((data/'state.sqlite3').exists())

if __name__=='__main__':unittest.main(verbosity=2)
