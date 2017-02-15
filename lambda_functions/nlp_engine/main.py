import requests
import re
import json
import os
import httplib
import urllib

YANDEX_KEY = os.getenv('YANDEX_KEY')
WATSON_KEY = os.getenv('WATSON_KEY')


Small = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}
Magnitude = {
    'thousand':     1000,
    'million':      1000000,
    'billion':      1000000000,
    'trillion':     1000000000000,
    'quadrillion':  1000000000000000,
    'quintillion':  1000000000000000000,
    'sextillion':   1000000000000000000000,
    'septillion':   1000000000000000000000000,
    'octillion':    1000000000000000000000000000,
    'nonillion':    1000000000000000000000000000000,
    'decillion':    1000000000000000000000000000000000,
}

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def text2num(s):
    a = re.split(r"[\s-]+", s)
    n = 0
    g = 0
    for w in a:
        x = Small.get(w, None)
        if x is not None:
            g += x
        elif w == "hundred" and g != 0:
            g *= 100
        else:
            x = Magnitude.get(w, None)
            if x is not None:
                n += g * x
                g = 0
            else:
                raise NumberException("Unknown number: "+w)
    return n + g

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


class ParserException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def translate(s):
    parameters = {
        'key': YANDEX_KEY,
        'lang':'en',
        'text': s
    }
    response = requests.post(
        'https://translate.yandex.net/api/v1.5/tr.json/translate',
        data=parameters)
    if response.status_code !=200:
        msg = "bad request. code: {} reason: {}".format(
            response.status_code, response.reason)
        raise ParserException("text-processing.com error. msg: {}".format(
            msg))
    return response.json()['text'][0]


def send_watson_request(raw_string, try_num=1, max_retries=3):
    if try_num >= max_retries:
        raise ParserException("cannot translate to english. input: {}".format(
            raw_string))

    parameters = {
        'apikey': WATSON_KEY,
        'outputMode': 'json',
        'extract': 'keywords,doc-sentiment,taxonomy,dates,entity',
        'sentiment': '0',
        'maxRetrieve': '5',
        'text': raw_string
    }

    response = requests.post(
        'https://gateway-a.watsonplatform.net/calls/text/TextGetCombinedData',
        data=parameters
    )
    if response.status_code != 200:
        msg = "bad request. code: {} reason: {}".format(
            response.status_code, response.reason)
        raise ParserException("IBM Watson Alchemy Error. msg: {}".format(
            msg))

    formatted_response = response.json()

    print(formatted_response)

    if formatted_response['language'] != 'english':
        translated_text = translate(raw_string)
        send_watson_request(translated_text,try_num+1)
    else:
        return response.json()


def get_number(response):
    num_list = re.findall('\d+', response)
    if num_list:
        return ",".join(num_list)

    def convert_string_to_num(response):
        for token in response.split(' '):
            try:
              num_list = text2num(token)
              return num_list
            except NumberException:
              print('number exception when converting text to num')
    num_list = convert_string_to_num(response)
    if num_list:
        return num_list
    translated_response = translate(response)
    num_list = convert_string_to_num(translated_response)
    if not num_list:
        raise ParserException('error parsing number metric. input: {}'.format(
            response))
    return {'metric_value': num_list, 'confidence': None}


def get_sentiment(response):
    alchemy_result = send_watson_request(response) 
    try:
        result_sentiment = alchemy_result["docSentiment"]["score"]
    except KeyError:
        result_sentiment = 0
    return {'metric_value': result_sentiment, 'confidence': None}    


def get_entities(response):
    alchemy_result = send_watson_request(response) 
    if len(alchemy_result["keywords"])==0:
        raise ParserException("cannot parse entities. input: {}".format(
            response))
    result_value = ",".join([keyword["text"] for keyword in alchemy_result["keywords"]])
    result_confidence = ",".join([keyword["relevance"] for keyword in alchemy_result["keywords"]])
    return {'metric_value': result_value, 'confidence': result_confidence}


def get_dates(response):
    alchemy_result = send_watson_request(response) 
    result_value = ",".join([date["date"] for date in alchemy_result["dates"]])
    return {'metric_value': result_value, 'confidence': None}


def get_geo(response):
    alchemy_result = send_watson_request(response)
    try:
        location = alchemy_result['entities'][0]['text']
        location_type = alchemy_result['entities'][0]['type']
        return {'location': location, 'location_type': location_type}
    except IndexError:
        raise ParserException("cannot parse geo information. input: {}".format(
            response))


def get_binary(response):
    # FROM THESAURUS.COM
    yes_list = set(['yes','sure', 'affirmative','amen','fine','good','okay','true','yea','all right','aye','beyond a doubt','by all means','certainly','definitely','even so','exactly','gladly','good enough','granted','indubitably','just so','most assuredly','naturally','of course','positively','precisely','sure thing','surely','undoubtedly','unquestionably','very well','willingly','without fail','yep'])
    no_list = set(['no','negative','absolutely not','nix','by no means','never','no way','not at all','not by any means'])
    maybe_list = set(['maybe','perchance','perhaps','possibly','as it may be','can be','conceivably','could be','credible','feasible','imaginably','it could be','might be','obtainable','weather permitting'])

    cleaned_response = ' '.join([token.lower() for token in response.split()])
    
    def logic(cleaned_response):
        if cleaned_response in yes_list:
            return "YES"
        elif cleaned_response in no_list:
            return "NO"
        elif cleaned_response in maybe_list:
            return "MAYBE"
        else:
            raise ParserException('Cannot parse yes/no/maybe')
    try:
        return_val = logic(cleaned_response)
        return {'metric_value': return_val, 'confidence': None}
    except ParserException:
        translated_response = translate(cleaned_response)
        return_val = logic(translated_response)
        return {'metric_value': return_val, 'confidence': None}


def lambda_handler(event, context):
    print(event)
    raw_response = event["raw_response"]
  
    metrics_calls = {
    'yesNoMaybe': get_binary,
    'numeric': get_number,
    'sentiment': get_sentiment,
    'entity': get_entities,
    # 4: get_dates, # unused
    # TODO test against image format provided by orchestrator
    'image': getImageTags,
    'geo': get_geo,
  }
  
    metric_response = []
    final_result = event.copy()

    for metric in event["question"]["metrics"]:
        metric_id = metric["metric_id"]
        metric_type = metric["metric_type"]
        print('fetching metric type: {}'.format(metric_type))
        result = metrics_calls[metric_type](raw_response)
    print('result: {}'.format(result))

    # populate different fields for geo
    if metric_type == 'geo':
        final_result['respondent']['location'] = result['location']
        final_result['respondent']['location_type'] = result['location_type']

    else:
        metric_response.append({'metric_id': metric_id, 
            'metric_type': metric_type, 
            'metric_value': result.get('metric_value'), 
            'confidence': result.get('confidence')}) 

    final_result["question"]["metrics"] = metric_response
    return final_result

