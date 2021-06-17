import pygame
import math
import random
from utils import relToAbsDual, absToRel

shuriken_texture = pygame.image.load("textures/shuriken.png")

class Shuriken(pygame.sprite.Sprite):
    def __init__(self, relpos, radians, velocity=6, explosion=False):
        pygame.sprite.Sprite.__init__(self)
        self.relpos, self.radians, self.velocity = relpos, radians, velocity
        self.reldx = absToRel(math.cos(self.radians))
        self.reldy = absToRel(math.sin(self.radians))
        self.reldxtotal, self.reldytotal = 0, 0
        self.rotangle = 0
        self.resize()

    def resize(self):
        self.original_image = pygame.transform.scale(shuriken_texture, relToAbsDual(0.1, 0.1))
        self.image = self.original_image

    def update(self, delta_time):
        self.image = pygame.transform.rotate(self.original_image, self.rotangle)
        self.rotangle += 4
        if self.rotangle > 360:
            self.rotangle = 0
        self.rect = self.image.get_rect()
        self.rect.center = relToAbsDual(self.relpos[0] + self.reldxtotal, self.relpos[1] + self.reldytotal)
        self.reldxtotal += self.reldx * self.velocity * (50 * delta_time)
        self.reldytotal += self.reldy * self.velocity * (50 * delta_time)

    def draw(self, window):
        window.blit(self.image, self.rect)
