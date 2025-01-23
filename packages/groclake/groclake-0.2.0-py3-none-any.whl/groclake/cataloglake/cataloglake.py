from ..utillake import Utillake


class Cataloglake():
    def __init__(self):
        self.utillake=Utillake()

    def fetch(self, payload):
        api_endpoint = '/cataloglake/catalog/fetch'
        return self.utillake.call_api(api_endpoint, payload)

    def push(self, payload):
        api_endpoint = '/cataloglake/catalog/push'
        return self.utillake.call_api(api_endpoint, payload)

    def create_mapper(self, payload):
        api_endpoint = '/cataloglake/catalog/metadata/createmapper'
        return self.utillake.call_api(api_endpoint, payload)

    def convert_mapper(self, payload):
        api_endpoint = '/cataloglake/catalog/metadata/convert'
        return self.utillake.call_api(api_endpoint, payload)

    def gen(self, payload):
        api_endpoint = '/cataloglake/catalog/gen'
        return self.utillake.call_api(api_endpoint, payload)

    def recommend(self, payload):
        api_endpoint = '/cataloglake/catalog/recommender/fetch'
        return self.utillake.call_api(api_endpoint, payload)

    def search(self, payload):
        api_endpoint = '/cataloglake/catalog/search/fetch'
        return self.utillake.call_api(api_endpoint, payload)

    def update(self, payload):
        api_endpoint = '/cataloglake/catalog/update'
        return self.utillake.call_api(api_endpoint, payload)

    def update_inventory(self, payload):
        api_endpoint = '/cataloglake/catalog/inventoryUpdate'
        return self.utillake.call_api(api_endpoint, payload)

    def fetch_inventory(self, payload):
        api_endpoint = '/cataloglake/catalog/inventoryFetch'
        return self.utillake.call_api(api_endpoint, payload)

    def update_price(self, payload):
        api_endpoint = '/cataloglake/catalog/priceUpdate'
        return self.utillake.call_api(api_endpoint, payload)

    def fetch_price(self, payload):
        api_endpoint = '/cataloglake/catalog/priceFetch'
        return self.utillake.call_api(api_endpoint, payload)

    def cache_image(self, payload):
        api_endpoint = '/cataloglake/catalog/imageCache'
        return self.utillake.call_api(api_endpoint, payload)

    def create(self, payload=None):
        api_endpoint = '/cataloglake/catalog/create'
        if not payload:
            payload={}
        return self.utillake.call_api(api_endpoint, payload)

    def cache(self, payload):
        api_endpoint = '/cataloglake/catalog/cache'
        return self.utillake.call_api(api_endpoint, payload)

    def send(self, payload):
        api_endpoint = '/cataloglake/catalog/send'
        return self.utillake.call_api(api_endpoint, payload)

    def delete(self, payload):
        api_endpoint = '/cataloglake/catalog/delete'
        return self.utillake.call_api(api_endpoint, payload)

    def search_intent_fetch(self, payload):
        api_endpoint = '/cataloglake/catalog/search/intent/fetch'
        return self.utillake.call_api(api_endpoint, payload)

    def address_intent_fetch(self, payload):
        api_endpoint = '/cataloglake/catalog/address/intent/fetch'
        return self.utillake.call_api(api_endpoint, payload)

    def fetch_mapper(self, payload):
        api_endpoint = '/cataloglake/catalog/metadata/fetchmapper'
        return self.utillake.call_api(api_endpoint, payload)

    def update_mapper(self, payload):
        api_endpoint = '/cataloglake/catalog/metadata/updatemapper'
        return self.utillake.call_api(api_endpoint, payload)