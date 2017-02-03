from twilio.rest import TwilioRestClient
# put your own credentials here
#ACCOUNT_SID = "SKb0bd8533115b1bc1f11ec488f6b2d395"
#AUTH_TOKEN = "Y8K16bvxjp0dFTuWL73ccncsTsRx9Czj"
ACCOUNT_SID = "AC373af54372b22c5a2a101e6419f833e1"
AUTH_TOKEN = "f9055d78c46088aaa337f9651d789e07"


def handler(event, context):
    # TODO implement
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    response = client.messages.create(
        to="+14159374697",
        from_="+15005550006",
        body="This is the ship that made the Kessel Run in fourteen parsecs?",
        media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg",
    )

    return True
