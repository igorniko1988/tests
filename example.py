import requests

class BaseClient:
    def __init__(self, base_url: str, timeout: float =10.0):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Accept':'application/json'})

    def request(self, method, path, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return self.session.request(method, f'{self.base_url}{path}',**kwargs)

    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def set_token(self, token):
        self.session.headers.update({'Authorizatio': f'Bearer {token}'})

    def clear_token(self):
        self.session.headers.pop('Authorization')

class AuthClient(BaseClient):

    def register(self, email, password):
        return self.post('/users', json={'email': email, 'password': password})

    def authorize(self, email, password):
        return self.post('/user/auth', json={'email': email, 'password': password})
