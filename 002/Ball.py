import pygame, sys
import numpy as np
import math

class Ball:
    xspeed = 0
    yspeed = 0
    xpos = 0
    ypos = 0
    size = 0
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
            if (self.yspeed < 0):
                self.yspeed = -yspeed
            
        elif(y + yspeed > 700):
            self.ypos = 700
            if (self.yspeed > 0):
                self.yspeed = -yspeed

        else:
            self.ypos += yspeed

        # Check for bouncing on paddles 
        # Left paddle 1
        if(x < 40 and (paddle1.ypos - 20 <= y <= (paddle1.ypos + paddle1.length))):
            #Get contact point and set
            gradient = self.yspeed / self.xspeed
            diff = 40 - self.xpos
            self.ypos -= diff * gradient
            contactY = self.ypos - paddle1.ypos + 10
            self.xpos = 40
            #Calculate relative x and y speeds
            xRatio = 1 - np.abs(60-contactY)/180
            speed = np.sqrt(np.power(self.xspeed,2)+np.power(self.yspeed,2)) + 0.5
            self.xspeed = speed * xRatio
            self.yspeed = np.sqrt(np.power(speed,2)-np.power(self.xspeed,2)) 
            if contactY < 60:
                self.yspeed = -self.yspeed
            #print("Contact: " + str(contactY) + "  X: " + str(self.xspeed) + "  Y: " + str(self.yspeed) + "  Speed: " + str(speed))
            hit = 1
        # Right Paddle 2
        elif(x+20 > paddle2.xpos and (paddle2.ypos - 20 <= y <= (paddle2.ypos + paddle2.length))):
           #Get contact point and set
            gradient = self.yspeed / self.xspeed
            diff = self.xpos - paddle2.xpos + 20
            self.ypos -= diff * gradient
            contactY = self.ypos - paddle2.ypos + 10
            self.xpos = paddle2.xpos - 20
            #Calculate relative x and y speeds
            xRatio = 1 - np.abs(60-contactY)/180
            speed = np.sqrt(np.power(self.xspeed,2)+np.power(self.yspeed,2))
            if speed < 25:
                speed += 0.5
            self.xspeed = -(speed * xRatio)
            self.yspeed = np.sqrt(np.power(speed,2)-np.power(self.xspeed,2)) 
            if contactY < 60:
                self.yspeed = -self.yspeed
            #print("Contact: " + str(contactY) + "  X: " + str(self.xspeed) + "  Y: " + str(self.yspeed) + "  Speed: " + str(speed))
            hit = 1
        else:
            self.xpos += xspeed

        return hit

    def discretePos(self, binX, binY):
        #bally_ = np.max([np.min([int(self.ypos // (720 / binY+1)), binY-1]), 0])
        #ballx_ = np.max([np.min([int(self.xpos // (780 / binX+1)), binX-1]), 0])
        bally_ = int(self.ypos // (720 / binY+1))
        ballx = int(self.xpos // (780 / binX+1))
        return ballx_, bally_

    def discreteVel(self, binX, binY, maxX, maxY, paddle):

       #Catch the sily bug
        if math.isnan(self.yspeed):
            self.xspeed = 8
            self.yspeed = 6
            self.ypos = 720/2
            self.xpos = 780/2

        ballxvel_ = 0

        if (paddle.xpos > 600):
                ballxvel_ = int((self.xspeed + maxX) // ((maxX * 2) / binX))
                ballxvel_ = np.max([0, np.min([binX - 1, ballxvel_])])
        else:
            if self.xspeed > 0:
                ballxvel_ = int((-self.xspeed + maxX) // ((maxX * 2) / binX))
                ballxvel_ = np.max([0, np.min([binX - 1, ballxvel_])])
            else:
                ballxvel_ = int((self.xspeed + maxX) // ((maxX * 2) / binX))
                ballxvel_ = np.max([0, np.min([binX - 1, ballxvel_])])

        ballyvel_ = int((self.yspeed + maxY) // ((maxY * 2) / binY))
        ballyvel_ = np.max([0, np.min([binY - 1, ballyvel_])])

        return ballxvel_, ballyvel_
