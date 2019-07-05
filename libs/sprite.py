"""
 Created by plough on 2019/7/5.
"""

class BaseSprite:

    def draw_self(self, screen):
        pass

    def pos_list(self):
        """精灵占据的位置列表（新食物不能生成到该位置），如果不占位置，返回空列表"""
        pass