import pygame

from utils.images import web_texture
from utils.__init__ import rta_height, rta_dual, atr_height


class Web(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(web_texture, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.relposx = self.relposy = 0.0

    def summon(self):
        self.relposx = round(number=(round((atr_height(pygame.mouse.get_pos()[0]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.relposy = round(number=(round((atr_height(pygame.mouse.get_pos()[1]) - 0.05) / 0.1) * 0.1), ndigits=1)

    def update(self):
        self.rect.x, self.rect.y = rta_height(self.relposx), rta_height(self.relposy)

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (rta_dual(0.1, 0.1)))
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)
