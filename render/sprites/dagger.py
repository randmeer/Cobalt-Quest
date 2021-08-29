import pygame
from utils import angle_deg, conv_deg_rad, sin, cos
from utils.images import Texture

class Dagger(pygame.sprite.Sprite):
    def __init__(self, mousepos, playerpos):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 2
        self.dead = False
        self.mp = mousepos
        self.pp = playerpos
        self.swing_deg = angle_deg(self.pp, self.mp)
        self.swing_rad = conv_deg_rad(self.swing_deg)
        dx = sin(self.swing_rad)
        dy = cos(self.swing_rad)
        self.swing_target = (self.pp[0] + dx * 20, self.pp[1] - dy * 20)
        self.swing_image = Texture("resources/textures/swing.png", single_run=True, set_height=16)
        self.image = pygame.transform.rotate(self.swing_image.get(), -self.swing_deg)
        self.rect = self.image.get_rect()
        self.rect.center = self.swing_target

    def update(self, delta_time, blocks, entitys, particles):
        if self.dead: return
        if self.swing_image.get() == False:
            self.dead = True
        else:
            self.image = pygame.transform.rotate(self.swing_image.get(), -self.swing_deg)

    def draw(self, surface):
        if self.dead: return
        surface.blit(self.image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
