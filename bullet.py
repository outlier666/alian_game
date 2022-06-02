# 作者：大大大帅逼
# 码龄：一年
# 开发时间：2022/4/2111:36
# 开发人员：Admin
# 文件名称：bullet
# 开发工具：PyCharm


import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midright

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x = self.x
        # self.y -= self.settings.bullet_speed
        # self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)