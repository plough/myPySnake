#!/usr/bin/env python3
# encoding: utf-8
import pygame

from constants import *
from libs.food_manager import food_manager
from libs.sound_manager import sound_manager


class Snake:
    INIT_LENGTH = 3
    INIT_HEAD_POS = (5, 3)
    INIT_DIRECTION = 'right'
    
    def __init__(self):
        # 监听者模式
        self.eat_food_listeners = []

        """
        默认坐标系为25×25
        """
        self.length = self.INIT_LENGTH
        self.head_pos = list(self.INIT_HEAD_POS)
        self.direction = self.INIT_DIRECTION
        self.body_list = self.init_body_list()
        
            
    def init_body_list(self):
        body_list = [tuple(self.head_pos)]  # 存储蛇身所在坐标
        x = self.head_pos[0]
        y = self.head_pos[1]
        for i in range(self.length - 1):
            if self.direction == 'right':
                x -= 1
            elif self.direction == 'left':
                x += 1
            elif self.direction == 'up':
                y -= 1
            else:
                y += 1
            body_list.append((x, y))
        return body_list
            

    def register_eat_food_listener(self, listener):
        self.eat_food_listeners.append(listener)

    # 传入表示方向的字符串
    def set_direction(self, new_direction):
        if self.is_valid_direction(new_direction):
            self.direction = new_direction
        else:
            raise Exception('传入了错误的方向值')

    def is_valid_direction(self, new_direction):
        if self.direction in ['up', 'down'] and new_direction in ['left', 'right']:
            return True
        elif self.direction in ['right', 'left'] and new_direction in ['up', 'down']:
            return True
        else:
            return False

    # 前进一步
    def moveForward(self):
        if self.meet_food():
            self.eat_food()
        else:
            self.body_list.pop()

        if self.direction == 'up':
            if self.head_pos[1] == 0:
                self.head_pos[1] = 24
            else:
                self.head_pos[1] -= 1
        elif self.direction == 'down':
            if self.head_pos[1] == 24:
                self.head_pos[1] = 0
            else:
                self.head_pos[1] += 1
        elif self.direction == 'right':
            if self.head_pos[0] == 24:
                self.head_pos[0] = 0
            else:
                self.head_pos[0] += 1
        else:
            if self.head_pos[0] == 0:
                self.head_pos[0] = 24
            else:
                self.head_pos[0] -= 1
        self.body_list.insert(0, tuple(self.head_pos))

    def meet_food(self):
        return tuple(self.head_pos) == food_manager.fruit_pos

    def eat_food(self):
        food_manager.hide_fruit()
        sound_manager.play_eat_sound()
        for listener in self.eat_food_listeners:
            listener()
        # self.gs.add_score()


    def is_dead(self):
        return tuple(self.head_pos) in self.body_list[1:]


    def draw_self(self, screen):
        for pos in self.body_list:
            pygame.draw.rect(screen, WHITE,
                    (pos[0]*USIZE, pos[1]*USIZE, USIZE, USIZE))
