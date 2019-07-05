#!/usr/bin/env python3
# encoding: utf-8
import pygame

from constants import *
from libs.direction_manager import DirectionManager
from libs.food_manager import food_manager
from libs.sound_manager import sound_manager
from libs.sprite import BaseSprite


class Snake(BaseSprite):

    INIT_LENGTH = 3
    INIT_HEAD_POS = (5, 3)
    INIT_DIRECTION = 'right'


    def __init__(self):
        # 监听者模式
        self.eat_food_listeners = []

        self.direction = self.INIT_DIRECTION
        self.body_list = self.init_body_list()  # 存储蛇身所在坐标


    def reset(self):
        self.direction = self.INIT_DIRECTION
        self.body_list = self.init_body_list()


    def init_body_list(self):
        x, y = self.INIT_HEAD_POS
        body_list = []
        for i in range(self.INIT_LENGTH):
            body_list.append((x, y))
            x, y = DirectionManager.back_one_step(self.direction, x, y)
        return body_list


    @property
    def head_pos(self):
        return self.body_list[0]


    def register_eat_food_listener(self, listener):
        self.eat_food_listeners.append(listener)


    # 传入表示方向的字符串
    def set_direction(self, new_direction):
        if self.is_valid_direction(new_direction):
            self.direction = new_direction
        else:
            raise Exception('传入了错误的方向值')


    def is_valid_direction(self, new_direction):
        return DirectionManager.is_valid_direction(self.direction, new_direction)


    # 前进一步
    def move_forward(self):
        if self.meet_food():
            self.eat_food()
        else:
            self.body_list.pop()

        x, y = self.head_pos
        x, y = DirectionManager.move_one_step(self.direction, x, y)

        self.body_list.insert(0, (x, y))


    def meet_food(self):
        return self.head_pos == food_manager.fruit_pos


    def eat_food(self):
        food_manager.hide_fruit()
        sound_manager.play_eat_sound()
        for listener in self.eat_food_listeners:
            listener()


    def is_dead(self):
        return self.head_pos in self.body_list[1:]


    def draw_self(self, screen):
        for pos in self.body_list:
            pygame.draw.rect(screen, WHITE,
                    (pos[0]*USIZE, pos[1]*USIZE, USIZE, USIZE))


    def pos_list(self):
        return self.body_list