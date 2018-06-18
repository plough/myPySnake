#!/usr/bin/env python3
# encoding: utf-8
import pygame
from constants import *


class Snake:
    def __init__(self, length = 3, headPos = [5,3], direction = 'right'):
        """
        默认坐标系为25×25
        """
        self.length = length
        self.headPos = headPos
        self.direction = direction

        self.bodyList = [tuple(headPos)] # 存储蛇身所在坐标
        tempX = headPos[0]
        tempY = headPos[1]
        for i in range(length - 1):
            if direction == 'right':
                tempX -= 1
            elif direction == 'left':
                tempX += 1
            elif direction == 'up':
                tempY -= 1
            else:
                tempY += 1
            self.bodyList.append((tempX, tempY))

    # 传入表示方向的字符串
    def changeDirection(self, newDirection):
        if self.isValidDirection(newDirection):
            self.direction = newDirection
        else:
            raise Exception('传入了错误的方向值')

    def isValidDirection(self, newDirection):
        if self.direction in ['up', 'down'] and newDirection in ['left', 'right']:
            return True
        elif self.direction in ['right', 'left'] and newDirection in ['up', 'down']:
            return True
        else:
            return False

    # 前进一步
    def moveForward(self, eatFood=False):
        if self.direction == 'up':
            if self.headPos[1] == 0:
                self.headPos[1] = 24
            else:
                self.headPos[1] -= 1
        elif self.direction == 'down':
            if self.headPos[1] == 24:
                self.headPos[1] = 0
            else:
                self.headPos[1] += 1
        elif self.direction == 'right':
            if self.headPos[0] == 24:
                self.headPos[0] = 0
            else:
                self.headPos[0] += 1
        else:
            if self.headPos[0] == 0:
                self.headPos[0] = 24
            else:
                self.headPos[0] -= 1
        self.bodyList.insert(0, tuple(self.headPos))
        if not eatFood:
            self.bodyList.pop()
        else:
            self.length += 1

    def draw_self(self, screen):
        for pos in self.bodyList:
            pygame.draw.rect(screen, WHITE, \
                    (pos[0]*USIZE, pos[1]*USIZE, USIZE, USIZE))
