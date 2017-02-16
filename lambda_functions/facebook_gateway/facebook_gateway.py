from pymessenger.bot import Bot
import requests
import json
import time
import os

MESSENGER_VALIDATION_TOKEN = os.getenv('MESSENGER_VALIDATION_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ORCHESTRATOR_URL = os.getenv('ORCHESTRATOR_URL')

def handler(event, context):

    bot = Bot(ACCESS_TOKEN)
    method = event['context']['http-method']
    queryparams = event['params']['querystring']
    if method == "GET":
        if queryparams['hub.verify_token'] == MESSENGER_VALIDATION_TOKEN:
            return int(queryparams['hub.challenge'])
        else:
            return "Incorrect verify token"

    for e in event['body-json']['entry']:
        messaging = e['messaging']
        for x in messaging:
            if x.get('message'):
                recipient_id = x['message']['sender']['id']
                if x['message'].get('text'):
                    message = x['message']['text']

                    session_id = '1234567890'
                    payload_data = {}
                    payload_data['messages'] = []
                    content_data = {}
                    content_data['_id'] = session_id
                    content_data['text'] = message
                    content_data['authorId'] = recipient_id
                    content_data['name'] = 'unknown'
                    content_data['received'] = time.time()
                    content_data['metadata'] = {}
                    content_data['actions'] = []
                    content_data['source'] = {}
                    content_data['source']['type'] = 'messenger'

                    payload_data['messages'].append(content_data)

                    r = requests.post(ORCHESTRATOR_URL, json=payload_data)

                    bot.send_text_message(recipient_id, r.text)
                    bot.send_text_message(recipient_id, r.status_code)

                    try:
                        response_data = r.json()
                        response_content = response_data['messages'][0]['text']
                        print(response_content)
                        bot.send_text_message(recipient_id, response_content)
                    except Exception:
                        bot.send_text_message(recipient_id, r.text)
                        pass

                if x['message'].get('attachments'):
                    for att in x['message'].get('attachments'):
                        bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])

    return "Success"
