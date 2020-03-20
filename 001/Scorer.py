from random import *

### Credit to Will Baumbach for the code that   ###
### formed the starting point of this game      ###
### https://github.com/WillBaumbach/Pong-Python ###

class Score:
    
    def __init__(self):
        self.player1score = 0
        self.player2score = 0

    def checkPoint(self, x, ball, width, height, framerate):
        if(x < 0):
            self.player2score += 1
            ball.xpos = width/2
            ball.ypos = height/2
            ball.xspeed = 8
            ball.yspeed = 6
            ball.pause = 2 * framerate
        elif(x > 760):
            self.player2score += 1
            ball.xpos = width/2
            ball.ypos = height/2
            ball.xspeed = 8
            ball.yspeed = 6
            ball.pause = 2 * framerate

    def printScore(self, p1, p2):
        n = 0

    def checkWin(self, p1, p2, limit):
        if(p1 == limit):
            return False
        elif(p2 == limit):
            return False 
        else:
            return True
