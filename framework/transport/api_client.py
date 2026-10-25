import allure
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from framework.transport.reporting import report


class ApiClient:
    def __init__(self, base_url, timeout = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = Session()
        retry = Retry(total=3, status_forcelist=[503], backoff_factor=0.5, raise_on_status=False, allowed_methods=None)
        self.session.mount('http://', HTTPAdapter(max_retries=retry))

    def _request(self, method, path, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        with allure.step(f'{method} {path}'):
            response = self.session.request(method, self.base_url + path, **kwargs)
            report(response)
        return response

    def set_token(self, token):
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def clear_token(self):
        self.session.headers.pop('Authorization', None)

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, **kwargs)
