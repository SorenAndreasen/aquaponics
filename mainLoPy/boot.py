import machine
from machine import UART
from network import WLAN
from machine import Pin
waterPump_p = Pin('P20', mode=Pin.OUT)
waterPump_p.value(1) # init water pump off
dosingPump_p = Pin('P19', mode=Pin.OUT)
dosingPump_p.value(1)
#from network import LoRa
#lora = LoRa(mode=LoRa.LORAWAN)
#from machine import SD
import socket
#import ssl
#import time
import os
import pycom
print('starting up..')
#sd = SD()
#os.mount(sd, '/sd')
#time.sleep(5)
#os.listdir('/sd')
#time.sleep(5)

uart = UART(0, 115200)
os.dupterm(uart)
pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # red

wlan = WLAN()
#print('SD mounted!')
if machine.reset_cause() != machine.SOFT_RESET:
    print('setting wlan config...')
    wlan.init(mode=WLAN.STA)
    wlan.ifconfig(config=('10.0.0.88', '255.255.255.0', '10.0.0.1', '8.8.8.8'))

if not wlan.isconnected():
    print('looking for network...')
    wlan.connect('NETGEAR64', auth=(WLAN.WPA2, 'oddchair195'), timeout=5000)
    while not wlan.isconnected():
        machine.idle()
print('connected to wifi!')

#s = socket.socket()
#ss = ssl.wrap_socket(s)
#ss.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
#print('connected to internet!')


#space = os.getfree('/flash')
#print('free flash mem: ', space)
#pycom.rgbled(0x007f00) # green
