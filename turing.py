import random
import time
from os import system, name
import pygame
import colorsys


seed = random.randint(0,1000000000)
#binary counter 434485148
#bonky ball 75357141
#windows 11 995612209
#giraffe 485395398
#snake eats its tail 538214588
#checkers 419209143
#wall 820547953
#drone build 888508048
#boot 784966256
#bricks 18558353
random.seed(seed)
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class ToroidalTuringMachine:

    # initialize a toroidal turing machine, with width (of connected square)
    # numStates (all set to clear tape, go to state 0, and not move), and head starts at pos 0 
    def __init__(self,width,numStates):
        #tape is a matrix of 1's and 0's
        self.tape = []
        for i in range(width):
            self.tape.append([0]*width)
        self.headPos = (int(width/2),int(width/2))
        self.state = 0
        self.width = width
        self.numStates = numStates
        # table stored as a map from (state, value) -> (new state, new value, move, )
        self.instructionTable = {}
        for i in range(self.numStates):
            self.instructionTable[(i,0)] = (0,(0,0),0)
            self.instructionTable[(i,1)] = (0,(0,0),0)


    def randomizeTable(self):
        for k in self.instructionTable:
            # keep order for backwards random compatability
            a = (random.randint(0,1),random.choice([(0,0),(0,-1),(0,1),(-1,0),(1,0)]),random.randint(0,self.numStates-1))
            self.instructionTable[k] = a[2],a[0],a[1]

    # move on toroidal tape by moveDist (0,1) (-1,0) etc
    def move(self,moveDist):
        self.headPos = ((self.headPos[0]+moveDist[0])%len(self.tape),(self.headPos[1]+moveDist[1])%len(self.tape))


    def step(self):
        newState,newValue,moveDist = self.instructionTable[(self.state,self.tape[self.headPos[0]][self.headPos[1]])]
        self.tape[self.headPos[0]][self.headPos[1]] = newValue
        self.move(moveDist)
        self.state = newState


    def printInstructionTable(self):
        for k in self.instructionTable:
            newState=self.instructionTable[k][0]
            newValue=self.instructionTable[k][1]
            direction=self.instructionTable[k][2]
            print('(s',k[0],', ',k[1],end=')➝',sep='')
            print('(s',newState,', ',newValue,', ',sep='',end='')
            if(direction==(0,0)):
                print('•',end='')
            if(direction==(0,1)):
                print('→',end='')
            if(direction==(1,0)):
                print('↓',end='')
            if(direction==(0,-1)):
                print('←',end='')
            if(direction==(-1,0)):
                print('↑',end='')
            print(')')

    def display(self,screen,screenWidth,screenHeight,font):
        
        cellSize = screenHeight/self.width
        for y in range(self.width):
            for x in range(self.width):
                color = (20,20,20) if self.tape[y][x]==0 else (255,255,255)
                pygame.draw.rect(screen,color,pygame.Rect(int((screenWidth-screenHeight)/2)+x*cellSize-1,y*cellSize-1,cellSize+2,cellSize+2))
        headColor = colorsys.hsv_to_rgb(self.state/self.numStates,1.0,1.0)
        headColor = (int(255*headColor[0]),int(255*headColor[1]),int(255*headColor[2]))
        pygame.draw.rect(screen,headColor,pygame.Rect(int((screenWidth-screenHeight)/2)+self.headPos[1]*cellSize-1,self.headPos[0]*cellSize-1,cellSize,cellSize))
pygame.init()
screen = pygame.display.set_mode((0,0))
black = 0,0,0

tm = ToroidalTuringMachine(50,20)
tm.randomizeTable()


width,height=pygame.display.get_surface().get_size()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('monospace', 30)
print(seed)

started = False
speed = 1
tm.printInstructionTable()
pygame.mouse.set_visible(False)
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
    time.sleep(0.005)
    pygame.display.flip()
