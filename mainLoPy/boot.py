import machine
from machine import UART
from network import WLAN
from machine import Pin
waterPump_p = Pin('P20', mode=Pin.OUT)
waterPump_p.value(1) # init water pump off
dosingPump_p = Pin('P19', mode=Pin.OUT)
dosingPump_p.value(1)

import socket
import os
import pycom
print('starting up..')

uart = UART(0, 115200)
os.dupterm(uart)
pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # red

wlan = WLAN()

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
