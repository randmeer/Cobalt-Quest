import pygame

from render.sprites import particle


class ParticleCloud(pygame.sprite.Sprite):
    def __init__(self, center, radius, particlesize, color, density, velocity, distribution=0.3,
                 colorvariation=50):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.particlesize = particlesize
        self.distribution = distribution
        self.color = color
        self.colorvariation = colorvariation
        self.density = density
        self.particles = []
        for i in range(self.density):
            particlesprite = particle.Particle(pos=self.center, size=self.particlesize,
                                               color=self.color, maxdistance=self.radius, velocity=self.velocity,
                                               distribution=self.distribution, colorvariation=self.colorvariation)
            self.particles.append(particlesprite)
        self.reposition(center=center)

    def update(self, delta_time):
        for i in self.particles:
            i.update(delta_time=delta_time)

    def draw(self, surface):
        for i in self.particles:
            i.draw(surface=surface)

    def reposition(self, center):
        self.center = center
        for i in self.particles:
            i.pos = center
        self.rect = pygame.Rect(self.center[0] - self.radius, self.center[1] - self.radius,
                                self.radius * 2, self.radius * 2)
        self.rect.center = self.center[0], self.center[1]

    def reset(self):
        for i in self.particles:
            i.dxtotal, i.dytotal = 0, 0
            i.generate_randoms()
            i.dead = False
