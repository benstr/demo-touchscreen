##from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
import json ## Import library to create and read JSON
import time ## Allows us to use 'sleep'
from Hologram.HologramCloud import HologramCloud

device_key = raw_input("What is your device key? ")
destination_number = raw_input("What is your destination number? ")
credentials = {'devicekey': device_key}

hologram = HologramCloud(credentials, network='cellular')

def handle_polling(timeout, fx, delay_interval=20):
    try:
        if timeout != -1:
            print 'waiting for ' + str(timeout) + ' seconds...'
            end = time.time() + timeout
            while time.time() < end:
                fx()
                time.sleep(delay_interval)
        else:
            while True:
                fx()
                time.sleep(delay_interval)
    except KeyboardInterrupt as e:
        sys.exit(e)

# FUNCTIONS
def convert_location_into_json(location_obj):
    location_list = ['date', 'time', 'latitude', 'longitude', 'altitude', 'uncertainty']
    response_list = [location_obj.date, location_obj.time, location_obj.latitude,
                     location_obj.longitude, location_obj.altitude, location_obj.uncertainty]
    location_data = dict(zip(location_list, response_list))
    return json.dumps(location_data)

def run_modem_location():
    location_obj = hologram.network.location
    if location_obj is None:
        return 'NA'
    else:
        return convert_location_into_json(location_obj)

def popReceivedSMS():
    print 'POP RECEIVED SMS'
    sms_obj = hologram.popReceivedSMS()

    if sms_obj is not None:
        print 'sender:', sms_obj.sender
        print sms_obj.timestamp.strftime('%c')
        print u'message:', sms_obj.message

def receiveSMS():
    print 'RECEIVE SMS'
    hologram.network.connect()

    hologram.event.subscribe('sms.received', popReceivedSMS)

    hologram.enableSMS()

    handle_polling(20, popReceivedSMS, 1)

    hologram.disableSMS()

    hologram.network.disconnect()

def start():
    print 'PYTHON STARTED'

def sendData():
	print 'PYTHON SEND'
    ##hologram.sendMessage("Hello Nova")
    ##hologram.disableSMS()

def sendSMS(destination_number):
    hologram.network.connect()
    hologram.sendSMS(destination_number, "Hello Nova")
    hologram.network.disconnect()

def sendSensor():
	print 'PYTHON SENSOR'
    ##hologram.disableSMS()
	exit()

# CODE

start()

sendSMS(destination_number)
receiveSMS()

while True:
    line = sys.stdin.readline()
    if line == "sendData\n":
    	sendData()
    elif line == "sendSMS\n":
        secondLine = sys.stdin.readline()
        print secondLine
    	sendSMS(secondLine)
    elif line == "sendSensor\n":
    	sendSensor()
    else:
    	print 'dunno'
