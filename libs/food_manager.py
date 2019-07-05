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

    def draw_fruit(self, screen, invalid_positions):
        """生成并绘制食物"""
        if not self.fruit_showing:
            self.fruit_pos = self.random_pos(invalid_positions)

        pygame.draw.rect(screen, RED,
                (self.fruit_pos[0]*USIZE, self.fruit_pos[1]*USIZE, USIZE, USIZE))

        self.fruit_showing = True

    @staticmethod
    def random_pos(invalid_positions):
        pos = None
        while not pos or pos in invalid_positions:
            x = random.randint(0, ROWS - 1)
            y = random.randint(0, ROWS - 1)
            pos = (x, y)
        return pos

    def hide_fruit(self):
        self.fruit_showing = False

# 单例模式
food_manager = FoodManager()