"""
 Created by plough on 2019/7/4.
"""

# 处理与食物有关的事情
import random

import pygame

from constants import *


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

# 单例模式
food_manager = FoodManager()