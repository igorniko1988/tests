from requests.auth import AuthBase
from requests import Response

class TokenApi(AuthBase):
    def __init__(self, token):
        self.token = token


    def __call__(self, request: Response):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request
