import random
import pygame
import colorsys
import math

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
        # count of white squares
        self.count = 0
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

        oldValue = self.tape[self.headPos[0]][self.headPos[1]]
        self.tape[self.headPos[0]][self.headPos[1]] = newValue

        #boolean subtraction ok
        self.count += newValue - oldValue
        
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


    def stateToColor(self,state):
        color = colorsys.hsv_to_rgb(state/self.numStates,1.0,1.0)
        color = (int(255*color[0]),int(255*color[1]),int(255*color[2]))
        return color

    #displays the current state as white
    def brainColor(self,state):
        if(state == self.state):
            return (255,255,255)
        else:
            return self.stateToColor(state)


    def display(self,screen,screenWidth,screenHeight,font):
        cellSize = screenHeight/self.width
        for y in range(self.width):
            for x in range(self.width):
                color = (20,20,20) if self.tape[y][x]==0 else (255,255,255)
                pygame.draw.rect(screen,color,pygame.Rect(int((screenWidth-screenHeight)/2)+x*cellSize-1,y*cellSize-1,cellSize+2,cellSize+2))
        headColor = self.stateToColor(self.state)
        pygame.draw.rect(screen,headColor,pygame.Rect(int((screenWidth-screenHeight)/2)+self.headPos[1]*cellSize-1,self.headPos[0]*cellSize-1,cellSize,cellSize))
    
    
    
    def stateToBrainPoint(self,state,x,y,radius,width,height):
        return (x+radius*math.sin(2*math.pi*state/self.numStates),y-radius*math.cos(2*math.pi*state/self.numStates))
    def drawBrain(self,screen,width,height,lastState):
        radius = 150
        x = int((width-height)/4)
        y = int((width-height)/4)
        pygame.draw.line(screen,self.stateToColor(lastState),self.stateToBrainPoint(lastState,x,y,radius,width,height),self.stateToBrainPoint(self.state,x,y,radius,width,height),3)

        for i in range(self.numStates):
            pygame.draw.circle(screen,self.brainColor(i),self.stateToBrainPoint(i,x,y,radius,width,height),5)
