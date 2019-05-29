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

    # 游戏状态
    class GameState:
        def __init__(self):
            self.GAMESTATE = 'playing'
            self.screen_size = USIZE * COLUMNS + 300, USIZE * ROWS  # 屏幕尺寸
            self.score = 0  # 得分
            self.full_screen = False  # 是否全屏
            self.speed = INITSPEED # FPS，游戏速度

        def add_score(self):
            self.score += 1
            if self.speed < 15:
                self.speed *= 1.1
            if self.score in (30, 50, 65, 75) or\
                (self.score > 75 and (self.score - 80) % 5 == 0):
                sound_manager.play_cheer_sound()

    # 处理与食物有关的事情
    class FoodManager:
        def __init__(self):
            self.fruit_showing = False  # 当前是否有食物
            self.fruit_pos = None  # 食物位置

        def draw_fruit(self, screen, snake):
            """生成并绘制食物"""
            if not self.fruit_showing:
                tempPos = None
                while not tempPos or tempPos in snake.bodyList:
                    fX = random.randint(0, ROWS-1)
                    fY = random.randint(0, ROWS-1)
                    tempPos = (fX, fY)
                self.fruit_pos = tempPos
            pygame.draw.rect(screen, RED, \
                    (self.fruit_pos[0]*USIZE, self.fruit_pos[1]*USIZE, USIZE, USIZE))
            self.fruit_showing = True

        def hide_fruit(self):
            self.fruit_showing = False


    def __init__(self):
        pygame.init()

        self.gs = self.GameState()
        self.fm = self.FoodManager()

        self.new_direction_setted = False # 加锁，防止一个时间周期内改变两次方向，碰到蛇身第二节。

        self.snake = Snake()  # 蛇对象

        self.fpsClock = pygame.time.Clock()
#
        self.fontObj = pygame.font.Font('res/Kaiti_GB2312.ttf', 20)
        self.scoreFont = pygame.font.Font('res/Kaiti_GB2312.ttf', 32)

        self.screen = self.new_screen(self.gs.screen_size)
        pygame.display.set_caption('mysnake 1.0')

    def start(self):
        self.draw_board()
        snake = self.snake

        while True:
            if self.new_direction_setted:
                self.new_direction_setted = False
            for event in pygame.event.get():
                self.handle_key_event(event)

            if self.gs.GAMESTATE == 'playing':
                if snake.is_dead():
                    self.gameover()

                if self.snake_meet_food():
                    self.snake_eat_food()

                self.snake.moveForward()
                self.draw_board()
            elif self.gs.GAMESTATE == 'over':
                pygame.mixer.music.pause()
                self.drawFinal()
            pygame.display.update()
            self.fpsClock.tick(self.gs.speed)

    def handle_key_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_f:
                self.screen = self.new_screen(self.gs.screen_size, full=not self.gs.full_screen)

            if self.gs.GAMESTATE == 'over' and event.key == K_RETURN:
                print('Return press')
                self.initGame()
            if event.key == K_SPACE:
                if self.gs.GAMESTATE == 'playing':
                    self.gs.GAMESTATE = 'pausing'
                    pygame.mixer.music.pause()
                elif self.gs.GAMESTATE == 'pausing':
                    self.gs.GAMESTATE = 'playing'
                    pygame.mixer.music.unpause()
            if self.gs.GAMESTATE == 'playing' and not self.new_direction_setted:
                direction = ''
                if event.key in (K_DOWN, K_s):
                    direction = 'down'
                elif event.key in (K_UP, K_w):
                    direction = 'up'
                elif event.key in (K_LEFT, K_a):
                    direction = 'left'
                elif event.key in (K_RIGHT, K_d):
                    direction = 'right'
                if self.snake.isValidDirection(direction):
                    self.snake.changeDirection(direction)
                    self.new_direction_setted = True
        if event.type == QUIT:
            #  pygame.quit()
            sys.exit()

    def gameover(self):
        self.gs.GAMESTATE = 'over'
        sound_manager.play_fail_sound()
        self.drawFinal()

    def new_screen(self, size, full=False):
        screen = None
        if full:
            self.gs.full_screen = True
            screen = pygame.display.set_mode(size, FULLSCREEN)
        else:
            self.gs.full_screen = False
            screen = pygame.display.set_mode(size)
        return screen

    # 辅助函数
    def initGame(self):
        """重新开始游戏时，对游戏初始化"""
        self.score = 0
        self.gs.GAMESTATE = 'playing'
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
        scoreText = self.scoreFont.render(u'最终得分: ' + str(self.gs.score),\
                True, WHITE)
        promptText = self.fontObj.render(u'按 "回车键" 再玩一次',
                True, WHITE)
        self.screen.blit(overText, (300, 200))
        self.screen.blit(scoreText, (300, 240))
        self.screen.blit(promptText, (300, 290))


    def snake_eat_food(self):
        self.snake.grow()
        self.fm.hide_fruit()
        sound_manager.play_eat_sound()
        self.gs.add_score()


    def draw_board(self):
        self.screen.fill(GREEN)
        # 分割线
        pygame.draw.line(self.screen, RED, (502, 0), (502, 500), 3)
        promptText = self.fontObj.render('按 "空格键" 开始/暂停', True, WHITE)
        #  promptText2 = fontObj.render(u'开始/暂停', True, WHITE)
        scoreText = self.scoreFont.render('得分: ' + str(self.gs.score), True, WHITE)
        self.screen.blit(promptText, (550, 100))
        #  screen.blit(promptText2, (560, 120))
        self.screen.blit(scoreText, (570, 220))
        # drawSnake()
        self.snake.draw_self(self.screen)
        self.fm.draw_fruit(self.screen, self.snake)

    # 蛇遇到食物了
    def snake_meet_food(self):
        return tuple(self.snake.headPos) == self.fm.fruit_pos

    def checkCollision(self):
        snake = self.snake
        # 吃到食物
        if tuple(snake.headPos) == self.fm.fruit_pos:
            sound_manager.play_eat_sound()
            return 1
        # 碰到自己身体
        if tuple(snake.headPos) in snake.bodyList[1:]:
            return -1
        return 0


if __name__ == '__main__':
    game = SnakeGame()
    game.start()
