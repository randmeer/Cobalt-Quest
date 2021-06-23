import math

import pygame

from utils.images import shuriken_texture
from sprites import particle_cloud
from utils.__init__ import relToAbsDual, absToRel, absToRelDual


class Shuriken(pygame.sprite.Sprite):
    def __init__(self, relpos, radians, velocity=6):
        pygame.sprite.Sprite.__init__(self)
        self.relpos, self.radians, self.velocity = relpos, radians, velocity
        self.reldx = absToRel(math.cos(self.radians))
        self.reldy = absToRel(math.sin(self.radians))
        self.reldxtotal, self.reldytotal = 0, 0
        self.rotangle = 0
        self.resize()
        self.trigger_explosion, self.exploding, self.dead = False, False, False
        self.explosiontimer = 1

    def resize(self):
        self.original_image = pygame.transform.scale(shuriken_texture, relToAbsDual(0.1, 0.1))
        self.image = self.original_image

    def update(self, delta_time, window):
        if self.trigger_explosion:
            self.dead = True
            self.smoke.update(window=window, delta_time=delta_time)
            self.fire.update(window=window, delta_time=delta_time)
            self.sparks.update(window=window, delta_time=delta_time)
            self.explosiontimer -= delta_time
            if self.explosiontimer < 0:
                self.exploding = False
            return
        self.image = pygame.transform.rotate(self.original_image, self.rotangle)
        self.rotangle += 4
        if self.rotangle > 360:
            self.rotangle = 0
        self.rect = self.image.get_rect()
        self.rect.center = relToAbsDual(self.relpos[0] + self.reldxtotal, self.relpos[1] + self.reldytotal)
        self.reldxtotal += self.reldx * self.velocity * 50 * delta_time
        self.reldytotal += self.reldy * self.velocity * 50 * delta_time

        self.draw(window=window)

    def explode(self):
        if self.dead: return
        self.smoke = particle_cloud.ParticleCloud(relcenter=absToRelDual(self.rect.centerx, self.rect.centery),
                                                  relradius=0.09,
                                                  relparticlesize=0.07, color=(70, 70, 70), density=10, relvelocity=1.5,
                                                  distribution=0.7, colorvariation=5)
        self.fire = particle_cloud.ParticleCloud(relcenter=absToRelDual(self.rect.centerx, self.rect.centery),
                                                 relradius=0.08,
                                                 relparticlesize=0.04, color=(200, 70, 0), density=20, relvelocity=1.2,
                                                 distribution=0.5, colorvariation=30)
        self.sparks = particle_cloud.ParticleCloud(relcenter=absToRelDual(self.rect.centerx, self.rect.centery),
                                                   relradius=0.1,
                                                   relparticlesize=0.01, color=(200, 100, 0), density=20, relvelocity=2,
                                                   distribution=0.5, colorvariation=5)
        self.trigger_explosion = True

    def draw(self, window):
        window.blit(self.image, self.rect)
