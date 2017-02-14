import httplib
import urllib
import base64
import json
import os

PROJECTOXFORD_KEY = os.getenv('PROJECTOXFORD_KEY')

def getImageTags(photo_file):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': PROJECTOXFORD_KEY,
    }

    params = urllib.urlencode({
    })

    with open(photo_file, 'rb') as image:
        image_data = image.read()

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/tag?%s" % params, image_data, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))
        conn.close()
        return data['tags']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
