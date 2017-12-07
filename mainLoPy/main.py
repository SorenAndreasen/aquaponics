import pycom
import time
import utime
import socket
import machine
import gc
from machine import ADC
from machine import Pin
from ds18x20 import DS18X20
from motors import MOTORS
from mqtt import MQTTClient
waterTemp = 0
plantTemp = 0
PH3_10 = 0
lastHour = 999
pycom.heartbeat(False)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#pycom.rgbled(0x007f00) # green

waterPump_p = Pin('P20', mode=Pin.OUT)
waterPump_p.value(1) # init water pump off


print('p20')
# TEMP:
temp_p = DS18X20(Pin('P11', mode=Pin.OUT))
time.sleep(1)

def sub_cb(topic, msg):
    print(msg)

# initialize time
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
#print('\nRTC Set from NTP to UTC:', rtc.now()) # UTC time
utime.timezone(3600) # adjust to danish time
print('adjusted:', utime.localtime())

#pycom.rgbled(0x007f00)

time.sleep(1)
client = MQTTClient("lopyMain", "io.adafruit.com", user="soerena", password="af35ecd7c14246b9adc0492a3ecc661f", port=1883)
time.sleep(1)
client.set_callback(sub_cb)
print('connected to adafruit!')
#pycom.rgbled(0x007f00) # set green light to show all OK
# colour analysis
m = MOTORS()
#tc = TCS3200()


def pcTakePicture():
    s.sendto(b'1', ("10.0.0.6", 7007))

def readAndPublishTemp():
    client.connect()
    waterTemp = temp_p.read_temps()[0] / 1000
    print("reading and publishing")
    client.publish(topic="soerena/feeds/waterTemp", msg=str(waterTemp))
    client.disconnect()
    #pycom.rgbled(0x007f00) # green
def sendToColorLoPy():
    s2.sendto(b'1', ("10.0.0.89", 7000))



def readAndPublishPH():
    client.connect()
    print("reading and publishing")
    m.prepareSample()
    time.sleep(180) # wait for sample to settle
    sendToColorLoPy() # 2nd lopy to read+publish colour
    pcTakePicture() # Macbook takes picture of reagent
    time.sleep(10) # allow time for image capturing
    m.rinse() # rinse glass
    client.disconnect()

def waterPlants():
    waterPump_p.value(0)
    time.sleep(100)
    waterPump_p.value(1)

while True:
    pycom.rgbled(0x007f00) # set green light to show all OK
    if utime.localtime()[3] != lastHour:
        pycom.rgbled(0) # turn off led
        lastHour = utime.localtime()[3]
        readAndPublishTemp()
        if utime.localtime()[3] == 9:
            readAndPublishPH()
            waterPlants()
        elif utime.localtime()[3] == 20:
            readAndPublishPH()
            waterPlants()
        time.sleep(1)
        gc.collect()
