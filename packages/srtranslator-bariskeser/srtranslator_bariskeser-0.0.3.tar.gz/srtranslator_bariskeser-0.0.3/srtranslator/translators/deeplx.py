from .base import Translator as BaseTranslator
import httpx, json

class DeepLX(BaseTranslator):
    max_char = 1500

    def translate(self, text, source_language, destination_language):
        deeplx_api = "http://node-kyb.bariskeser.com:1188/v1/translate"
        data = {
        	"text": text,
        	"source_lang": source_language,
        	"target_lang": destination_language
        }
        post_data = json.dumps(data)
        result = httpx.post(url = deeplx_api, data = post_data).text
        return result.result
