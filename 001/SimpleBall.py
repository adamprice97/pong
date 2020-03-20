import pygame, sys
import numpy as np

class SimpleBall:

    pause = 0
    def __init__(self, x, y, xspeed, yspeed, size):
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.xpos = x
        self.ypos = y
        self.size = size


    def move(self, x, y, xspeed, yspeed, paddle1, paddle2):

        hit = 0 

        if(self.pause > 0):
            self. pause -= 1
            return
        
        # Check for bouncing on the top and bottom wall.
        if(y + yspeed < 0):
            self.ypos = 0
            self.yspeed = -yspeed
            
        elif(y + yspeed > 720):
            self.ypos = 720
            self.yspeed = -yspeed

        else:
            self.ypos += yspeed

        # Check for bouncing on paddles 
        # Left paddle
        if(x < 40 and (paddle1.ypos - 20 <= y <= (paddle1.ypos + paddle1.length))):
            self.xspeed -= 0.5
            self.xspeed = -self.xspeed
            self.xpos = 40

            if (self.yspeed > 0):
                self.yspeed += 0.5
            else:
                self.yspeed -= 0.5

            hit = 1
        # Right Paddle 
        elif(x > 720 and (paddle2.ypos - 20 <= y <= (paddle2.ypos + paddle2.length))):

            self.xspeed += 0.5
            self.xspeed = -self.xspeed
            self.xpos = 720

            if (self.yspeed > 0):
                self.yspeed += 0.5
            else:
                self.yspeed -= 0.5
            
            hit = 1
        else:
            self.xpos += xspeed

        return hit

    def discretePos(self, binX, binY):
        bally_ = int(self.ypos // (720 / binY+1)) 
        ballx_ = np.max([np.min([int(self.xpos // (780 / binX+1)), binX-1]), 0])

        return ballx_, bally_

    def discreteVel(self, binX, binY, maxX, maxY):
        ballxvel_ = int((self.xspeed + maxX) // ((maxX * 2) / binX))
        ballxvel_ = np.min([binX - 1, ballxvel_])
        ballxvel_ = np.max([0, ballxvel_])

        ballyvel_ = int((self.yspeed + maxY) // ((maxY * 2) / binY))
        ballyvel_ = np.min([binY - 1, ballyvel_])
        ballyvel_ = np.max([0, ballyvel_])

        return ballxvel_, ballyvel_




