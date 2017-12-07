import pycom
import time
import utime
import socket
import select
import machine
import gc
from machine import Pin
from tcs3200 import TCS3200
from mqtt import MQTTClient


pycom.heartbeat(False)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(False)
s.bind(("10.0.0.89", 7000))

def sub_cb(topic, msg):
    print(msg)

time.sleep(1)
client = MQTTClient("lightLopy", "io.adafruit.com", user="soerena", password="af35ecd7c14246b9adc0492a3ecc661f", port=1883)
time.sleep(1)
client.set_callback(sub_cb)
time.sleep(1)
client.connect()
time.sleep(1)
print('connected to adafruit!')


tc = TCS3200()
#pycom.rgbled(0x007f00) # set green light to show all OK


def readAndPublishColour():
    client.connect()
    print("reading and publishing")
    rgb = tc.getRGB()
    client.publish(topic="soerena/feeds/rgbFreq", msg=str(rgb))
    client.disconnect()
    pycom.rgbled(0x007f00) # green

while True:
    ready = select.select([s], [], [], 1)
    if ready[0]:
        pycom.rgbled(0x007f00) # set green light to show all OK
        data = s.recv(1024)
        print(data)
        readAndPublishColour()
        time.sleep(1)
        pycom.rgbled(0)
