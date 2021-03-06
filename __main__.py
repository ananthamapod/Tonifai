#!usr/bin/python

import os
from flask import Flask, request, redirect, send_from_directory
from models.Record import db, Record

from twilio.rest import TwilioRestClient
import twilio.twiml

from image import image

app = Flask(__name__, static_url_path='')

# Credentials
twilio_account_sid = 'AC613975d801ea2516d3cbdaa570550163'
#os.environ['TWILIO_ID'] or

twilio_auth_token = '76599dfd9b6cb8e3830385b2506d7439'
#os.environ['TWILIO_TOKEN'] or

twilio_number = "+19733214779"
#os.environ['TWILIO_NUMBER'] or


@app.route("/", methods=['GET','POST'])
def add():
    """Takes in contact and image data."""
    pass
    return "This works"

@app.route("/sing", methods=['GET','POST'])
def sing():
    """Take in the response to the text sent and decide whether to call."""
    print request.values
    if request.values.get('From') and request.values.get('Body'):
        # assumes if there is a From parameter that this is from Twilio
        sender = request.values.get('From')
        answer = request.values.get('Body').lower()
        print answer
        # if response is some kind of yes
        if answer in ['yeah', 'yes', 'yep', 'yup', 'yea', 'ya']:
            # send the song call
            print "This is true"
            client = TwilioRestClient(twilio_account_sid, twilio_auth_token)

            call = client.calls.create(
                url="https://2c7cfed2.ngrok.com/twiml/" + "Temp" + ".xml",
                to=sender,
                from_=twilio_number,
                method="GET",
                status_callback="https://2c7cfed2.ngrok.com/monitor",
                status_callback_method="POST",
                status_events=['completed']
            )
    else:
        print "test"
    return "Yessir"

@app.route("/monitor", methods=['POST'])
def monitor():
    """Monitors status of phone call to delete xml at the end"""
    called = request.values.get("Called")
    caller = request.values.get("Caller")
    callstatus = request.values.get("CallStatus")

    if(callstatus == "completed"):
        print "Awesome"

    return "Great"

@app.route("/initiate", methods=['GET', 'POST'])
def initiate():
    fixedNumber = ""
    print request.form['number']
    print "A"
    print request.values.get('number')
    for elem in request.values.get('number'):
        if elem.isnumeric():
            fixedNumber = fixedNumber + str(elem)
    print "B"
    if len(fixedNumber) == 10:
        fixedNumber = "+1" + fixedNumber
    elif len(fixedNumber) == 11:
        fixedNumber = "+" + fixedNumber

    print "C"
    r = Record(fixedNumber, request.values.get("image"))
    phones = Record.query.filter_by(phone=fixedNumber).all()

    print "D"
    if phones == None:
        db.session.add(r)
        db.session.commit()
    else:
        pass

    print "E"
    image(fixedNumber, request.values.get("image"))
    client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(to=fixedNumber, from_=twilio_number, body="Hey! Want to HEAR what your PICTURE looks like? Send \"yes\" to this SMS!")

    return "None"

#@app.route("/audio/test.mp3", methods=['GET','POST'])
#def audioFiles():
#    app.send_static_file('audio/test.mp3')



if __name__ == "__main__":
    app.run(debug=True)
    print __name__
