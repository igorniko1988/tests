from framework.services.auth_service import Auth
from framework.transport.api_client import ApiClient

class Api:
    def __init__(self, client: ApiClient):
        self.client = client
        self.auth = Auth(self.client)