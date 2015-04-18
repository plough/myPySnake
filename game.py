#!/usr/bin/env python
# encoding: utf-8
# BUG: 快速转方向时，舌头可能会咬到第二节身体，导致游戏非正常结束

from snake import Snake
import random
import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800, 500))
pygame.display.set_caption('mysnake 1.0')

# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
#
USIZE = 20 # 单位长度
ROWS = 25
COLUMNS = 25
GAMESTATE = 'playing'
score = 0
isFruitShowing = False
fruitPos = None
snake = Snake()
#
INITSPEED = 5
speed = INITSPEED # FPS
fpsClock = pygame.time.Clock()
#
fontObj = pygame.font.Font('freesansbold.ttf', 20)
scoreFont = pygame.font.Font('freesansbold.ttf', 32)


# 辅助函数
def initGame():
    """重新开始游戏时，对游戏初始化"""
    global score, GAMESTATE, isFruitShowing, fruitPos,\
            speed, snake
    score = 0
    GAMESTATE = 'playing'
    isFruitShowing = False
    fruitPos = None
    speed = INITSPEED
    snake = Snake()
def drawFinal():
    pygame.draw.rect(DISPLAYSURF, RED, \
            (200, 120, 400, 300))
    pygame.draw.rect(DISPLAYSURF, BLACK, \
            (210, 130, 380, 280))
    overText = scoreFont.render('GAME OVER!',\
            True, WHITE)
    scoreText = scoreFont.render('Your Score: ' + str(score),\
            True, WHITE)
    promptText = fontObj.render('Press "ENTER" to RESTART',
            True, WHITE)
    DISPLAYSURF.blit(overText, (300, 200))
    DISPLAYSURF.blit(scoreText, (300, 240))
    DISPLAYSURF.blit(promptText, (280, 290))

def drawFruit():
    """生成并绘制食物"""
    global isFruitShowing, fruitPos
    if not isFruitShowing:
        tempPos = None
        while not tempPos or tempPos in snake.bodyList:
            fX = random.randint(0, ROWS-1)
            fY = random.randint(0, ROWS-1)
            tempPos = (fX, fY)
        fruitPos = tempPos
    pygame.draw.rect(DISPLAYSURF, RED, \
            (fruitPos[0]*USIZE, fruitPos[1]*USIZE, USIZE, USIZE))
    isFruitShowing = True

def drawSnake():
    for pos in snake.bodyList:
        pygame.draw.rect(DISPLAYSURF, WHITE, \
                (pos[0]*USIZE, pos[1]*USIZE, USIZE, USIZE))

def redraw():
    DISPLAYSURF.fill(BLACK)
    # 分割线
    pygame.draw.line(DISPLAYSURF, RED, (502, 0), (502, 500), 3)
    promptText = fontObj.render('Press "SPACE" to', True, WHITE)
    promptText2 = fontObj.render('START/PAUSE', True, WHITE)
    scoreText = scoreFont.render('Score: ' + str(score), True, WHITE)
    DISPLAYSURF.blit(promptText, (550, 100))
    DISPLAYSURF.blit(promptText2, (560, 120))
    DISPLAYSURF.blit(scoreText, (570, 220))
    drawSnake()
    drawFruit()

def checkCollision():
    # 吃到食物
    if tuple(snake.headPos) == fruitPos:
        return 1
    # 碰到自己身体
    if tuple(snake.headPos) in snake.bodyList[1:]:
        return -1
    return 0

redraw()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if GAMESTATE == 'over' and event.key == K_RETURN:
                print 'Return press'
                initGame()
            if event.key == K_SPACE:
                if GAMESTATE == 'playing':
                    GAMESTATE = 'pausing'
                elif GAMESTATE == 'pausing':
                    GAMESTATE = 'playing'
            if GAMESTATE == 'playing':
                newDirection = ''
                if event.key == K_DOWN:
                    newDirection = 'down'
                elif event.key == K_UP:
                    newDirection = 'up'
                elif event.key == K_LEFT:
                    newDirection = 'left'
                elif event.key == K_RIGHT:
                    newDirection = 'right'
                if snake.isValidDirection(newDirection):
                    snake.changeDirection(newDirection)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if GAMESTATE == 'playing':
        result = checkCollision()
        if result == 0:
            snake.moveForward()
        elif result == 1:
            snake.moveForward(True)
            score += 1
            isFruitShowing = False
            if speed < 15:
                speed *= 1.1
        elif result == -1:
            GAMESTATE = 'over'
            drawFinal()
        redraw()
    elif GAMESTATE == 'over':
        drawFinal()
    pygame.display.update()
    fpsClock.tick(speed)
