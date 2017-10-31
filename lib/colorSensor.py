import machine
from machine import Pin
import time
import pycom
from machine import ADC

adc = machine.ADC()
sensorPin = adc.channel(pin='P14', attn=ADC.ATTN_11DB) # G4 on expansion board
ledArray = [0x7f0000, 0x007f00, 0x0000ff] # red, green, blue



class ColorSensor:

    balanceSet = False
    colourArray = [0, 0, 0]
    whiteArray = [0, 0, 0]
    blackArray = [0, 0, 0]
    avgRead = 0


    def checkBalance(self):
        print("checking balance")
        if not self.balanceSet:
            self.setBalance()

    def setBalance(self):
        print("setting balance")
        time.sleep(5)
        for num in range(0, 3): # set white bal
            print(num)
            pycom.rgbled(ledArray[num]) # set to color
            time.sleep(0.1)
            self.getReadings(5)
            self.whiteArray[num] = self.avgRead
            print('avgRead from bal ', self.avgRead)
            pycom.rgbled(0x000000) # turn off led
            time.sleep(0.1)
        time.sleep(5)
        for num in range(0, 3): # set black bal
            pycom.rgbled(ledArray[num])
            time.sleep(0.1)
            self.getReadings(5)
            self.blackArray[num] = self.avgRead
            pycom.rgbled(0x000000) # turn off led
            time.sleep(0.1)
        self.balanceSet = True
        time.sleep(5)


    def checkColour(self):
        print("checking colour")
        for num in range(0, 3):
            pycom.rgbled(ledArray[num]) # set to color
            time.sleep(0.1)
            self.getReadings(5)
            self.colourArray[num] = self.avgRead
            print('whitearray ', self.whiteArray[num], ' blackArray ', self.blackArray[num])
            greyDiff = self.whiteArray[num] - self.blackArray[num]
            print('greydiff: ', greyDiff)
            self.colourArray[num] = (self.colourArray[num] - self.blackArray[num])/(greyDiff)*255
            pycom.rgbled(0x000000) # turn off led
            time.sleep(0.1)

    def printColour(self):
        print('printing colour')
        return self.colourArray[0], self.colourArray[1], self.colourArray[2]

    def getReadings(self, times):
        reading = 0
        tally = 0
        for num in range(0, times+1):
            reading = sensorPin()
            print('reading ', reading)
            tally = reading + tally
            time.sleep(0.01)
        self.avgRead = (tally)/times
        print('avgRead ', self.avgRead)
        #print('avgRead ', avgRead)
