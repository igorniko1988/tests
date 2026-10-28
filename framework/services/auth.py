from framework.transport.api_client import ApiClient

class AuthService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def register(self, email: str, password: str):
        return self.api_client.post('/auth/register', json={'email': email, 'password': password})

    def login(self, email: str, password: str):
        return self.api_client.post('/auth/login', json={'email': email, 'password': password})

    def me(self):
        return self.api_client.get('/me')
