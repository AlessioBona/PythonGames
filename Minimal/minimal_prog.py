#----------------------------- actual code --------------------------------

# import the pygame module, so you can use it
import pygame
import RPi.GPIO as GPIO
import time

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220 #define the maximum measured distance
timeOut = MAX_DISTANCE*60 #calculate timeout according to the maximum measured distance

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
    
def getSonar(): #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH) #make trigPin send 10us high level
    time.sleep(0.00001) #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut) #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0 # the sound speed is 340m/s, and calculate distance
    return distance

def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD) #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT) #
    GPIO.setup(echoPin, GPIO.IN) #

# define a main function
def main():

    # initialize the pygame module
    pygame.init()
    clock = pygame.time.Clock()
    
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
    
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((800,600))
    
    # define a variable to control the main loop
    running = True

    class Rocket:
        def __init__ (self, x = 50, y = 50):
            self.x = x
            self.y = y
            self.moveDown = True
            self.image = pygame.image.load("rocket.png")
            
        def move(self):
            if self.y == 50:
                self.moveDown = True
            if self.moveDown == False:
                self.y -= 1
            if self.moveDown == True:
                self.y += 1
            if self.y == 600 - 50:
                self.moveDown = False

    rocket = Rocket()
    rocketMove = 10



    def drawScene():
        screen.fill((0, 0, 0))
        screen.blit(rocket.image, (rocket.x -35, rocket.y -35))
        pygame.display.update()



    
    # main loop
    while running:

        clock.tick(1)
        #GPIO.setup(11,GPIO.IN)
        distance = getSonar()
        print ("The distance is : %.2f cm"%(distance))
        
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                GPIO.cleanup()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    rocket.y += rocketMove
                if event.key == pygame.K_UP:
                    rocket.y -= rocketMove

        rocket.move()
        drawScene()


    

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    setup()
    main()
