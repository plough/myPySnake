"""
 Created by plough on 2019/7/4.
"""

from constants import *
# 游戏状态
from libs.sound_manager import sound_manager


class GameState:
    # 三种状态：playing, pausing, over

    def __init__(self):
        self.state = 'playing'
        self.score = 0  # 得分
        self.speed = INITSPEED  # FPS，游戏速度

    def reset(self):
        self.set_play()
        self.score = 0  # 得分
        self.speed = INITSPEED  # FPS，游戏速度

    def add_score(self):
        self.score += 1
        if self.speed < 15:
            self.speed *= 1.1
        if self.score in (30, 50, 65, 75) or\
            (self.score > 75 and (self.score - 80) % 5 == 0):
            sound_manager.play_cheer_sound()

    def set_play(self):
        self.state = 'playing'

    def set_pause(self):
        self.state = 'pausing'

    def set_over(self):
        self.state = 'over'
        sound_manager.play_fail_sound()
        sound_manager.pause_music()

    def is_play(self):
        return self.state == 'playing'

    def is_pause(self):
        return self.state == 'pausing'

    def is_over(self):
        return self.state == 'over'

    def toggle_state(self):
        if self.is_play():
            self.set_pause()
            sound_manager.pause_music()
        elif self.is_pause():
            self.set_play()
            sound_manager.resume_music()