import pygame
from utils import relToAbsDual
from utils import renderText

class Button(pygame.sprite.Sprite):

    def __init__(self, relwidth, relheight, textcontent):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface(relToAbsDual(relwidth, relheight))
        self.surface.fill((255, 255, 255))
        self.text = textcontent
        self.textcolor = (0, 0, 0)
        self.textsize = 30
        self.rect = self.surface.get_rect()

    def draw(self, window):
        window.blit(self.surface, self.rect)
        renderText(window=window, text=self.text, position=self.rect.center, color=self.textcolor, size=self.textsize)
