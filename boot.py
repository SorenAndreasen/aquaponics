import machine
from machine import UART
from network import WLAN
from machine import SD
import socket
import ssl
import time
import os
import pycom
print('starting up..')
sd = SD()
os.mount(sd, '/sd')
time.sleep(5)
os.listdir('/sd')
time.sleep(5)



uart = UART(0, 115200)
os.dupterm(uart)
pycom.heartbeat(False)
wlan = WLAN()
print('SD mounted!')
if machine.reset_cause() != machine.SOFT_RESET:
    print('setting wlan config...')
    wlan.init(mode=WLAN.STA)
    wlan.ifconfig(config=('10.0.0.88', '255.255.255.0', '10.0.0.1', '8.8.8.8'))

if not wlan.isconnected():
    print('looking for network...')
    pycom.rgbled(0x7f0000) # red
    wlan.connect('NETGEAR64', auth=(WLAN.WPA2, 'oddchair195'), timeout=5000)
    while not wlan.isconnected():
        machine.idle()
print('connected to wifi!')

s = socket.socket()
ss = ssl.wrap_socket(s)
ss.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
print('connected to internet!')
pycom.rgbled(0x007f00) # green
space = os.getfree('/flash')
print('free flash mem: ', space)
