#!/usr/bin/env python3
# encoding: utf-8

"""
 游戏主逻辑 & 入口类

 Created by plough on 2019/7/5.
"""

import sys

import pygame
from pygame.locals import *

from constants import *
from core.game_board import GameBoard
from core.game_state import GameState
from core.snake import Snake
from libs.sound_manager import sound_manager


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.game_state = GameState()  # 当前游戏状态
        self.snake = self.create_snake()  # 蛇
        self.board = GameBoard()  # 画板
        self.fpsClock = pygame.time.Clock()

        self.new_direction_setted = False  # 加锁，防止一个时间周期内改变两次方向，碰到蛇身第二节。

        pygame.display.set_caption(TITLE)

    def start(self):
        self.board.draw(self.snake, self.game_state.score)

        # 游戏主循环
        while True:
            if self.new_direction_setted:
                self.new_direction_setted = False

            for event in pygame.event.get():
                self.handle_key_event(event)

            if self.game_state.is_play():
                if self.snake.is_dead():
                    self.game_over()
                else:
                    self.snake.moveForward()
                    self.board.draw(self.snake, self.game_state.score)
            elif self.game_state.is_over():
                sound_manager.pause_music()
                self.board.draw_final(self.game_state.score)

            pygame.display.update()
            self.fpsClock.tick(self.game_state.speed)

    def handle_key_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_f:
                self.board.toggle_screen()

            if self.game_state.is_over() and event.key == K_RETURN:
                print('Return press')
                self.restart()
            if event.key == K_SPACE:
                if self.game_state.is_play():
                    self.game_state.set_pause()
                    pygame.mixer.music.pause()
                elif self.game_state.is_pause():
                    self.game_state.set_play()
                    pygame.mixer.music.unpause()
            if self.game_state.is_play() and not self.new_direction_setted:
                direction = ''
                if event.key in (K_DOWN, K_s):
                    direction = 'down'
                elif event.key in (K_UP, K_w):
                    direction = 'up'
                elif event.key in (K_LEFT, K_a):
                    direction = 'left'
                elif event.key in (K_RIGHT, K_d):
                    direction = 'right'
                if self.snake.is_valid_direction(direction):
                    self.snake.set_direction(direction)
                    self.new_direction_setted = True
        if event.type == QUIT:
            #  pygame.quit()
            sys.exit()

    def game_over(self):
        self.game_state.set_over()
        sound_manager.play_fail_sound()
        self.board.draw_final(self.game_state.score)

    def restart(self):
        """重新开始游戏时，对游戏初始化"""
        self.game_state.reset()
        self.new_direction_setted = False  # 加锁，防止一个时间周期内改变两次方向，碰到蛇身第二节。
        self.snake = self.create_snake()  # 蛇对象
        sound_manager.replay_music()

    def create_snake(self):
        snake = Snake()
        def on_eat_food():
            self.game_state.add_score()
        snake.register_eat_food_listener(on_eat_food)
        return snake


if __name__ == '__main__':
    game = SnakeGame()
    game.start()
