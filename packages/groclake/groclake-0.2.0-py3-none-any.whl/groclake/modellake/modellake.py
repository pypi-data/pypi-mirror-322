from ..utillake import Utillake


class Modellake:
    def __init__(self):
        self.utillake=Utillake()

    def translate(self, payload):
        api_endpoint = '/modellake/translate'
        return self.utillake.call_api(api_endpoint, payload)

    def chat_complete(self, payload):
        api_endpoint = '/modellake/chat/completion'
        return self.utillake.call_api(api_endpoint, payload)

    def text_to_speech(self, payload):
        api_endpoint = '/modellake/textToSpeech'
        return self.utillake.call_api(api_endpoint, payload)