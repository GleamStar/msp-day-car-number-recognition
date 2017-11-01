import httplib
import urllib
import json

# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'd5d9578f7b9b4b8bbc256e052034d886'

# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.urlencode({
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
})


class AzureCVService:
    """Azure CV Request Helper"""

    def __init__(self):
        self.conn = None

    def read_local_image(self, path):
        f = open(path, "rb")
        body = f.read()
        f.close()
        return body

    def make_cv_request(self, body):
        try:
            # Execute the REST API call and get the response.
            self.conn = httplib.HTTPSConnection(uri_base)
            self.conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
            return self.conn.getresponse().read()
        except Exception as e:
            print('Error:')
            print(e)
        finally:
            self.conn.close()

    def print_response(self, response):
        parsed_data = json.loads(response)
        text = ''
        for parsed_item in parsed_data['regions']:
            for parsed_line in parsed_item['lines']:
                for word in parsed_line['words']:
                    text += ' ' + word['text'].encode('utf-8').strip()
                text += '\n'
        print(text)
