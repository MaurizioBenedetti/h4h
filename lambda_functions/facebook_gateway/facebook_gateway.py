from pymessenger.bot import Bot
import requests
import time
import os

MESSENGER_VALIDATION_TOKEN = os.getenv('MESSENGER_VALIDATION_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ORCHESTRATOR_URL = os.getenv('ORCHESTRATOR_URL')


def handler(event, context):

    print(
        'received event: {}'.format(event)
    )

    bot = Bot(ACCESS_TOKEN)
    method = event['context']['http-method']
    queryparams = event['params']['querystring']
    if method == "GET":
        if queryparams['hub.verify_token'] == MESSENGER_VALIDATION_TOKEN:
            return int(queryparams['hub.challenge'])
        else:
            return "Incorrect verify token"

    print('method: POST')
    for e in event['body-json']['entry']:
        messaging = e['messaging']
        for x in messaging:
            if x.get('message'):
                recipient_id = x['sender']['id']
                if x['message'].get('text'):
                    message = x['message']['text']
                    payload_data = {}
                    payload_data['messages'] = []
                    content_data = {}
                    content_data['_id'] = e['id']
                    content_data['text'] = message
                    content_data['authorId'] = recipient_id
                    content_data['name'] = 'unknown'
                    content_data['received'] = time.time()
                    content_data['metadata'] = {}
                    content_data['actions'] = []
                    content_data['source'] = {}
                    content_data['source']['type'] = 'messenger'

                    payload_data['messages'].append(content_data)

                    print(
                        'sending message to orchestrator: {}'
                        .format(payload_data)
                    )

                    r = requests.post(ORCHESTRATOR_URL, json=payload_data)

                    print(
                        'got response from orchestrator: {} {}'
                        .format(r.status_code, r.json())
                    )

                    fb_response = bot.send_text_message(recipient_id, r.json())

                    print(
                        'got response from facebook: {}'
                        .format(fb_response)
                    )

                if x['message'].get('attachments'):
                    for att in x['message'].get('attachments'):
                        bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])

    return "Success"
