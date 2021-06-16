import pygame
from sprites import particle
from utils import absToRel, relToAbsDual, relToAbs

outline_texture = pygame.image.load("textures/outline.png")

class ParticleCloud(pygame.sprite.Sprite):
    def __init__(self, relcenter, relradius, relparticlesize, color, density):
        pygame.sprite.Sprite.__init__(self)
        self.relcenter = relcenter
        self.relradius = relradius
        self.relparticlesize = relparticlesize
        self.color = color
        self.density = density
        self.particles = []
        for i in range(self.density):
            particlesprite = particle.Particle(relposition=self.relcenter, relsize=self.relparticlesize, color=self.color)
            self.particles.append(particlesprite)
        self.run = False
        self.timer = 1

    def update(self, window, delta_time):
        if self.run:
            print(self.relcenter)
            for i in self.particles:
                i.update()
                i.draw(surface=window)
            self.rect = pygame.Rect(relToAbs(self.relcenter[0]-self.relradius), relToAbs(self.relcenter[1]-self.relradius), relToAbs(self.relradius*2), relToAbs(self.relradius*2))
            self.rect.center = relToAbsDual(self.relcenter[0], self.relcenter[1])
            self.timer -= 1 * delta_time
            if self.timer < 0:
                self.run = False

    def reposition(self, relcenter):
        for i in self.particles:
            i.relpos = relcenter
