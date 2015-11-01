import os
from flask import Flask, request, redirect

from twilio.rest import TwilioRestClient
import twilio.twiml

app = Flask(__name__)

# Credentials
twilio_account_sid = 'AC9cda9f49921253df4a0781b4318f4d23'
#os.environ['TWILIO_ID'] or

twilio_auth_token = '82b0d956d668f10c8b2b6ce7195052ef'
#os.environ['TWILIO_TOKEN'] or

twilio_number = "+17323557153"
#os.environ['TWILIO_NUMBER'] or


@app.route("/", methods=['POST'])
def add():
    """Takes in contact and image data."""
    pass
    return "None"

@app.route("/sing", methods=['GET','POST'])
def sing():
    """Take in the response to the text sent and decide whether to call."""
    if request.values.get('From') and request.values.get('Body'):
        # assumes if there is a From parameter that this is from Twilio
        sender = request.values.get('From')
        answer = request.values.get('Body').lower()
        # if response is some kind of yes
        if answer.lower() in ['yeah', 'yes', 'yep', 'yup', 'yea', 'ya']:
            # send the song call
            client = TwilioRestClient(account_sid, auth_token)

            call = client.create(
                url="https://2c7cfed2.ngrok.com/twiml/Temp.xml",
                to=sender,
                #from=twilio_number,
                method="GET",
                status_callback="https://2c7cfed2.ngrok.com/monitor" + str(sender),
                status_events=['completed']
            )

@app.route("/monitor/<phone>")
def monitor(phone):
    """Monitors status of phone call to delete xml at the end"""





if __name__ == "__main__":
    app.run(debug=True)
    print __name__
