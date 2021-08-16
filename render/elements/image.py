import pygame
from utils import rta_dual, set_anchor_point

class Image(pygame.sprite.Sprite):
    def __init__(self, relpos, anchor="center", image=None):
        pygame.sprite.Sprite.__init__(self)
        if image is not None:
            self.image = image
        self.rect = self.image.get_rect()
        self.anchor = anchor
        self.relpos = relpos
        pos = rta_dual(self.relpos[0], self.relpos[1])
        set_anchor_point(self.rect, pos, self.anchor)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
