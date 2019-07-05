# 管理声音的类
import os

import pygame

class SoundManager:
    def __init__(self):
        self._init_music()
        self.sound_eat = self._loadSound('eat.ogg')
        self.sound_fail = self._loadSound('gameover.ogg')
        self.sound_cheer = self._loadSound('cheer.ogg')

    # 背景音乐
    def _init_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('res', 'background.mp3'))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def _loadSound(self, fname):
        return pygame.mixer.Sound(os.path.join('res', fname))

    def replay_music(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.unpause()

    def pause_music(self):
        pygame.mixer.music.pause()

    def play_eat_sound(self):
        self.sound_eat.play()

    def play_fail_sound(self):
        self.sound_fail.play()

    def play_cheer_sound(self):
        self.sound_cheer.play()

# 单例模式
sound_manager = SoundManager()