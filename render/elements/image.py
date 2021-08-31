import pygame
from utils import rta_dual, set_anchor_point, mp_screen

class Image(pygame.sprite.Sprite):
    def __init__(self, relpos, image, anchor="center", tags=None, visible=True, h_event=False, h_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.visible = visible
        self.hoverevent = h_event
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
        self.h_image = h_image
        self.surface = self.image
        self.rect = self.image.get_rect()
        self.anchor = anchor
        self.relpos = relpos
        pos = rta_dual(self.relpos[0], self.relpos[1])
        set_anchor_point(self.rect, pos, self.anchor)

    def set_visible(self, visible):
        self.visible = visible

    def update(self):
        if self.hoverevent and self.rect.collidepoint(mp_screen()):
            self.surface = self.h_image
        else:
            self.surface = self.image

    def draw(self, surface):
        if self.visible:
            surface.blit(self.surface, self.rect)
