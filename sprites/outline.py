import pygame
from utils import absToRel
from utils import relToAbs

outline_texture = pygame.image.load("textures/Outline.png")

def rel_pos(ind):
    return round(number=(round((absToRel(pygame.mouse.get_pos()[ind]) - 0.05) / 0.1) * 0.1), ndigits=1)

class Outline(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(outline_texture, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.relposx = 0.0
        self.relposy = 0.0

    def draw(self, window):
        self.relposx = rel_pos(0)
        self.relposy = rel_pos(1)
        self.rect.x = relToAbs(self.relposx)
        self.rect.y = relToAbs(self.relposy)
        window.blit(self.image, self.rect)
