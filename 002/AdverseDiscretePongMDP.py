from random import randint
from Paddle import *
from Ball import *
import numpy as np

### MDP for a discrete version of the pong game ###
### returns state in vetor (paddle1YLocation, BallXLocation, BallYLocation, BallXVel, BallYVel) ###
#### init with ballType, and bin sizes ### 

class AdverseDiscretePongMDP():
    #paddle1 = 0
    #paddle2 = 0
    #pongball = 0

    def __init__(self, ballXbin, ballYbin, ballXvelbin, ballYvelbin, ballXvelmax, ballYvelmax):
        #Create the Paddles(x,y,length,width,speed,playernumber).
        self.paddle1 = Paddle(20, 300, 120, 20, 10, 2)
        self.paddle2 = Paddle(740, 300, 120, 20, 10, 2)

        randomx = randint(15,16)
        randomy = 0#randint(4,9)
        if(randint(0,1) == 1):
            randomx = -randomx
        #if(randint(0,1) == 1):
        #    randomy = -randomy
        self.pongball = Ball(780/2, 360 , randomx, randomy, 20)

        self.ballXBin = ballXbin
        self.ballYBin = ballYbin
        self.ballxvelBin = ballXvelbin
        self.ballyvelBin = ballYvelbin
        self.ballxvelMax = ballXvelmax
        self.ballyvelMax = ballYvelmax

    #Take action and update environment
    #Return new state of environment
    def update(self, a1, a2, steps):
    
        running = True
        r1, r2, hit, w1, w2 = 0, 0, 0, 0 ,0

        for i in range(0, steps):

            #Move paddle based on action
            self.paddle1.move(a1)
            self.paddle2.move(a2)

            hit = self.pongball.move(self.pongball.xpos, self.pongball.ypos, self.pongball.xspeed, self.pongball.yspeed, self.paddle1, self.paddle2)
      
            #Punish if ball is missed
            if (self.pongball.xpos < 0):
                r1 = -1
                r2 = 1
                w2 = 1
                running = False
                self.pongball.xpos = 0
                break
 
            if (self.pongball.xpos > 780):
                r2 = -1
                r1 = 1
                w1 = 1
                running = False
                self.pongball.xpos = 779
                break

            if hit == 1:
                self.pongball.xpos < 100
                r1 = 5
            else:
                r2 = 5

            #failsafe
            if (self.pongball.ypos < -20 or self.pongball.ypos > 800):
                running = False
                break


        #discreatise
        xv1, yv1 = self.pongball.discreteVel(self.ballxvelBin, self.ballyvelBin, self.ballxvelMax, self.ballyvelMax, self.paddle1)
        xv2, yv2 = self.pongball.discreteVel(self.ballxvelBin, self.ballyvelBin, self.ballxvelMax, self.ballyvelMax, self.paddle2)
        
        x1, y1 = self.relative1(self.paddle1)
        x2, y2 = self.relative2(self.paddle2)

        #return (x1, x2), (y1, y2), (xv1, xv2), (yv1, yv2), (r1, r2), (w1, w2), running, hit
        return ((x1, y1, xv1, yv1),(x2, y2, xv2, yv2)) , (r1, r2), (w1, w2), running, hit
        #return (p1, p2), (x, y, xv, yv), (r1, r2), (w1, w2), running, hit

    
    def relative1(self, paddle):
        xdiff = np.abs((paddle.xpos + 20) - self.pongball.xpos)
        xdiff = int((xdiff) // (780 / self.ballXBin))
        xdiff = np.max([0, np.min([xdiff, self.ballXBin-1])])
        
        ydiff = paddle.ypos - self.pongball.ypos;
        ydiff = int((ydiff + 720) // (720*2 / self.ballYBin))
        ydiff = np.max([0, np.min([ydiff, self.ballYBin-1])])

        return xdiff, ydiff

    def relative2(self, paddle):
        xdiff = np.abs(paddle.xpos - (self.pongball.xpos))
        xdiff = int((xdiff) // (780 / self.ballXBin))
        xdiff = np.max([0, np.min([xdiff, self.ballXBin-1])])
        
        ydiff = paddle.ypos - self.pongball.ypos;
        ydiff = int((ydiff + 720) // (720*2 / self.ballYBin))
        ydiff = np.max([0, np.min([ydiff, self.ballYBin-1])])

        return xdiff, ydiff

    def reset(self):
        self.paddle1.ypos = 300
        self.paddle2.ypos = 300

        randomx = randint(15,16)
        randomy =0# randint(4,9)
        if(randint(0,1) == 1):
            randomx = -randomx
        #if(randint(0,1) == 1):
        #    randomy = -randomy
        self.pongball.xpos = 780/2
        self.pongball.ypos = 720/2 
        self.pongball.xspeed = randomx
        self.pongball.yspeed = randomy

        #discreatise
        xv1, yv1 = self.pongball.discreteVel(self.ballxvelBin, self.ballyvelBin, self.ballxvelMax, self.ballyvelMax, self.paddle1)
        xv2, yv2 = self.pongball.discreteVel(self.ballxvelBin, self.ballyvelBin, self.ballxvelMax, self.ballyvelMax, self.paddle2)
        
        x1, y1 = self.relative1(self.paddle1)
        x2, y2 = self.relative2(self.paddle2)


        return ((x1, y1, xv1, yv1),(x2, y2, xv2, yv2)), True

    def observe(self):
        return self.paddle1, self.paddle2, self.pongball