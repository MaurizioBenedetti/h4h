from pymessenger.bot import Bot
import requests
import json
import time
import os

MESSENGER_VALIDATION_TOKEN = os.getenv('MESSENGER_VALIDATION_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

def handler(event, context):
    #MESSENGER_VALIDATION_TOKEN = event["stage-variables"]["MESSENGER_VALIDATION_TOKEN"]
    #ACCESS_TOKEN = event["stage-variables"]["PAGE_ACCESS_TOKEN"]
    print(event)
    #print(context)
    #sqs = boto3.resource('sqs')

    bot = Bot(ACCESS_TOKEN)
    method = event['context']['http-method']
    queryparams = event['params']['querystring']
    if method == "GET":
        if queryparams['hub.verify_token'] == MESSENGER_VALIDATION_TOKEN:
            return queryparams['hub.challenge']
        else:
            return "Incorrect verify token"
    #print(event)
    #queue = sqs.get_queue_by_name(QueueName='inbound')
    #response = queue.send_message(MessageBody='Test Message to SQS')
    
    #bot.send_text_message(recipient_id, message)
    for event in event['body-json']['entry']:
        messaging = event['messaging']
        for x in messaging:
            if x.get('message'):
                recipient_id = x['sender']['id']
                print(recipient_id)
                if x['message'].get('text'):
                    message = x['message']['text']
                    
                    # Get the queue. This returns an SQS.Queue instance
                    #queue = sqs.get_queue_by_name(QueueName='inbound')
                    
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

                    print(message)
                    #payload_data = self.payload(recipient_id, message)
                    #bot.send_text_message(recipient_id, message)
                    #bot.send_text_message(recipient_id, message)
                    json_data = json.dumps(payload_data)
                    #bot.send_text_message(recipient_id, json_data)
                    r = requests.post('https://p2prxjz2t3.execute-api.us-east-1.amazonaws.com/Production/get_session', data=json_data)
                    # You can now access identifiers and attributes
                    
                    bot.send_text_message(recipient_id, r.text)
                    bot.send_text_message(recipient_id, r.status)
                    try:
                        response_data = r.json()
                        response_content = response_data['messages'][0]['text']
                        print(response_content)
                        bot.send_text_message(recipient_id, response_content)
                    except:
                        print(r.text)
                        bot.send_text_message(recipient_id, r.text)
                        pass

                    #print(queue.url)
                    #print(queue.attributes.get('DelaySeconds'))
                if x['message'].get('attachments'):
                    for att in x['message'].get('attachments'):
                        bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
    return "Success"
