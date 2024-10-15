from twilio.rest import Client
from time import time
from numpy import round

start  = time()

def generate(phone):
    global start
    # set Twilio account SID, auth token, and phone number
    account_sid = 'AC70d82eba573132115cf2c557ac85bdb1'
    auth_token = 'd028c51cbc25a7b098cf788cd5dd4177'
    twilio_number = '+19893732989'

    # create Twilio client
    client = Client(account_sid, auth_token)

    # send SMS message containing OTP
    end = time()

    if round(end-start, 0) > 300000:
        message = client.messages.create(
            body=f'Fire detected!!!',
            from_=twilio_number,
            to="+91"+phone
        )
        start = time()

    
