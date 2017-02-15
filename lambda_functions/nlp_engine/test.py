import os

os.environ['WATSON_KEY']='ce0618f33d6b5dcb305c884dd1ab6ce720dc0562'
os.environ['PROJECTOXFORD_KEY']='fe1ddf67faa347b1847318f516e6065f'
os.environ['YANDEX_KEY']='trnsl.1.1.20170108T012202Z.fa1a8d03eb8d33be.60cd4068fa2f37d75d11fad1906531974ce3ccdf'


from main import lambda_handler

event ={
 "response_id": "test",
 "timestamp":"test",
 "session_id": "test",
 "raw_response": "I farm apples and chickens",
 "question": {
   "question_id": "1",
   "question_text": "What do you farm?",
   "metrics": [
     {"metric_id": 1, "metric_type": "sentiment"},
     {"metric_id": 4, "metric_type": "entity"}
   ]
 }
}
response = lambda_handler(event, None)
print('response: {}'.format(response))
assert(response != None)
