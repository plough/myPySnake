"""
 Created by plough on 2019/7/4.
"""
import pygame

from constants import *
from libs.food_manager import food_manager


class GameBoard:

    def __init__(self, game_state):
        self.fontObj = pygame.font.Font('res/Kaiti_GB2312.ttf', 20)
        self.scoreFont = pygame.font.Font('res/Kaiti_GB2312.ttf', 32)
        self.full_screen = False  # 是否全屏
        self.screen = self._new_screen(SCREEN_SIZE)
        self.sprites = []  # 精灵列表
        self.game_state = game_state


    def add_sprite(self, sprite):
        self.sprites.append(sprite)


    def draw(self):
        self._draw_board()
        if self.game_state.is_over():
            self._draw_over_tip()
        pygame.display.update()


    def toggle_screen(self):
        self.screen = self._new_screen(SCREEN_SIZE, full=not self.full_screen)


    def _draw_board(self):
        self.screen.fill(GREEN)
        # 分割线
        pygame.draw.line(self.screen, RED, (502, 0), (502, 500), 3)
        prompt_text = self.fontObj.render('按 "空格键" 开始/暂停', True, WHITE)
        score_text = self.scoreFont.render('得分: {}'.format(self._get_score()), True, WHITE)
        self.screen.blit(prompt_text, (550, 100))
        self.screen.blit(score_text, (570, 220))

        invalid_pos_list = []
        for sprite in self.sprites:
            sprite.draw_self(self.screen)
            invalid_pos_list.extend(sprite.pos_list())

        food_manager.draw_fruit(self.screen, invalid_pos_list)


    def _new_screen(self, size, full=False):
        if full:
            self.full_screen = True
            return pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.full_screen = False
        return pygame.display.set_mode(size)


    def _draw_over_tip(self):
        pygame.draw.rect(self.screen, RED,
                         (200, 120, 400, 300))
        pygame.draw.rect(self.screen, BLACK,
                         (210, 130, 380, 280))
        over_text = self.scoreFont.render('GAME OVER!',
                                          True, WHITE)
        score_text = self.scoreFont.render('最终得分: {}'.format(self._get_score()),
                                           True, WHITE)
        prompt_text = self.fontObj.render('按 "回车键" 再玩一次',
                                          True, WHITE)
        self.screen.blit(over_text, (300, 200))
        self.screen.blit(score_text, (300, 240))
        self.screen.blit(prompt_text, (300, 290))


    def _get_score(self):
        return self.game_state.score