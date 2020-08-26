from random import random, randrange

def double (x):
    if isinstance (x, int):
        if x > 0:
            return x + x
        else:
            raise ValueError ()
    else:
        raise TypeError ()

def getRandomInput ():
    choice = random ()
    if choice < 0.75:
        return randrange (1, 1001) # valid input 1 to 1000
    elif choice < 0.85:
        return -randrange (1001) # invalid input -1000 to 0
    else:
        return random () * 1000 # invalid input 0.0 to 1000.0

function = double
nTestCases = 100
dataFileName = 'TestData'
