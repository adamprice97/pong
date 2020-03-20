import pygame, sys
from pygame.locals import *

### Credit to Will Baumbach for the code that   ###
### formed the starting point of this game      ###
### https://github.com/WillBaumbach/Pong-Python ###

class Paddle:
    def __init__(self, x, y, l, w, s, n):
        self.ypos = y
        self.xpos = x
        self.length = l
        self.width = w
        self.speed = s
        self.number = n

    def move(self, ypos, k, playernumber):
        if playernumber == 1:
            if k[pygame.K_UP]:
                if(ypos-self.speed < -60):
                    self.ypos = -60
                else:
                    self.ypos -= 10 # self.speed
            if k[pygame.K_DOWN]:
                if(ypos+self.length+self.speed > 780):
                    self.ypos = 780-self.length
                else:
                    self.ypos += 10# self.speed

        if playernumber == 2:
            if k == 0:
                self.ypos -= 10 # self.speed
                if (self.ypos < 0):
                    self.ypos = 0
            if k == 1:
                self.ypos += 10
                if(self.ypos > 720):
                    self.ypos = 720

    def discretePos(self, Bin):
        return int(self.ypos // (720 / Bin+1))
 

