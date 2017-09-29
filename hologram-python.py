##from Hologram.HologramCloud import HologramCloud ## Import Hologram cloud library
import json ## Import library to create and read JSON
import time ## Allows us to use 'sleep'
from Hologram.HologramCloud import HologramCloud
import sys
import logging

#logging.basicConfig(level=logging.DEBUG)


class HologramDemo(object):

    def __init__(self):
        with open('/home/pi/credentials.json', 'r') as f:
            self.credentials = json.load(f)
            self.init_hologram()

    def init_hologram(self):
        self.hologram = HologramCloud(self.credentials, network='cellular',
                authentication_type='csrpsk')

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

    def run_modem_location(self):
        location_obj = hologram.network.location
        if location_obj is None:
            return 'NA'
        else:
            return convert_location_into_json(location_obj)

    def popReceivedSMS(self):
        print 'POP RECEIVED SMS'
        sms_obj = hologram.popReceivedSMS()

        if sms_obj is not None:
            print 'sender:', sms_obj.sender
            print sms_obj.timestamp.strftime('%c')
            print u'message:', sms_obj.message

    def receiveSMS(self):
        print 'RECEIVE SMS'
        hologram.network.connect()

        hologram.event.subscribe('sms.received', popReceivedSMS)

        hologram.enableSMS()

        handle_polling(20, popReceivedSMS, 1)

        hologram.disableSMS()

        hologram.network.disconnect()

    def start(self):
        print 'PYTHON STARTED'

    def sendData(self):
        print('Sending data to cloud')
        self.hologram.network.connect()
        self.hologram.sendMessage('Hello Nova')
        self.hologram.network.disconnect()
        print('Data Sent')

    def sendSMS(self, destination_number):
        print('Sending SMS to %s'%destination_number)
        self.hologram.network.connect()
        self.hologram.sendSMS(destination_number, "Hello Nova")
        self.hologram.network.disconnect()
        print('SMS Sent')

    def sendSensor(self):
            print 'PYTHON SENSOR'
        ##hologram.disableSMS()
            exit()

    def demoLoop(self):
        print("Starting Demo")
        while True:
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


h = HologramDemo()
h.demoLoop()

