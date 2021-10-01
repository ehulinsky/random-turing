import random
import time
from os import system, name
import pygame
import math
import turingmachine

seed = random.randint(0,1000000000)
#all seeds for 20 state 50 width
#binary counter 434485148
#binary counter 2: 260700664
#bonky ball 75357141
#windows 11 995612209
#giraffe 485395398
#snake eats its tail 538214588
#checkers 419209143
#wall 820547953
#drone build 888508048
#boot 784966256
#bricks 18558353

#construction 934773422
#false security path 424135065
#so close to perfection 113388331
#reflection 999905358
#fall thru hole 493108843
#cheker draw erase 301488471
#build lines 288426509
#transformation 62617459
#dominos draw eraase 445363045
#tunnel bore 422634187

# this seed controls which turing machine is generated
random.seed(seed)

        
        

pygame.init()

black = 0,0,0

tm = turingmachine.ToroidalTuringMachine(50,20)
tm.randomizeTable()




pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('monospace', 30)
print(seed)

started = True
speed = 1
tm.printInstructionTable()
pygame.mouse.set_visible(False)

maxCount = 0
newMaxTimes = []
lastState = 0

steps = 0


started = False
screen = pygame.display.set_mode((0,0))
width,height=pygame.display.get_surface().get_size()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                started = True
            if event.key == pygame.K_f:
                speed = 10 if speed==1 else 1

    screen.fill(black)
    if started:
        for i in range(speed):
            tm.step()

    tm.display(screen,width,height,myfont)
    tm.drawBrain(screen,width,height,lastState)
    lastState = tm.state
    time.sleep(0.005)
    pygame.display.flip()
