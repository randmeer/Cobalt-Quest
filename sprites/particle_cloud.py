import pygame
from sprites import particle
from utils import absToRel, relToAbsDual, relToAbs

outline_texture = pygame.image.load("textures/outline.png")

class ParticleCloud(pygame.sprite.Sprite):
    def __init__(self, relcenter, relradius, relparticlesize, color, density, relvelocity, distribution=0.3):
        pygame.sprite.Sprite.__init__(self)
        self.relcenter = relcenter
        self.relradius = relradius
        self.relv = relvelocity
        self.relparticlesize = relparticlesize
        self.distribution = distribution
        self.color = color
        self.density = density
        self.particles = []
        for i in range(self.density):
            particlesprite = particle.Particle(relposition=self.relcenter, relsize=self.relparticlesize,
                                               color=self.color, relmaxdistance=self.relradius, relvelocity=self.relv, distribution=self.distribution)
            self.particles.append(particlesprite)

    def update(self, window, delta_time):
        for i in self.particles:
            i.update(delta_time=delta_time)
            i.draw(surface=window)
        self.rect = pygame.Rect(relToAbs(self.relcenter[0] - self.relradius),
                                relToAbs(self.relcenter[1] - self.relradius), relToAbs(self.relradius * 2),
                                relToAbs(self.relradius * 2))
        self.rect.center = relToAbsDual(self.relcenter[0], self.relcenter[1])

    def reposition(self, relcenter):
        self.relcenter = relcenter
        for i in self.particles:
            i.relpos = relcenter

    def reset(self):
        for i in self.particles:
            i.reldxtotal, i.reldytotal = 0, 0
            i.generate_randoms()
            i.dead = False
