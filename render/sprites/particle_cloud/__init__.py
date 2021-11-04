import pygame

from render.sprites.particle_cloud import particle
from utils import globs, get_outline_mask

class ParticleCloud(pygame.sprite.Sprite):
    def __init__(self, center, radius, particlesize, color, density, velocity, rotation=False, distribution=0.3, damagecooldown=0.5, damage=0,
                 colorvariation=50, priority=2, no_debug=False, spawnradius=0, spawnregion=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.priority = priority
        self.dc = 0
        self.dc_max = damagecooldown
        self.damage = damage
        self.no_debug = no_debug
        self.center = list(center)
        self.radius = radius
        self.spawnradius = spawnradius
        self.spawnregion = spawnregion
        if spawnradius != 0:
            self.spawnregion = (spawnradius, spawnradius)
        self.velocity = velocity
        self.particlesize = particlesize
        self.distribution = distribution
        self.color = color
        self.colorvariation = colorvariation
        self.density = density
        self.rotation = rotation
        self.particles = []
        for i in range(self.density):
            self.particles.append(particle.Particle(pos=self.center, size=self.particlesize, spawnregion=self.spawnregion,
                                                    color=self.color, maxdistance=self.radius, velocity=self.velocity,
                                                    distribution=self.distribution, colorvariation=self.colorvariation,
                                                    rotation=self.rotation))
        self.rect = pygame.Rect(self.center[0] - self.radius, self.center[1] - self.radius,
                                self.radius * 2, self.radius * 2)
        self.rect.center = self.center[0], self.center[1]

    def update(self, delta_time, entitys, player, particles, blocks, projectiles, melee):
        for i in self.particles:
            i.update(delta_time=delta_time, particles=self.particles)
        if len(self.particles) == 0:
            particles.remove(self)

        if self.damage > 0:
            self.dc -= delta_time
            if self.dc < 0:
                for i in entitys:
                    if self.rect.colliderect(i.hitbox):
                        i.damage(damage=self.damage, particles=particles)
                        self.dc = self.dc_max
                if self.rect.colliderect(player.hitbox):
                    player.damage(damage=self.damage, particles=particles)

    def draw(self, surface):
        for i in self.particles:
            i.draw(surface=surface)
        if globs.soft_debug and not self.no_debug:
            surf = pygame.Surface((self.rect.width, self.rect.height))
            surf.fill((0, 0, 0))
            outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
            surface.blit(outlinesurf, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
