"""
 Created by plough on 2019/7/4.
"""
import pygame

from constants import *
from libs.food_manager import food_manager


class GameBoard:

    def __init__(self):
        self.fontObj = pygame.font.Font('res/Kaiti_GB2312.ttf', 20)
        self.scoreFont = pygame.font.Font('res/Kaiti_GB2312.ttf', 32)
        self.full_screen = False  # 是否全屏
        self.screen = self.new_screen(SCREEN_SIZE)


    def draw(self, snake, score):
        self.screen.fill(GREEN)
        # 分割线
        pygame.draw.line(self.screen, RED, (502, 0), (502, 500), 3)
        prompt_text = self.fontObj.render('按 "空格键" 开始/暂停', True, WHITE)
        score_text = self.scoreFont.render('得分: {}'.format(score), True, WHITE)
        self.screen.blit(prompt_text, (550, 100))
        self.screen.blit(score_text, (570, 220))

        snake.draw_self(self.screen)
        food_manager.draw_fruit(self.screen, snake.body_list)


    def new_screen(self, size, full=False):
        if full:
            self.full_screen = True
            return pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.full_screen = False
        return pygame.display.set_mode(size)


    def draw_final(self, score):
        screen = self.screen
        pygame.draw.rect(screen, RED,
                (200, 120, 400, 300))
        pygame.draw.rect(screen, BLACK,
                (210, 130, 380, 280))
        over_text = self.scoreFont.render('GAME OVER!',
                True, WHITE)
        score_text = self.scoreFont.render('最终得分: {}'.format(score),
                True, WHITE)
        prompt_text = self.fontObj.render('按 "回车键" 再玩一次',
                True, WHITE)
        self.screen.blit(over_text, (300, 200))
        self.screen.blit(score_text, (300, 240))
        self.screen.blit(prompt_text, (300, 290))


    def toggle_screen(self):
        self.screen = self.new_screen(SCREEN_SIZE, full=not self.full_screen)