"""
 Created by plough on 2019/7/4.
"""

# 游戏状态
from sound_manager import sound_manager
from constants import *


class GameState:
    def __init__(self):
        self.STATE = 'playing'
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