import math
import random
import pygame
from utils import absToRel, relToAbsDual, relToAbs

outline_texture = pygame.image.load("textures/outline.png")

class Particle(pygame.sprite.Sprite):
    def __init__(self, relposition, relsize, color, relmaxdistance, relvelocity, distribution, colorvariation):
        pygame.sprite.Sprite.__init__(self)
        self.relpos = relposition
        self.relsize = relsize
        self.originalcolor = color
        self.colorvariation = colorvariation
        self.relmaxdist = relmaxdistance
        self.distribution = distribution
        self.originalrelvelocity = relvelocity
        self.dead = False
        self.generate_randoms()

        self.update(0)
        self.relborderdist = 0

    def generate_randoms(self):
        self.color = [self.originalcolor[0] + random.randint(-self.colorvariation, self.colorvariation), self.originalcolor[1] + random.randint(-self.colorvariation, self.colorvariation),
                      self.originalcolor[2] + random.randint(-self.colorvariation, self.colorvariation)]
        for i in range(3):
            if self.color[i] < 0:
                self.color[i] = 0
            if self.color[i] > 255:
                self.color[i] = 255
        self.rotangle = random.randint(0, 90)
        self.radians = random.uniform(0, 2*math.pi)
        self.velocity = random.uniform(1-(self.distribution), 1+(self.distribution)) * self.originalrelvelocity
        self.reldx = absToRel(math.cos(self.radians))
        self.reldy = absToRel(math.sin(self.radians))
        self.reldxtotal, self.reldytotal = 0, 0

    def update(self, delta_time):
        if self.dead: return
        self.image = pygame.Surface(relToAbsDual(self.relsize, self.relsize))
        self.image.fill(self.color)
        self.image = pygame.transform.rotate(self.image, self.rotangle)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = relToAbsDual(self.relpos[0] + self.reldxtotal, self.relpos[1] + self.reldytotal)
        if self.rotangle > 90:
            self.rotangle = 0
        else:
            self.rotangle += 1
        self.reldxtotal += self.reldx * self.velocity * 50 * delta_time
        self.reldytotal += self.reldy * self.velocity * 50 * delta_time
        self.relborderdist = self.relmaxdist - math.hypot(absToRel(self.rect.centerx) - self.relpos[0], absToRel(self.rect.centery) - self.relpos[1])
        if self.relborderdist < 0:
            self.dead = True

    def draw(self, surface):
        if self.dead: return
        surface.blit(self.image, self.rect)
