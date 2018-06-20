#!/usr/bin/env python3
# encoding: utf-8

from snake import Snake
import random
import os
import pygame, sys
from pygame.locals import *
from constants import *
from soundmanager import sound_manager

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.GAMESTATE = 'playing'
        self.size = USIZE * COLUMNS + 300, USIZE * ROWS
        self.score = 0
        self.isFruitShowing = False
        self.isLocked = False # 加锁，防止一个时间周期内改变两次方向，碰到蛇身第二节。
        self.isFullScreen = False
        self.fruitPos = None
        self.snake = Snake()
        self.speed = INITSPEED # FPS
        self.fpsClock = pygame.time.Clock()
#
        self.fontObj = pygame.font.SysFont('楷体', 20)
        self.scoreFont = pygame.font.SysFont('楷体', 32)

        self.screen = self.newScreen(self.size)
        pygame.display.set_caption('mysnake 1.0')

    def start(self):
        self.redraw()
        snake = self.snake

        while True:
            if self.isLocked:
                self.isLocked = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_f:
                        self.screen = self.newScreen(self.size, full=not self.isFullScreen)

                    if self.GAMESTATE == 'over' and event.key == K_RETURN:
                        print('Return press')
                        initGame()
                    if event.key == K_SPACE:
                        if self.GAMESTATE == 'playing':
                            self.GAMESTATE = 'pausing'
                            pygame.mixer.music.pause()
                        elif self.GAMESTATE == 'pausing':
                            self.GAMESTATE = 'playing'
                            pygame.mixer.music.unpause()
                    if self.GAMESTATE == 'playing' and not self.isLocked:
                        self.newDirection = ''
                        if event.key in (K_DOWN, K_s):
                            self.newDirection = 'down'
                        elif event.key in (K_UP, K_w):
                            self.newDirection = 'up'
                        elif event.key in (K_LEFT, K_a):
                            self.newDirection = 'left'
                        elif event.key in (K_RIGHT, K_d):
                            self.newDirection = 'right'
                        if snake.isValidDirection(self.newDirection):
                            snake.changeDirection(self.newDirection)
                            self.isLocked = True
                if event.type == QUIT:
                    #  pygame.quit()
                    sys.exit()
            if self.GAMESTATE == 'playing':
                result = self.checkCollision()
                if result == 0:
                    snake.moveForward()
                elif result == 1:
                    snake.moveForward(True)
                    self.score += 1
                    self.isFruitShowing = False
                    if self.speed < 15:
                        self.speed *= 1.1
                    if self.score in (30, 50, 65, 75) or\
                        (self.score > 75 and (self.score - 80) % 5 == 0):
                        sound_manager.play_cheer_sound()
                elif result == -1:
                    self.GAMESTATE = 'over'
                    sound_manager.play_fail_sound()
                    self.drawFinal()
                self.redraw()
            elif GAMESTATE == 'over':
                pygame.mixer.music.pause()
                self.drawFinal()
            pygame.display.update()
            self.fpsClock.tick(self.speed)

    def newScreen(self, size, full=False):
        screen = None
        if full:
            self.isFullScreen = True
            screen = pygame.display.set_mode(size, FULLSCREEN)
        else:
            self.isFullScreen = False
            screen = pygame.display.set_mode(size)
        return screen

    # 辅助函数
    def initGame(self):
        """重新开始游戏时，对游戏初始化"""
        self.score = 0
        self.GAMESTATE = 'playing'
        self.isFruitShowing = False
        self.fruitPos = None
        self.speed = INITSPEED
        self.snake = Snake()
        pygame.mixer.music.rewind()
        pygame.mixer.music.unpause()

    def drawFinal(self):
        screen = self.screen
        pygame.draw.rect(screen, RED, \
                (200, 120, 400, 300))
        pygame.draw.rect(screen, BLACK, \
                (210, 130, 380, 280))
        overText = self.scoreFont.render('GAME OVER!',\
                True, WHITE)
        scoreText = self.coreFont.render(u'最终得分: ' + str(self.score),\
                True, WHITE)
        promptText = self.fontObj.render(u'按 "回车键" 再玩一次',
                True, WHITE)
        self.screen.blit(overText, (300, 200))
        self.screen.blit(scoreText, (300, 240))
        self.screen.blit(promptText, (300, 290))


    def drawFruit(self):
        """生成并绘制食物"""
        if not self.isFruitShowing:
            tempPos = None
            while not tempPos or tempPos in self.snake.bodyList:
                fX = random.randint(0, ROWS-1)
                fY = random.randint(0, ROWS-1)
                tempPos = (fX, fY)
            self.fruitPos = tempPos
        pygame.draw.rect(self.screen, RED, \
                (self.fruitPos[0]*USIZE, self.fruitPos[1]*USIZE, USIZE, USIZE))
        self.isFruitShowing = True


    def redraw(self):
        self.screen.fill(GREEN)
        # 分割线
        pygame.draw.line(self.screen, RED, (502, 0), (502, 500), 3)
        promptText = self.fontObj.render(u'按 "空格键" 开始/暂停', True, WHITE)
        #  promptText2 = fontObj.render(u'开始/暂停', True, WHITE)
        scoreText = self.scoreFont.render(u'得分: ' + str(self.score), True, WHITE)
        self.screen.blit(promptText, (550, 100))
        #  screen.blit(promptText2, (560, 120))
        self.screen.blit(scoreText, (570, 220))
        # drawSnake()
        self.snake.draw_self(self.screen)
        self.drawFruit()


    def checkCollision(self):
        snake = self.snake
        # 吃到食物
        if tuple(snake.headPos) == self.fruitPos:
            sound_manager.play_eat_sound()
            return 1
        # 碰到自己身体
        if tuple(snake.headPos) in snake.bodyList[1:]:
            return -1
        return 0


if __name__ == '__main__':
    game = SnakeGame()
    game.start()
