##from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
import json ## Import library to create and read JSON
from Hologram.HologramCloud import HologramCloud
import logging
import os
import select
import sys
import time ## Allows us to use 'sleep'
import traceback

#logging.basicConfig(level=logging.DEBUG)


class HologramDemo(object):

    def __init__(self):
        credsfile = os.path.dirname(os.path.realpath(__file__)) +\
            '/credentials.json'
        with open(credsfile, 'r') as f:
            self.credentials = json.load(f)
            self.init_hologram()

    def init_hologram(self):
        self.hologram = HologramCloud(self.credentials, network='cellular',
                authentication_type='csrpsk')
        self.hologram.enableSMS()


    # FUNCTIONS
    def convert_location_into_json(location_obj):
        location_list = ['date', 'time', 'latitude', 'longitude', 'altitude', 'uncertainty']
        response_list = [location_obj.date, location_obj.time, location_obj.latitude,
                         location_obj.longitude, location_obj.altitude, location_obj.uncertainty]
        location_data = dict(zip(location_list, response_list))
        return json.dumps(location_data)

    def run_modem_location(self):
        location_obj = hologram.network.location
        if location_obj is None:
            return 'NA'
        else:
            return convert_location_into_json(location_obj)



    def checkForSMS(self):
        sms_obj = self.hologram.popReceivedSMS()

        if sms_obj is not None:
            print u"Got SMS: ", sms_obj.message


    def start(self):
        print 'PYTHON STARTED'

    def sendData(self):
        print('Sending data to cloud')
        self.hologram.network.connect()
        self.hologram.sendMessage('Hello Nova')
        self.hologram.network.disconnect()
        print('Done')

    def sendSMS(self, destination_number):
        print('Sending SMS to %s'%destination_number)
        self.hologram.network.connect()
        self.hologram.sendSMS(destination_number, "Hello Nova")
        self.hologram.network.disconnect()
        print('Done')

    def sendSensor(self):
            print 'PYTHON SENSOR'
        ##hologram.disableSMS()
            exit()

    def demoLoop(self):
        print("Starting Demo")
        try :
            while True:
                rd, wr, er = select.select([sys.stdin], [], [], 5)
                if rd:
                    line = sys.stdin.readline()
                    if line == "sendData\n":
                        self.sendData()
                    elif line == "sendSMS\n":
                        secondLine = sys.stdin.readline()
                        print secondLine
                        self.sendSMS(secondLine.rstrip())
                    elif line == "sendSensor\n":
                        self.sendSensor()
                    else:
                        print 'dunno'
                self.checkForSMS()
        except Exception:
            print(traceback.format_exc())
            self.hologram.network.disconnect()


h = HologramDemo()
h.demoLoop()

