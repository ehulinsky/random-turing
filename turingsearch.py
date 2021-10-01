import random
import turingmachine
import math
import time


# start searching seeds at a random location and search up from there
seed = random.randrange(1000000000)
steps = 0
maxCount = 0
# max times stores the maximum number of filled squares reached for each step in form: (step, value)
newMaxTimes = []


# base 2 logarithmic function, to search for binary counter
def targetFunction(x):
    return math.log(x)/math.log(2)

while 1:
    random.seed(seed)
    tm = turingmachine.ToroidalTuringMachine(50,20)
    tm.randomizeTable()
    for i in range(600):
        tm.step()
        steps += 1
        if tm.count > maxCount:
            maxCount = tm.count
        newMaxTimes += [(steps,maxCount)]
    
    if len(newMaxTimes) > 1:
        # find average squared error, comparing target function to 
        value = sum(map(lambda x:(targetFunction(x[0]) - x[1])**2, newMaxTimes))/len(newMaxTimes)
        # print likely candidates
        if value < 1:
            print(seed, value)


    newMaxTimes = []
    maxCount = 0
    steps = 0
    lastState = tm.state
    seed += 1