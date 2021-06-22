import pygame

from utils import relToAbs, relToAbsDual, absToRel

web_texture = pygame.image.load("textures/web.png")

class Web(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(web_texture, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.relposx = self.relposy = 0.0

    def summon(self):
        self.relposx = round(number=(round((absToRel(pygame.mouse.get_pos()[0]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.relposy = round(number=(round((absToRel(pygame.mouse.get_pos()[1]) - 0.05) / 0.1) * 0.1), ndigits=1)

    def update(self):
        self.rect.x, self.rect.y = relToAbs(self.relposx), relToAbs(self.relposy)

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (relToAbsDual(0.1, 0.1)))
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)
