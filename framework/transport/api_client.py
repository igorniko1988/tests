from requests import Session

class ApiClient:
    def __init__(self, base_url, timeout = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = Session()

    def _request(self, method, path, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        url = self.base_url + path
        return self.session.request(method, url, **kwargs)

    def set_token(self, token):
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def clear_token(self):
        self.session.headers.pop('Authorization', None)

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)


