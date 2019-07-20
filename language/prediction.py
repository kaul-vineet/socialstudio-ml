class prediction:

    def __init__(self,access_token):
        self.access_token = access_token

    def predict_social_tag(self, document, model_id):
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        import requests
        import json
        LANG_INTENT_URL = 'https://api.einstein.ai/v2/language/intent'
        
        multipart_data = MultipartEncoder(
            fields={'document': document,
                    'modelId' : model_id})

        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': multipart_data.content_type}
        res = requests.post(LANG_INTENT_URL,
                            headers=headers, data=multipart_data)
        if res.ok:
            json_response = json.loads(res.text)
            return json_response
        else:
            return res
