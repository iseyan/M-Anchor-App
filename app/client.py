"""Agent-side client. No store, shell, bootstrap or administrator operation."""
import json
from urllib.request import Request, urlopen
from urllib.parse import quote

class AnchorClient:
    def __init__(self, agent_token, base_url='http://127.0.0.1:8765'):
        self.base_url = base_url.rstrip('/')
        self.agent_token = agent_token

    def _request(self, path, raw=None):
        if raw is not None and not isinstance(raw, bytes):
            raise TypeError('Supply exact UTF-8 proposal bytes')
        request = Request(self.base_url + path, data=raw, headers={
            'Authorization': 'Bearer ' + self.agent_token,
            'Content-Type': 'application/json'})
        with urlopen(request, timeout=20) as response:
            return json.load(response)

    def state(self, case_id):
        return self._request('/v1/cases/' + quote(case_id, safe=''))

    def propose(self, case_id, raw):
        return self._request('/v1/cases/' + quote(case_id, safe='') + '/proposals', raw)
