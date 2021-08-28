import math
import pygame

from utils.images import shuriken_tx
from render.sprites import particle_cloud


class Shuriken(pygame.sprite.Sprite):
    def __init__(self, pos, radians, velocity=3, exploding=False):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = shuriken_tx
        self.image = self.original_image
        self.pos, self.radians, self.velocity = pos, radians, velocity
        self.dx = math.sin(self.radians)
        self.dy = math.cos(self.radians)
        self.dxtotal, self.dytotal = 0, 0
        self.rotangle = 0
        self.dead = False
        self.explosiontimer = 1
        self.update(0, blocks=[], particles=[])

    def update(self, delta_time, blocks, particles):
        if self.dead: return
        for i in blocks:
            if self.rect.colliderect(i.rect):
                self.explode(particles=particles)
        self.image = pygame.transform.rotate(self.original_image, self.rotangle)
        self.rotangle += 4
        if self.rotangle > 360:
            self.rotangle = 0
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0] + self.dxtotal, self.pos[1] + self.dytotal)
        self.dxtotal += self.dx * self.velocity * 50 * delta_time
        self.dytotal -= self.dy * self.velocity * 50 * delta_time

    def explode(self, particles):
        if self.dead: return
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=20,
                                                 particlesize=(7, 7), color=(70, 70, 70), density=2, velocity=30,
                                                 distribution=0.8, colorvariation=5))
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=15,
                                                particlesize=(3, 3), color=(200, 70, 0), density=3, velocity=40,
                                                distribution=0.8, colorvariation=30))
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=25,
                                                  particlesize=(1, 1), color=(200, 100, 0), density=3, velocity=50,
                                                  distribution=0.7, colorvariation=5))
        #particles.append(particle_cloud.ParticleCloud(center=self.rect.center, radius=40, particlesize=(10, 10),
        #                                              color=(40, 20, 20), density=10, velocity=100, colorvariation=10))
        self.dead = True

    def draw(self, surface):
        if self.dead: return
        surface.blit(self.image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
        # if self.exploding:
            # self.smoke.draw(surface=surface)
            # self.fire.draw(surface=surface)
            # self.sparks.draw(surface=surface)
            # self.test.draw(surface=surface)
