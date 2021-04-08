import pygame, random
from data import globals


class Web(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("data/textures/web.png"), (50, 50))
        self.rect = self.image.get_rect()

    def summon(self):
        self.rect.x = round((pygame.mouse.get_pos()[0] - 25) / 50) * 50
        self.rect.y = round((pygame.mouse.get_pos()[1] - 25) / 50) * 50

    def draw(self, window):
        window.blit(self.image, self.rect)
