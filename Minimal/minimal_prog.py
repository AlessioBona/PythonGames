#----------------------------- actual code --------------------------------

# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    
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
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    rocketY += rocketMove
                if event.key == pygame.K_UP:
                    rocketY -= rocketMove

        rocket.move()
        drawScene()


    

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
