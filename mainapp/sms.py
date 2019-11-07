# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC9ac592dbc2675279beaddd13f3bc5f06'
auth_token = '1f72c7ff88e5806a3d3d3a044c9b45f2'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     to='+15017122661',
                     from_='+254729446214'
                 )

print(message.sid)
