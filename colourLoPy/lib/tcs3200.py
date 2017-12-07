import pycom
from pycom import pulses_get
import time
import utime
import machine
from machine import Timer
import gc
from machine import Pin
gc.enable()

s0 = Pin('P4', mode=Pin.OUT)
s1 = Pin('P11', mode=Pin.OUT)
s2 = Pin('P10', mode=Pin.OUT)
s3 = Pin('P9', mode=Pin.OUT)
sout = Pin('P8', mode=Pin.IN)
oe = Pin('P23', mode=Pin.OUT) # enable disable
s0.value(1) # set frequency scale to 100%
s1.value(1)
# 19000, 7000, 5000, 4000  white
# 7000, 2300, 2100, 2081 black
# 16000-20000, 6200, 5100, 6000, PH 7
# 130000, 7600, 4050, 3070, PH 3

s2Array = [0, 1, 0, 1] # arrays for setting color filters on sensor
s3Array = [0, 1, 1, 0] # red, green, blue, clear
whiteArray = [30000, 30000, 30000, 90000]
blackArray = [1000, 1000, 1000, 1000]
greyDiff = [(whiteArray[0]-blackArray[0]), (whiteArray[1]-blackArray[1]), (whiteArray[2]-blackArray[2]), (whiteArray[3]-blackArray[3])]
rgbArray = [0, 0, 0, 0] # r,g,b, clear
rgbArrayScaled = [0, 0, 0]

class OETIMER: # oe timer, sets oe pin high after 1 ms
    def __init__(self, timeout):
        self.__alarm = Timer.Alarm(self.setOEHighHandler, ms=timeout, periodic=False)

    def setOEHighHandler(self, alarm):
        oe.value(1)


class TCS3200:

    def go(self):
        self.getRGB()
        time.sleep(2)
        self.getRGBScaled()
        time.sleep(1)
        self.setLED()
    def getRGBScaled(self):
        clearFactor = (rgbArray[3] - blackArray[3]) / greyDiff[3]
        print('clearFactor: ', clearFactor)
        for num in range(0, 3):
            rgbArrayScaled[num] = (rgbArray[num] - blackArray[num])/(greyDiff[num])*255
            if rgbArrayScaled[num] > 255:
                rgbArrayScaled[num] = 255
            elif rgbArrayScaled[num] < 0:
                rgbArrayScaled[num] = 0
        return rgbArrayScaled

    def getRGB(self):
        for col in range(0, 4):
            for num in range(0, 3): # let sensor settle
                trash = self.collectData(1, 1500, 0, 10, col)
                time.sleep_ms(50)
            rgbArray[col] = self.collectData(1, 1500, 0, 10, col)
            time.sleep_ms(50)
        return rgbArray

    def collectData(self, timeout1, timeout2, printout, readings, fil):
        freqArray = []
        for num in range(0, readings):
            invalidData = 1
            while invalidData: # keep trying until we get a valid measurement
                s2.value(s2Array[fil]) # set colour filters
                s3.value(s3Array[fil])
                #s2.value(0) # set filter
                #s3.value(0)
                oe.value(0) # enable
                time.sleep_ms(1)
                oeTimer = OETIMER(timeout1) # set timer to turn off sensor
                data = pulses_get(sout, timeout2) # get period values
                time.sleep_ms(2)
                if len(data) > 3: # valid data
                    validData = 1
                    del data[-1] # delete last element
                    del data[-1] # delete last element
                    del data[0] # delete first element
                    if printout:
                        print('len: ', len(data))
                        print(data)
                    sum = 0
                    for trans in data:
                        sum += trans[1]
                    avrPeriodUs = sum / len(data) # average period in micro seconds
                    avrPeriodSec = avrPeriodUs / 1000000 # convert to seconds
                    avrFreq = 1 / avrPeriodSec # get frequency
                    freqArray.append(avrFreq)
                    time.sleep_ms(10)
                    # calc average frequency over all measurements
                    sum = 0
                    for f in freqArray:
                        sum += f
                    avr = sum / len(freqArray)
                    if printout:
                        print(freqArray)
                        print('avr freq: ', avr)
                    if fil == 0:
                        return (avr + 2000) # compensate for lack of red
                    elif fil == 1:
                        return (avr + 3000) # compensate for lack of green
                    else:
                        return avr
                else:
                    time.sleep_ms(20)


    def setLED():
        r = int(rgbArrayScaled[0])
        g = int(rgbArrayScaled[1])
        b = int(rgbArrayScaled[2])
        colour = ((r & 0xff) << 16) + ((g & 0xff) << 8) + (b & 0xff)
        print(r, ' ', g, ' ', b)
        pycom.rgbled(colour)

    def oldColour():
        cs.checkColour()
        rgb = cs.printColour()
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        #print(r, g, b)
        rgb = createRGB(r, g, b)
        pycom.rgbled(rgb)


