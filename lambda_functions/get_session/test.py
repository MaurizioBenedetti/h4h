import os

os.environ['NLP_HOST']='https://dtfjzeii9h.execute-api.us-east-1.amazonaws.com/prod/nlp'
os.environ['BACKEND_HOST']='http://h4h-api.48yn9m8g4b.us-east-1.elasticbeanstalk.com/api/handlemessage/'

from lambda_function import lambda_handler

event ={
  "messages": [
    {
      "_id": "514981590aa1900b9b9b1",
      "text": "The harvest went really well",
      "role": "appUser",
      "authorId": "d7f6e61d116c311a637261bd96516f",
      "name": "Steve",
      "received": 1444348338.704,
      "metadata": {},
      "actions": [],
      "source": {
        "type": "messenger"
      }
    }
  ]
}
response = lambda_handler(event, None)
print('response: {}'.format(response))
assert(response != None)
