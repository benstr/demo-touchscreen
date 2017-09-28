##from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
import json ## Import library to create and read JSON
import time ## Allows us to use 'sleep'
import sys

##hologram = HologramCloud(dict(), network='cellular', enable_inbound=False)

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

def received_sms():
  print "Received SMS"
  ##sms_obj = hologram.popReceivedSMS()
  ##print sms_obj.message
  return sms_obj.message

def start():
    print 'PYTHON STARTED'
    ##hologram.network.connect()

def sendData():
	print 'PYTHON SEND'
    ##hologram.sendMessage("Hello Nova")
    ##hologram.disableSMS()

def sendSMS(phoneNum):
	print 'PYTHON SMS'
    print phoneNum
    ##hologram.enableSMS()
    ##hologram.sendSMS(phoneNum, "Hello Nova")
    ##hologram.event.subscribe('sms.received', received_sms)

def sendSensor():
	print 'PYTHON SENSOR'
    ##hologram.disableSMS()
	exit()


# CODE

start()

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
