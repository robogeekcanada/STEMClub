#Robo-Geek 2016 original code

import pygame

#colors settings RGB
WHITE   = (255,255,255)
BLACK   = (0,0,0)
RED     = (255,0,0)
BLUE    = (0,0,255)
GREEN   = (0,255,0)

pygame.init()

#screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)


#Game Loop------------------
gameLoop = True
fps = pygame.time.Clock()

while gameLoop:

    #exit management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False

    #start with a blank canvas
    screen.fill(WHITE)

    #drawing examples
    pygame.draw.line(screen, GREEN, [0,0],[50,50],20)

    pygame.draw.rect(screen, BLACK, [75,10,50,20],2)
    pygame.draw.rect(screen, RED, [75,10,49,19])
    
    pygame.draw.ellipse(screen, BLACK, [255,10,50,20],2)
    pygame.draw.ellipse(screen, BLUE, [255,10,48,18])
    

    pygame.draw.circle(screen, BLUE, [60,250],25) 

    #refresh the screen at fps
    pygame.display.flip()
    fps.tick(60)

pygame.quit()

#End of Game Loop---------------
