"""
 Created by plough on 2019/7/5.
"""
from pygame.constants import *

from constants import *


class DirectionManager:
    directions = {
        'left': [-1, 0],
        'right': [1, 0],
        'up': [0, -1],
        'down': [0, 1]
    }

    @staticmethod
    def flip_direction(direction):
        if direction == 'left':
            return 'right'
        if direction == 'right':
            return 'left'
        if direction == 'up':
            return 'down'
        if direction == 'down':
            return 'up'


    @staticmethod
    def back_one_step(direction, x, y, min_x = 0, max_x = COLUMNS - 1, min_y = 0, max_y = ROWS - 1):
        direction = DirectionManager.flip_direction(direction)
        return DirectionManager.move_one_step(direction, x, y, min_x, max_x, min_y, max_y)


    @classmethod
    def move_one_step(cls, direction, x, y, min_x = 0, max_x = COLUMNS - 1, min_y = 0, max_y = ROWS - 1):
        step = DirectionManager.directions[direction]
        x += step[0]
        y += step[1]

        # 边界检查
        if x < min_x:
            x = max_x
        elif x > max_x:
            x = min_x
        if y < min_y:
            y = max_y
        elif y > max_y:
            y = min_y

        return x, y

    @staticmethod
    def get_direction_by_key(key):
        direction = ''
        if key in (K_DOWN, K_s):
            direction = 'down'
        elif key in (K_UP, K_w):
            direction = 'up'
        elif key in (K_LEFT, K_a):
            direction = 'left'
        elif key in (K_RIGHT, K_d):
            direction = 'right'
        return direction


    @staticmethod
    def is_valid_direction(current_direction, new_direction):
        if current_direction in ['up', 'down'] and new_direction in ['left', 'right']:
            return True
        elif current_direction in ['right', 'left'] and new_direction in ['up', 'down']:
            return True
        else:
            return False