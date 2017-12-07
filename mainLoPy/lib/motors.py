import machine
from machine import Pin
import time
import pycom
from machine import ADC
from machine import PWM

adc = machine.ADC()
sensorPin = adc.channel(pin='P14', attn=ADC.ATTN_6DB) # G4 on expansion board
rgbArray = [0x7f0000, 0x007f00, 0x0000ff] # red, green, blue
red_p = Pin('P10', mode=Pin.OUT)
green_p = Pin('P9', mode=Pin.OUT)
blue_p = Pin('P7', mode=Pin.OUT)
ledArray = [red_p, green_p, blue_p]

step_p = Pin('P8', mode=Pin.OUT)
stepDir_p = Pin('P21', mode=Pin.OUT)
stepDir_p.value(0) # down


class MOTORS:

    dosingPump_p = Pin('P19', mode=Pin.OUT)
    dosingPump_p.value(0)
    time.sleep_ms(5)
    dosingPump_p.value(1)

    # SERVO:
    pwm = PWM(0, frequency=50)
    servo_p = pwm.channel(0, pin='P22', duty_cycle=0.127)
    servo_p.duty_cycle(0.107)

    buzPin = Pin('P12') # Pin Y2 with timer 8 Channel 2
    buzTimer = PWM(1, frequency=800)
    buzCh = buzTimer.channel(2, duty_cycle=0, pin=buzPin)
    # 0.107 # upright position
    # 0.03 # pouring position.. 0.028

    balanceSet = True
    colourArray = [0, 0, 0]
    whiteArray = [407.8, 1380.2, 512.2]
    blackArray = [0, 0, 0]
    avgRead = 0
    highestRead = 0

    def getAmbientLight(self):
        reading = sensorPin()
        return reading
    def shake(self):
        for num in range(0, 5): # shake
            self.servo_p.duty_cycle(0.122)
            time.sleep_ms(250)
            self.servo_p.duty_cycle(0.107)
            time.sleep_ms(250)
        time.sleep(1)
    def rinse(self):
        self.servo_p.duty_cycle(0.028) # pour out possible content
        time.sleep(5)
        self.servo_p.duty_cycle(0.107) # turn back glass
        time.sleep(2)
        for num in range(0, 3): # rinse glass 3 times
            self.dosingPump_p.value(0) # take in water from aquarium
            time.sleep(6) # how mwuch water to take in?
            self.dosingPump_p.value(1) # turn off dosing pump
            time.sleep(1)
            self.shake()
            self.servo_p.duty_cycle(0.028) # pour out possible content
            time.sleep(5)
            self.servo_p.duty_cycle(0.107) # turn back glass
            time.sleep(2)
    def takeInWater(self):
        self.dosingPump_p.value(0) # take in water from aquarium
        time.sleep(4) # 5 ml
        self.dosingPump_p.value(1) # turn off dosing pump
        time.sleep(1)
    def plungerManual(self, value, dir):
        if dir == 1:
            stepDir_p.value(1) # up
            for num in range(0, value): # take plunger down 1 ml
                step_p.value(1)
                time.sleep_ms(10)
                step_p.value(0)
                time.sleep_ms(10)
        else:
            stepDir_p.value(0) # down
            for num in range(0, value): # take plunger down 1 ml
                step_p.value(1)
                time.sleep_ms(10)
                step_p.value(0)
                time.sleep_ms(10)
    def plungerDown(self):
        stepDir_p.value(0) # down
        for num in range(0, 150): # take plunger down 1 ml
            step_p.value(1)
            time.sleep_ms(10)
            step_p.value(0)
            time.sleep_ms(10)
    def prepareSample(self):
        self.rinse()
        self.takeInWater()
        self.plungerDown()
        time.sleep(5)
        self.shake()
    def checkBalance(self):
        print("checking balance")
        if not self.balanceSet:
            self.setBalance()

    def setBalance(self):
        for num in range(0, 5): # warn user to insert white
            self.buzCh.duty_cycle(0.5)
            time.sleep(0.5)
            self.buzCh.duty_cycle(0)
            time.sleep(0.5)
        print("setting balance")
        for num in range(0, 3): # set white bal
            print('white ', num)
            #pycom.rgbled(rgbArray[num]) # set to color
            ledArray[num].value(1) # turn on respective color
            time.sleep(4)
            self.getReadings(60)
            #self.whiteArray[num] = self.avgRead # set to average
            self.whiteArray[num] = self.highestRead # set to highest
            #print('avgRead from white bal ', self.avgRead)
            print('highest from white bal ', self.highestRead)
            #pycom.rgbled(0x000000)
            ledArray[num].value(0) # turn off respective color
            time.sleep(0.1)
        for num in range(0, 10): # warn user to insert black
            self.buzCh.duty_cycle(0.5)
            time.sleep(0.25)
            self.buzCh.duty_cycle(0)
            time.sleep(0.25)
        for num in range(0, 3): # set black bal
            print('black ', num)
            #pycom.rgbled(rgbArray[num])
            ledArray[num].value(1) # turn on respective color
            time.sleep(4)
            self.getReadings(60)
            #self.blackArray[num] = self.avgRead
            self.blackArray[num] = self.highestRead # set to highest
            #print('avgRead from black bal ', self.avgRead)
            print('highest from black bal ', self.highestRead)
            #pycom.rgbled(0x000000) # turn off led
            ledArray[num].value(0) # turn off respective color
            time.sleep(0.1)
        self.balanceSet = True
        print("balanced set!")
        time.sleep(5)


    def checkColour(self):
        print("checking color...")
        for num in range(0, 3):
            #pycom.rgbled(rgbArray[num]) # set to color
            ledArray[num].value(1) # turn on respective color
            time.sleep(4) # allow cds to mastabilize
            self.getReadings(30)
            if self.avgRead > self.whiteArray[num]:
                self.colourArray[num] = self.whiteArray[num]
            else:
                self.colourArray[num] = self.avgRead

            print('avgRead: ', self.avgRead)
            print('whitearray ', self.whiteArray[num], ' blackArray ', self.blackArray[num])
            greyDiff = self.whiteArray[num] - self.blackArray[num]
            print('greydiff: ', greyDiff)

            # the reading returned minus the lowest value divided by the possible range multiplied
            # by 255 will give us a value roughly between 0-255 representing the value for the current
            # reflectivity(for the colour it is exposed to) of what is being scanned:
            self.colourArray[num] = (self.colourArray[num] - self.blackArray[num])/(greyDiff)*255

            #pycom.rgbled(0x000000) # turn off led
            ledArray[num].value(0) # turn off respective color
            time.sleep(0.1)

    def printColour(self):
        #print('printing colour')
        return self.colourArray[0], self.colourArray[1], self.colourArray[2]

    def getReadings(self, times):
        reading = 0
        tally = 0
        self.highestRead = 0
        for num in range(0, times+1):
            reading = sensorPin()
            if reading > self.highestRead:
                self.highestRead = reading
            #print('reading ', reading)
            tally = reading + tally
            time.sleep(0.1)
        self.avgRead = (tally)/times
        #print('avgRead ', self.avgRead)
