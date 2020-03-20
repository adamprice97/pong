from random import randint
from Paddle import *
from SimpleBall import *
import numpy as np

### MDP for a discrete version of the pong game ###
### returns state in vetor (paddle1YLocation, BallXLocation, BallYLocation, BallXVel, BallYVel) ###
#### init with ballType, and bin sizes ### 

class DiscretePongMDP():
    #paddle1 = 0
    #paddle2 = 0
    #pongball = 0

    def __init__(self, p1bin, ballXbin, ballYbin, ballXvelbin, ballYvelbin, ballXvelmax, ballYvelmax):
        #Create the Paddles(x,y,length,width,speed,playernumber).
        self.paddle1 = Paddle(740, 300, 120, 20, 10, 2)
        self.paddle2 = Paddle(20, 300, 120, 20, 10, 2)

        self.pongball = SimpleBall(780/2, 720/2 , 8, 6, 20)

        self.paddleBin = p1bin
        self.ballXBin = ballXbin
        self.ballYBin = ballYbin
        self.ballxvelBin = ballXvelbin
        self.ballyvelBin = ballYvelbin
        self.ballxvelMax = ballXvelmax
        self.ballyvelMax = ballYvelmax

    #Take action and update environment
    #Return new state of environment
    def update(self, a):
    
        running = True
        r = 0
        hit = 0

        #Move paddle based on action
        self.paddle2.move(self.paddle2.ypos, a, self.paddle2.number)
       
        #Follow Ball Y cord AI
        if (self.paddle1.ypos + 60 > self.pongball.ypos):
            a = 0
        else:
            a = 1
        self.paddle1.move(self.paddle1.ypos, a, self.paddle1.number)

        hit = self.pongball.move(self.pongball.xpos, self.pongball.ypos, self.pongball.xspeed, self.pongball.yspeed, self.paddle2, self.paddle1)

        
        ##Punish if ball is missed
        if (self.pongball.xpos < 0):
            r = -100
            running = False

        ##Reward if successful 
        if (self.pongball.xpos > 780):
            r = 100
            running = False

        #discreatise
        xv, yv = self.pongball.discreteVel(self.ballxvelBin, self.ballyvelBin, self.ballxvelMax, self.ballyvelMax)
        x, y = self.pongball.discretePos(self.ballXBin, self.ballYBin)
        p = self.paddle2.discretePos(self.paddleBin)

        return (p, x, y, xv, yv), r, running, hit

