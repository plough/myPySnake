# 管理声音的类
import os

import pygame

class SoundManager:
    music_path = os.path.join('res', 'background.mp3')

    def __init__(self):
        self._init_music()
        self.sound_eat = self._load_sound('eat.ogg')
        self.sound_fail = self._load_sound('gameover.ogg')
        self.sound_cheer = self._load_sound('cheer.ogg')

    # 背景音乐
    @classmethod
    def _init_music(cls):
        pygame.mixer.init()
        pygame.mixer.music.load(cls.music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    @staticmethod
    def _load_sound(file_name):
        return pygame.mixer.Sound(os.path.join('res', file_name))

    @staticmethod
    def replay_music():
        pygame.mixer.music.rewind()
        pygame.mixer.music.unpause()

    @staticmethod
    def pause_music():
        pygame.mixer.music.pause()

    @staticmethod
    def resume_music():
        pygame.mixer.music.unpause()

    def play_eat_sound(self):
        self.sound_eat.play()

    def play_fail_sound(self):
        self.sound_fail.play()

    def play_cheer_sound(self):
        self.sound_cheer.play()

# 单例模式
sound_manager = SoundManager()