class dataset:

    def __init__(self,access_token):
        self.access_token = access_token
        
    def create_intent_dataset(self, path):
      type = 'text-intent'
      return self._create_dataset(path, type)

    def _create_dataset(self, path, type):
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        import requests
        import json

        LANG_DATASETS_URL = 'https://api.einstein.ai/v2/language/datasets'
        multipart_data = MultipartEncoder(
            fields={
                'path': path,
                'type': type
            }
        )
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': multipart_data.content_type}
        res = requests.post(LANG_DATASETS_URL + '/upload',
                            headers=headers, data=multipart_data)
        json_response = json.loads(res.text)
        return json_response

    def get_train_status(self, id):
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        import requests
        import json
        LANG_DATASETS_TRAINURL = 'https://api.einstein.ai/v2/language'

        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Cache-Control': 'no-cache'}
        res = requests.get(LANG_DATASETS_TRAINURL + '/train/'+id,
                           headers=headers)
        return res
        
    def train_dataset(self, id):
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        import requests
        import json
        LANG_DATASETS_TRAINURL = 'https://api.einstein.ai/v2/language'
        
        multipart_data = MultipartEncoder(
            fields={'name': 'Social Classification Model',
                    'datasetId' : id})

        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': multipart_data.content_type}
        res = requests.post(LANG_DATASETS_TRAINURL + '/train',
                              headers=headers, data=multipart_data)
        return res
