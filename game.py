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
from libs.direction_manager import DirectionManager
from libs.lock import SimpleLock
from libs.sound_manager import sound_manager


class SnakeGame:

    def __init__(self):
        pygame.init()

        self.game_state = GameState()  # 当前游戏状态
        self.snake = self._create_snake()  # 蛇

        self.board = GameBoard(self.game_state)  # 画板
        self.board.add_sprite(self.snake)

        self.fps_clock = pygame.time.Clock()  # 控制帧率
        self.direction_lock = SimpleLock()  # 方向锁，防止在一个时钟周期内，连续改变方向，导致撞到蛇身第二节

        pygame.display.set_caption(TITLE)


    def start(self):
        self.board.draw()

        # 游戏主循环
        while True:
            self.direction_lock.unlock()

            for event in pygame.event.get():
                self.handle_key_event(event)

            if self.game_state.is_play():
                if self.snake.is_dead():
                    self.game_state.set_over()
                else:
                    self.snake.move_forward()

            self.board.draw()

            self.fps_clock.tick(self.game_state.speed)


    def handle_key_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

            if event.key == K_f:
                self.board.toggle_screen()

            elif self.game_state.is_over() and event.key == K_RETURN:
                self.restart()

            elif event.key == K_SPACE:
                self.game_state.toggle_state()

            elif self.game_state.is_play() and not self.direction_lock.is_locked():
                direction = DirectionManager.get_direction_by_key(event.key)
                if self.snake.is_valid_direction(direction):
                    self.snake.set_direction(direction)
                    self.direction_lock.lock()

        if event.type == QUIT:
            sys.exit()


    def restart(self):
        """重新开始游戏时，对游戏初始化"""
        self.game_state.reset()
        self.direction_lock.unlock()
        self.snake.reset()
        sound_manager.replay_music()


    def _create_snake(self):
        snake = Snake()
        def on_eat_food():
            self.game_state.add_score()
        snake.register_eat_food_listener(on_eat_food)
        return snake


if __name__ == '__main__':
    game = SnakeGame()
    game.start()
