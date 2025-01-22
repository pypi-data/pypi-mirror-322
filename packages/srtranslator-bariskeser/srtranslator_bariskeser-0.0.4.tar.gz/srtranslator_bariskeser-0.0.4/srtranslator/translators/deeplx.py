import httpx
import json
from .base import Translator


class DeepLX(Translator):
    max_char = 1500

    def translate(self, text: str, source_language: str, destination_language: str):
        deeplx_api = "http://node-kyb.bariskeser.com:1188/v1/translate"
        data = {
        	"text": text,
        	"source_lang": source_language,
        	"target_lang": destination_language
        }
        post_data = json.dumps(data)
        result = httpx.post(url = deeplx_api, data = post_data).text
        return result.text
