import pygame, sys
from pygame.locals import *
from Paddle import *
from Ball import *
from Scorer import *
from random import randint
import numpy as np
import os
import time
from AdverseDiscretePongMDP import *

### Credit to Will Baumbach for the code that   ###
### formed the starting point of this game      ###
### https://github.com/WillBaumbach/Pong-Python ###

#Start Pygame
pygame.init()
pygame.font.init()
limit = 3
qAgent = 2
qTable1 = np.load('q_table1_end002.npy') 
qTable2 = np.load('q_table2_end002.npy') 
MaxSpeed = 20
buffer = 1 
#Variables.
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 720
FRAMERATE = 60
BG = pygame.image.load("assets/pongBG.jpg")
FONT = pygame.font.Font("assets/munro.ttf", 30)
SCOREFONT = pygame.font.Font("assets/munro.ttf", 48)

#Create screen, clock, and name window.
os.environ['SDL_VIDEO_CENTERED'] = '1'
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()

# Create the scorer
scorer = Score()
game = AdverseDiscretePongMDP(qTable2.shape[0], qTable2.shape[1], qTable2.shape[2], qTable2.shape[3], MaxSpeed, MaxSpeed)
s, running = game.reset()
# Draw a padle on the screen.
def drawPaddle(x, y, length, width):
    pygame.draw.rect(DISPLAYSURF, (255,255,255), (x,y,length,width))

# Draw the ball on the screen.
def drawBall(x, y, size):
    pygame.draw.rect(DISPLAYSURF, (255,255,255), (x,y,size,size))

time.sleep(7)
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    a2 = 2

    k = pygame.key.get_pressed()
    if k[pygame.K_UP]:
        a2 = 0
    if k[pygame.K_DOWN]:
        a2 = 1

    if (qAgent==0):
            #Follow Ball Y cord AI
        if (game.paddle1.ypos + 60 > game.pongball.ypos):
            a = 0
        else:
            a = 1
    elif qAgent==1:
        actions = qTable1[s[0]][:]
        a1 = np.argmax(actions)
    elif qAgent==2:
        actions = qTable1[s[0]][:]
        a1 = np.argmax(actions)
        actions = qTable2[s[1]][:]
        a2 = np.argmax(actions)

    s, r, w, running, hit = game.update(a1,a2, buffer)
        

    # Drawing screen
    DISPLAYSURF.blit(BG, (0,0))
        
    # Draw ball and paddles
    drawBall(game.pongball.xpos, game.pongball.ypos, game.pongball.size)
    drawPaddle(game.paddle1.xpos, game.paddle1.ypos, game.paddle1.width, game.paddle1.length)
    drawPaddle(game.paddle2.xpos, game.paddle2.ypos, game.paddle2.width, game.paddle2.length)

    # Check for a point
    if scorer.checkPoint(game.pongball.xpos, game.pongball, game.paddle1, game.paddle2, SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE) == 1:
        game.reset()
    running = scorer.checkWin(scorer.player1score, scorer.player2score, limit)

    string = str(scorer.player1score)
    score = SCOREFONT.render(string, True, (255,255,255))
    DISPLAYSURF.blit(score, (180,20))

    string = str(scorer.player2score)
    score = SCOREFONT.render(string, True, (255,255,255))
    DISPLAYSURF.blit(score, (560,20))

    string = "Q-Agent"
    score = FONT.render(string, True, (255,255,255))
    DISPLAYSURF.blit(score, (180,670))

    string = "Me!"
    score = FONT.render(string, True, (255,255,255))
    DISPLAYSURF.blit(score, (550,670))

    # Update display and tick clock.
    pygame.display.update()
    pygame.display.flip()
    clock.tick(FRAMERATE)

# WIP: Trying to implement a game over screen with "Play again" and "Quit"
while not running:
        
    # Print box for "Play Again"
    # pygame.draw.rect(DISPLAYSURF, (0,204,0), (100,375,200,150))
    # Print box for "Exit"
    # pygame.draw.rect(DISPLAYSURF, (204,0,0), (480,375,200,150))
    if(scorer.player1score == limit):
        string = "Player 1 wins!"
        winText = FONT.render(string, True, (255,255,255))
        DISPLAYSURF.blit(winText, (100,200))
        pygame.display.update()
            
    else:
        string = "Player 2 wins!"
        winText = FONT.render(string, True, (255,255,255))
        DISPLAYSURF.blit(winText, (500,200))
        pygame.display.update()
        

    # Update display and tick clock.
        
    pygame.display.flip()
    clock.tick(FRAMERATE)

