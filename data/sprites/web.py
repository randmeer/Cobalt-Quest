import pygame, random
from data import globals
from data.utils import relToAbsHeight
from data.utils import absToRelHeight


class Web(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(pygame.image.load("data/textures/web.png"), (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.relposx = 0.0
        self.relposy = 0.0

    def summon(self):
        self.rect.x = round((pygame.mouse.get_pos()[0] - 25) / 50) * 50
        self.rect.y = round((pygame.mouse.get_pos()[1] - 25) / 50) * 50

        self.relposx = round(number=(round((absToRelHeight(pygame.mouse.get_pos()[0]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.relposy = round(number=(round((absToRelHeight(pygame.mouse.get_pos()[1]) - 0.05) / 0.1) * 0.1), ndigits=1)

    def update(self):
        self.rect.x = relToAbsHeight(self.relposx)
        self.rect.y = relToAbsHeight(self.relposy)

    def draw(self, window):
        window.blit(self.image, self.rect)
