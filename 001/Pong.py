import pygame, sys
from pygame.locals import *
from Paddle import *
from SimpleBall import *
from Scorer import *
from random import randint
import numpy as np

### Credit to Will Baumbach for the code that   ###
### formed the starting point of this game      ###
### https://github.com/WillBaumbach/Pong-Python ###

#Start Pygame
pygame.init()
pygame.font.init()
running = True
limit = 2

#Variables.
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 720
FRAMERATE = 60
BG = pygame.image.load("assets/pongBG.jpg")
FONT = pygame.font.Font("assets/munro.ttf", 30)

#Create screen, clock, and name window.
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()

#Create the scorer
scorer = Score()

#Create the Paddles(x,y,length,width,speed,playernumber).
paddle1 = Paddle(740, 300, 120, 20, 10, 1)
paddle2 = Paddle(20, 300, 120, 20, 10, 2)

#Spawn the Ball(x, y, xspeed, yspeed, size)
randomx = 8
if(randint(0,1) == 1):
    randomx = -randomx
pongball = SimpleBall(SCREEN_WIDTH/2, randint(20,700) , randomx, 6, 20)

#Draw a padle on the screen.
def drawPaddle(x, y, length, width):
    pygame.draw.rect(DISPLAYSURF, (255,255,255), (x,y,length,width))

#Draw the ball on the screen.
def drawBall(x, y, size):
    pygame.draw.rect(DISPLAYSURF, (255,255,255), (x,y,size,size))

#Game Loop
while True:
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

       
        k = pygame.key.get_pressed()
        paddle1.move(paddle1.ypos, k, paddle1.number)

         #Follow Ball Y cord AI
        if (paddle2.ypos + 60 > pongball.ypos):
            a = 0
        else:
            a = 1
        paddle2.move(paddle2.ypos, a, paddle2.number)
        pongball.move(pongball.xpos, pongball.ypos, pongball.xspeed, pongball.yspeed, paddle2, paddle1)
        
        #Drawing screen
        DISPLAYSURF.blit(BG, (0,0))
        
        #Draw ball and paddles
        drawBall(pongball.xpos, pongball.ypos, pongball.size)
        drawPaddle(paddle1.xpos, paddle1.ypos, paddle1.width, paddle1.length)
        drawPaddle(paddle2.xpos, paddle2.ypos, paddle2.width, paddle2.length)

        #Check for a point
        scorer.checkPoint(pongball.xpos, pongball, SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE)
        scorer.printScore(scorer.player1score, scorer.player2score)
        running = scorer.checkWin(scorer.player1score, scorer.player2score, 2)

        #Update display and tick clock.
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FRAMERATE)

    while not running:
        
        if(scorer.player1score == limit):
            string = "You win!"
            winText = FONT.render(string, True, (255,255,255))
            DISPLAYSURF.blit(winText, (100,200))
            pygame.display.update()
            
        else:
            string = "CPU wins!"
            winText = FONT.render(string, True, (255,255,255))
            DISPLAYSURF.blit(winText, (500,200))
            pygame.display.update()
        

        # Update display and tick clock.     
        pygame.display.flip()
        clock.tick(FRAMERATE)
