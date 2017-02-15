from __future__ import print_function # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json, hashlib, requests, traceback, os

# set constants from env variables
BACKEND_HOST = os.getenv('BACKEND_HOST')
NLP_HOST = os.getenv('NLP_HOST')
REPEAT_QUESTION = 'Sorry, I didn\'t understand that.  Could you please try again?'

class NoResponseMetrics(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def get_session_status(session_id):

    table = get_dynamo_table('Session')

    try:
        response = table.get_item(
           Key={'SessionID': session_id}
        )
        return 'Item' in response and 'CurrentStatus' in response['Item']

    except ClientError:
        raise ClientError(
            '[InternalServerError] could not get session status'
        )


def get_session(session_id):

    table = get_dynamo_table('Session')

    response = table.get_item(
       Key={
            'SessionID': session_id
        }
    )
    if 'Item' in response.keys():
        return response
    else:
        return None


def persist_session(incoming_message, next_status='open'):

    table = get_dynamo_table('Session')

    try:
        return table.update_item(
            Key={
                'SessionID': incoming_message['respondent']['session_id']
            },
            UpdateExpression="set SessionData = :d, CurrentStatus = :c",
            ExpressionAttributeValues={
                ':d': json.dumps(incoming_message),
                ':c': next_status
            },
            ReturnValues='ALL_NEW'
        )['Attributes']
    except KeyError:
        raise KeyError(
            '[BadRequest] authorId is required'
        )
    except ClientError:
        raise ClientError(
            '[InternalServerError] could not create/update session object'
        )


def get_dynamo_table(table):
    return boto3.resource(
        'dynamodb',
        region_name="us-east-1",
        endpoint_url="https://dynamodb.us-east-1.amazonaws.com"
    ).Table(table)


def normalize_json_schema(event):
    """
    Parses the raw event from the message gateway into a json
    object to be used by the rest of the orchestrator

    Attributes:
        event: the raw event message from the gateway

    Raises:
        KeyError: throws bad request error if the event is missing a required
            key
    """

    def get_message_key_or_400(key):

        if type(key) is str:
            try:
                return event['messages'][0][key]
            except (KeyError, IndexError):
                raise KeyError(
                    '[BadRequest] key {} is required'.format(key)
                )
        if type(key) is list:
            curr_object = event['messages'][0]
            for current_key in key:
                try:
                    curr_object = curr_object[current_key]
                except KeyError:
                    raise KeyError(
                        '[BadRequest] key {} not found'.format(current_key)
                    )
            return curr_object

    return {
        'timestamp': get_message_key_or_400('received'),
        'respondent':
        {
            'respondent_id': get_message_key_or_400('authorId'),
            'session_id': hashlib.sha256(
                get_message_key_or_400('authorId')
            ).hexdigest(),
            "device_type": get_message_key_or_400(['source', 'type'])
        },
        "raw_response": get_message_key_or_400('text')
    }


def close_session(session_id):
    table = get_dynamo_table('Session')

    try:
        response = table.delete_item(
            Key={'SessionID': session_id}
        )
        return response
    except ClientError:
        raise ClientError(
            '[InternalServerError] unable to delete session'
        )


def get_next_response(message):
    print(message)
    r = requests.post(BACKEND_HOST, json=message)
    print(r)
    return r.json()


def send_msg_nlp(message):

    r = requests.post(NLP_HOST, json=message)
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 500:
        raise NoResponseMetrics(
            'could not parse metrics from NLP'
        )


def merge_dicts(dict1, dict2):
    for key in dict2:
        if (
            key in dict1 and
            isinstance(dict1[key], dict) and
            isinstance(dict2[key], dict)
        ):
            merge_dicts(dict1[key], dict2[key])
        else:
            dict1[key] = dict2[key]


def lambda_handler(event, context):
    incoming_message = normalize_json_schema(event)

    # get a has of the respondent's id and check to see if there is an
    # existing session
    session_id = incoming_message['respondent']['session_id']
    session_exists = get_session_status(session_id)


    # if this is a new session, get the first question
    # and create a new session
    if not session_exists:
        print("Creating a brand new session!")

        # get next response to user from backend
        merge_dicts(incoming_message, get_next_response(incoming_message))
        persist_session(incoming_message)

        print(incoming_message)

        return incoming_message['question']['question_text']

    # if this is not a new session, route the question response
    # to the NLP for parsing then get next question from backend
    else:
        print('Found an existing session.')

        session = persist_session(incoming_message)
        print('session: {}'.format(session))

        try:
            if 'TERMINATE' in session['on_next']:
                close_session(session_id)
                return

        # no on_next in session
        except KeyError:
            pass

        # call nlp to add values
        try:
            r_nlp = send_msg_nlp(session)
        except NoResponseMetrics:
            return REPEAT_QUESTION
        print('response from nlp api: {}'.format(json.dumps(r_nlp)))

        #send msg to backend
        r_be = get_next_response(r_nlp)
        print('response from back end: {}'.format(json.dumps(r_be)))

        # update json
        merge_dicts(session, r_be)
        print('normalized responses to be put in sessiondb: {}'.format(incoming_message))

        #update session status
        persist_session(incoming_message)
        print('message to be sent to user: {}'.format(incoming_message['question']))
        return incoming_message['question']