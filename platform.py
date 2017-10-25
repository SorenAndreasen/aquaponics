
import machine
from machine import Pin
from machine import ADC
import time
import utime
colourAnalysisPosition = 0
waterPosition = 0
testSyringePosition = 0

# Pin 19 = G6
# pin 20 = G7
# Pin 21 = G8
# Pin 22 = G9
class PlatformController:
    p1 = Pin('P19', mode=Pin.OUT)
    p2 = Pin('P20', mode=Pin.OUT)
    p3 = Pin('P21', mode=Pin.OUT)
    p4 = Pin('P22', mode=Pin.OUT)

    adc = machine.ADC()
    sensorPin = adc.channel(pin='P13', attn=ADC.ATTN_11DB) #G5 on expansion board
    currentPosition = 0

    def __init__(self):
        print("moving")

        self.p4.value(1)
        time.sleep(5)
        print("done")

    def moveToColourAnalysis(self):
        print("moving to colour analysis")
        if self.currentPosition < colourAnalysisPosition:
            self.p1.value(1)
            self.p2.value(0)
        elif self.currentPosition > colourAnalysisPosition:
            self.p1.value(0)
            self.p2.value(1)

        #while self.currentPosition != colourAnalysisPosition:
            # wait for platform to arrive at destination
        #self.p1.value(0)
        #self.p2.value(0)

    def moveToWater(self):
        print("moving to water")
        if currentPosition < waterPosition:
            self.p1.value(1)
            self.p2.value(0)
        elif currentPosition > waterPosition:
            self.p1.value(0)
            self.p2.value(1)

        #while self.currentPosition != waterPosition:
            # wait for platform to arrive at destination
        #self.p1.value(0)
        #self.p2.value(0)

    def moveToTestSyringe(self):
        print("moving to test syringe")
        if self.currentPosition < testSyringePosition:
            self.p1.value(1)
            self.p2.value(0)
        elif self.currentPosition > testSyringePosition:
            self.p1.value(0)
            self.p2.value(1)

        #while self.currentPosition != testSyringePosition:
            # wait for platform to arrive at destination
        #self.p1.value(0)
        #self.p2.value(0)

    def turnJarDownwards(self):
        print("turning jar downwards")


    def turnJarUpwards(self):
        print("turning jar upwards")
