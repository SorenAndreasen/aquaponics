
from network import Bluetooth
from network import WLAN
from mqtt import MQTTClient
from colorSensor import ColorSensor
from platform import PlatformController
import pycom
import time
import utime
import machine


#print('rtc.now:'+str(rtc.now())+" utime.time:"+str(int(utime.time())))
pycom.heartbeat(False)

def sub_cb(topic, msg):
    print(msg)

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

for net in nets:
     if net.ssid == 'NETGEAR64':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'oddchair195'), timeout=5000)
        while not wlan.isconnected():
            pycom.rgbled(0x7f0000)
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

# initialize time
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
#print('\nRTC Set from NTP to UTC:', rtc.now()) # UTC time
utime.timezone(7200) # adjust to danish time
print('adjusted:', utime.localtime(), '\n')





pycom.rgbled(0x007f00)
client = MQTTClient("device_id", "io.adafruit.com", user="soerena", password="af35ecd7c14246b9adc0492a3ecc661f", port=1883)
client.set_callback(sub_cb)
client.connect()



time.sleep(1)
pycom.rgbled(0x000000) # turn off led

# colour analysis
#cs = ColorSensor()
#cs.checkBalance()
#cs.checkColour()
#print(cs.printColour())

# pump control

# platform control
pCont = PlatformController()


# put in while true loop:
if utime.localtime()[3] == 8:
    print("measure morning")
elif utime.localtime()[3] == 12:
    print("measure midday")
elif utime.localtime()[3] == 20:
    print("measure evening")

#time.sleep(2)
#print("Sending")
#client.publish(topic="soerena/feeds/aquaponics", msg="10")
#time.sleep(2)
#print("Sending")
#client.publish(topic="soerena/feeds/aquaponics", msg="30")
#time.sleep(2)
