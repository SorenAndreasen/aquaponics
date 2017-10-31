
from network import Bluetooth
from network import WLAN
from mqtt import MQTTClient
#from colorSensor import ColorSensor
#from platform import PlatformController
import pycom
import time
import utime
import machine
from machine import Pin
from machine import PWM
from ds18x20 import DS18X20
print('started!')
pycom.heartbeat(False)
pycom.rgbled(0x7f7f00) # yellow

pwm = PWM(0, frequency=50)
pwm_c = pwm.channel(0, pin='P22', duty_cycle=0.127)
pwm_c.duty_cycle(0.097)
# red temp
#d=DS18X20(Pin('P21', mode=Pin.OUT)) # G8
#result=d.read_temps()
#print(result)
#time.sleep(1)







#ow = OneWire(Pin('P13'))
#temp = DS18X20(ow)
#for num in range(0, 10):
#    print(temp.read_temp_async())
#    time.sleep(1)
#    temp.start_convertion()
#    time.sleep(1)

#pycom.rgbled(0x7f0000) # red
#pwm = machine.PWM(0, frequency=50)
#pwm_c = pwm.channel(0, pin='P12', duty_cycle=0.04)
#time.sleep(4)
#pwm_c.duty_cycle(0.112)
#time.sleep(4)
#pwm_c.duty_cycle(1)
#time.sleep(4)
#pwm_c.duty_cycle(0)

#p = Pin('P7', mode=Pin.OUT)
#for num in range(0, 141):
#    servoPulse(angle=angle)
#    angle = angle + 5
#for num in range(0, 141):
#    servoPulse(angle=angle)
#    angle = angle - 5

#print('rtc.now:'+str(rtc.now())+" utime.time:"+str(int(utime.time())))


def sub_cb(topic, msg):
    print(msg)


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
# pCont = PlatformController()


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
