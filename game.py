#!/usr/bin/env python3
# encoding: utf-8
import sys

import pygame
from pygame.locals import *

from constants import *
from food_manager import food_manager
from game_board import GameBoard
from game_state import GameState
from snake import Snake
from sound_manager import sound_manager


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.game_state = GameState()  # 当前游戏状态
        self.snake = Snake()  # 蛇
        self.board = GameBoard(self.game_state, self.snake)  # 画板
        self.fpsClock = pygame.time.Clock()

        self.new_direction_setted = False  # 加锁，防止一个时间周期内改变两次方向，碰到蛇身第二节。

        pygame.display.set_caption(TITLE)

    def start(self):
        self.board.draw()

        while True:
            if self.new_direction_setted:
                self.new_direction_setted = False
            for event in pygame.event.get():
                self.handle_key_event(event)

            if self.game_state.STATE == 'playing':
                if self.snake.is_dead():
                    self.gameover()

                elif self.snake_meet_food():
                    self.snake_eat_food()

                self.snake.moveForward()
                self.board.draw()
            elif self.game_state.STATE == 'over':
                sound_manager.pause_music()
                self.board.drawFinal()
            pygame.display.update()
            self.fpsClock.tick(self.game_state.speed)

    def handle_key_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_f:
                self.board.toggle_screen()

            if self.game_state.STATE == 'over' and event.key == K_RETURN:
                print('Return press')
                self.initGame()
            if event.key == K_SPACE:
                if self.game_state.STATE == 'playing':
                    self.game_state.STATE = 'pausing'
                    pygame.mixer.music.pause()
                elif self.game_state.STATE == 'pausing':
                    self.game_state.STATE = 'playing'
                    pygame.mixer.music.unpause()
            if self.game_state.STATE == 'playing' and not self.new_direction_setted:
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
        self.game_state.STATE = 'over'
        sound_manager.play_fail_sound()
        self.board.drawFinal()


    # 辅助函数
    def initGame(self):
        """重新开始游戏时，对游戏初始化"""
        self.game_state = GameState()
        self.new_direction_setted = False  # 加锁，防止一个时间周期内改变两次方向，碰到蛇身第二节。
        self.snake = Snake()  # 蛇对象
        self.board.update(self.game_state, self.snake)  # 画板
        sound_manager.replay_music()


    def snake_eat_food(self):
        self.snake.grow()
        food_manager.hide_fruit()
        sound_manager.play_eat_sound()
        self.game_state.add_score()

    # 蛇遇到食物了
    def snake_meet_food(self):
        return tuple(self.snake.headPos) == food_manager.fruit_pos

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
