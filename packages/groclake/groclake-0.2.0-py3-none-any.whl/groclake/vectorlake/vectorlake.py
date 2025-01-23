from ..utillake import Utillake


class Vectorlake:
    def __init__(self):
        self.utillake = Utillake()

    def generate(self, query):
        api_endpoint = '/vector/generate'
        return self.utillake.call_api(api_endpoint, {'query': query})

    def push(self, payload):
        api_endpoint = '/vector/push'
        return self.utillake.call_api(api_endpoint, payload)

    def search(self, payload):
        api_endpoint = '/vector/search'
        return self.utillake.call_api(api_endpoint, payload)

    def create(self, payload=None):
        api_endpoint = '/vector/create'
        if payload is None:
            payload = {}
        return self.utillake.call_api(api_endpoint, payload)