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

    def move(self, k):
        if self.number == 1:
            if k[pygame.K_UP]:
                self.ypos -= 10 # self.speed
                if (self.ypos < 0):
                    self.ypos = 0
            if k[pygame.K_DOWN]:
                self.ypos += 10
                if(self.ypos > 600):
                    self.ypos = 600

        if self.number == 2:
            if k == 0:
                self.ypos -= 10 # self.speed
                if (self.ypos < 0):
                    self.ypos = 0
            if k == 1:
                self.ypos += 10
                if(self.ypos > 600):
                    self.ypos = 600

    def discretePos(self, Bin):
        return int(self.ypos // (720 / Bin+1))
 

