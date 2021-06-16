import math
import random

import pygame
from utils import absToRel, relToAbsDual, relToAbs

outline_texture = pygame.image.load("textures/outline.png")

class Particle(pygame.sprite.Sprite):
    def __init__(self, relposition, relsize, color):
        pygame.sprite.Sprite.__init__(self)
        self.relpos = relposition
        self.relsize = relsize
        self.color = (color[0] + random.randint(-4, 4), color[1] + random.randint(-4, 4), color[2] + random.randint(-4, 4))
        self.rotangle = random.randint(0, 90)
        self.radians = random.uniform(0, math.pi)
        self.dx, self.dy = 0, 0
        self.update()

    def update(self):
        self.image = pygame.Surface(relToAbsDual(self.relsize, self.relsize))
        self.image.fill(self.color)
        self.image.convert_alpha()
        self.image = pygame.transform.rotate(self.image, self.rotangle)
        self.rect = self.image.get_rect()
        self.rect.center = relToAbsDual(self.relpos[0], self.relpos[1])
        if self.rotangle > 90:
            self.rotangle = 0
        else:
            self.rotangle += 1
        self.dx = math.cos(self.radians)
        self.dy = math.sin(self.radians)


        #print(self.relpos[0])
        #print(self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
