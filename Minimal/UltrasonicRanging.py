#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import pygame
import RPi.GPIO as GPIO
import time

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

class Rocket:
        def __init__ (self, x = 50, y = 50):
            self.x = x
            self.y = y
            self.moveDown = True
            self.image = pygame.image.load("rocket.png")
            
        def move(self, distance):
            inputHigh = distance
            if distance > 40:
                return
            if distance < 2:
                return
            if distance > 28:
                inputHigh = 28
            if distance < 3:
                inputHigh = 3
            if self.y < 600 - 50 - (inputHigh-3)*20 - 20:
                self.y += 12
            elif self.y > 600 - 50 - (inputHigh-3)*20 + 20:
                self.y -= 12
            if self.y > 550:
                self.y = 550
            if self.y < 50:
                self.y = 50
            
                

def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance


    
def setup():
    pygame.init()
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT)   #
    GPIO.setup(echoPin, GPIO.IN)    #

def loop():
    GPIO.setup(11,GPIO.IN)
    print ('How many times?')
    
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    clock = pygame.time.Clock()
    
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((800,600))

    rocket = Rocket()

    def drawScene():
        screen.fill((0, 0, 0))
        screen.blit(rocket.image, (rocket.x -35, rocket.y -35))
        pygame.display.update()

    
    while(True):
        clock.tick(18)
        distance = getSonar()
        print ("The distance is : %.2f cm"%(distance))
        rocket.move(distance)
        drawScene()

        #time.sleep(1)
        
if __name__ == '__main__':     #program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
        GPIO.cleanup()         #release resource


	
