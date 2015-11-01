#!usr/bin/python

import os
from flask import Flask, request, redirect, send_from_directory
from models.Record import db, Record
import requests
from lxml import html

from twilio.rest import TwilioRestClient
import twilio.twiml

# from image import image

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

    # Create a dictionary for the phone number and image.
    data = {}

    # Try to grab data as JSON. Exception - get it normally.
    try:
        json = request.get_json()
        data = [json["number"], json["image"]]
	print "JSON"
    except:
        data = [request.values.get("number"), request.values.get("image")]
	print "Other"

    fh = open("img.png", "wb")
    fh.write(data[1].decode('base64'))
    fh.close()
 
    # Create variable for the fixed number.
    fixedNumber = ""
    
    # Loop over characters, for every character that's numeric - append to the fixedNumber.
    for elem in data[0]:
        if elem.isnumeric():
            fixedNumber = fixedNumber + str(elem)

    # If the length is only 10, add +1. If it's only 11, add + (first number should be a 1).
    if len(fixedNumber) == 10:
        fixedNumber = "+1" + fixedNumber
    elif len(fixedNumber) == 11:
        fixedNumber = "+" + fixedNumber

    # Store fixed number back to dictionary.
    data[0] = fixedNumber

    # Create new record, query all items in the db where the phone number is equal to the 
    # input phone number.
    r = Record(data[0], data[1])
    phones = Record.query.filter_by(phone=fixedNumber).all()

    # As long as that record does not exist, add it and commit.
    # Pass this if already there, just send them a new text!
    if phones == None:
        db.session.add(r)
        db.session.commit()
    else:
        pass

    # image(fixedNumber, request.values.get("image"))
    # Generate Twilio client. Send text.
    client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(to=fixedNumber, from_=twilio_number, body="Hey! Want to HEAR what your PICTURE looks like? Send \"yes\" to this SMS!")

    return "None"

#@app.route("/audio/test.mp3", methods=['GET','POST'])
#def audioFiles():
#    app.send_static_file('audio/test.mp3')

def get_tags():
    payload = {
	"grant_type": "client_credentials",
	"client_id": "JBVqlsHeEhudFSEQirJzt04piCJ5fBsVux7kNoxA",
	"client_secret": "9QdRHGl5VbYSj4dgnJEegrA8ppAuH3KNmit_2A7O"
    }
    token = requests.post("https://api.clarifai.com/v1/token/", params=payload).json()
    access_token = token['access_token']
    payload = {
    	"url": "http://jayravaliya.com:5000/img.png"
    }
    header = {
	"Authorization" : "Bearer " + access_token
    }
    final = requests.post("https://api.clarifai.com/v1/tag/", params=payload, headers=header)
    print final.text

def get_song(tags):
    search = ""
    for elem in tags:
	search = search + elem + "+"

    payload = {"q" : search}

    page = requests.get("http://search.azlyrics.com/search.php", params=payload)
    tree = html.document_fromstring(page.text)

    for val in tree.xpath("//a[contains(@href, 'lyrics')]"):
        if len(val.text_content()) > 1:
		print val.text_content()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
