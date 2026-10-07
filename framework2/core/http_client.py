import time
import logging
import requests
from requests.adapters import HTTPAdapter
from pprint import pprint
from urllib3.util.retry import Retry
import time
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('headers')

SECRET_HEADERS = {'authorization', 'cookie'}

def hide_secrets(headers: dict):
    safe = {k:'****' if k.lower() in SECRET_HEADERS else v for k,v in headers.items()}
    return safe

def _build_adapter() -> HTTPAdapter:
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=(502,503,504),
        allowed_methods=frozenset({'GET','PUT','DELETE'}),
        raise_on_status=False
    )

    return HTTPAdapter(max_retries=retry)



class HttpClient:
    def __init__(self, base_url: str, timeout=10, auth = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._session = requests.Session()
        self._session.auth = auth

        adapter = _build_adapter()
        self._session.mount('http://',adapter)

    def request(self, method,  path: str, **kwargs):
        url = f"{self.base_url}{path}"
        response =  self._session.request(method,url, **kwargs)
        self._log(response)
        return response

    def _log(self, response: requests.Response):
        request = response.request
        log.debug(f'Hide request headers{hide_secrets(request.headers)}')
        log.debug(f'Response status {response.status_code}')


    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('DELETE', path , **kwargs)

    def patch(self, path, **kwargs):
        return self.request('PATCH', path, **kwargs)

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
