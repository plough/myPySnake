"""
 Created by plough on 2019/7/4.
"""
import pygame

from constants import *
from food_manager import food_manager


class GameBoard:

    def __init__(self, gs, snake):
        self.fontObj = pygame.font.Font('res/Kaiti_GB2312.ttf', 20)
        self.scoreFont = pygame.font.Font('res/Kaiti_GB2312.ttf', 32)
        self.gs = gs
        self.snake = snake
        self.screen = self.new_screen(self.gs.screen_size)

    def update(self, gs, snake):
        self.gs = gs
        self.snake = snake

    def draw(self):
        self.screen.fill(GREEN)
        # 分割线
        pygame.draw.line(self.screen, RED, (502, 0), (502, 500), 3)
        promptText = self.fontObj.render('按 "空格键" 开始/暂停', True, WHITE)
        #  promptText2 = fontObj.render(u'开始/暂停', True, WHITE)
        scoreText = self.scoreFont.render('得分: ' + str(self.gs.score), True, WHITE)
        self.screen.blit(promptText, (550, 100))
        #  screen.blit(promptText2, (560, 120))
        self.screen.blit(scoreText, (570, 220))
        # drawSnake()
        self.snake.draw_self(self.screen)
        food_manager.draw_fruit(self.screen, self.snake)


    def new_screen(self, size, full=False):
        screen = None
        if full:
            self.gs.full_screen = True
            screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.gs.full_screen = False
            screen = pygame.display.set_mode(size)
        return screen

    def drawFinal(self):
        screen = self.screen
        pygame.draw.rect(screen, RED,
                (200, 120, 400, 300))
        pygame.draw.rect(screen, BLACK,
                (210, 130, 380, 280))
        over_text = self.scoreFont.render('GAME OVER!',
                True, WHITE)
        score_text = self.scoreFont.render(u'最终得分: ' + str(self.gs.score),
                True, WHITE)
        prompt_text = self.fontObj.render(u'按 "回车键" 再玩一次',
                True, WHITE)
        self.screen.blit(over_text, (300, 200))
        self.screen.blit(score_text, (300, 240))
        self.screen.blit(prompt_text, (300, 290))

    def toggle_screen(self):
        self.screen = self.new_screen(self.gs.screen_size, full=not self.gs.full_screen)