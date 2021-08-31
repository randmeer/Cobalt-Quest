import math
import pygame

from utils import play_sound, globs, get_outline_mask
from utils.images import item_tx
from render.sprites import particle_cloud


class Shuriken(pygame.sprite.Sprite):
    def __init__(self, pos, radians, velocity=3, exploding=False):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 2
        self.original_image = item_tx["shuriken"]
        self.image = self.original_image
        self.pos, self.radians, self.velocity = pos, radians, velocity
        self.dx = math.sin(self.radians)
        self.dy = math.cos(self.radians)
        self.dxtotal, self.dytotal = 0, 0
        self.rotangle = 0
        self.dead = False
        self.collided = False
        self.exploding = exploding
        self.despawn_seconds = 4
        self.hitbox = pygame.Rect((0, 0), (3, 3))
        self.update(0, blocks=[], particles=[], entitys=[])

    def update(self, delta_time, blocks, entitys, particles):
        if self.dead: return
        if self.collided:
            self.post_collision_update(delta_time=delta_time)
            return

        for i in blocks:
            if self.hitbox.colliderect(i.rect):
                self.collide(particles=particles)
                return
        for i in entitys:
            if self.hitbox.colliderect(i.hitbox):
                self.collide(particles=particles)
                return
        self.image = pygame.transform.rotate(self.original_image, self.rotangle)
        self.rotangle += 4
        if self.rotangle > 360:
            self.rotangle = 0
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0] + self.dxtotal, self.pos[1] + self.dytotal)
        self.hitbox.center = self.rect.center
        self.dxtotal += self.dx * self.velocity * 50 * delta_time
        self.dytotal -= self.dy * self.velocity * 50 * delta_time
        if self.exploding:
            particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=5,
                                                          particlesize=(1, 1), color=(200, 100, 0), density=1,
                                                          velocity=50,
                                                          distribution=0.7, colorvariation=5))

    def collide(self, particles):
        if self.exploding:
            play_sound('explosion')
            self.explode(particles=particles)
            self.dead = True
        else:
            play_sound('hit')
        self.collided = True

    def post_collision_update(self, delta_time):
        if self.exploding: return
        if self.despawn_seconds < 0:
            self.dead = True
        else:
            self.despawn_seconds -= delta_time

    def explode(self, particles):
        if self.dead: return
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=20,
                                                      particlesize=(7, 7), color=(70, 70, 70), density=15, velocity=30,
                                                      distribution=0.8, colorvariation=5))
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=15,
                                                      particlesize=(3, 3), color=(200, 70, 0), density=10, velocity=40,
                                                      distribution=0.8, colorvariation=30, damage=20))
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=25,
                                                      particlesize=(1, 1), color=(200, 100, 0), density=20, velocity=50,
                                                      distribution=0.7, colorvariation=5))

    def draw(self, surface):
        if self.dead: return
        image = self.image.copy()
        if globs.soft_debug:
            surf = pygame.Surface((self.hitbox.width, self.hitbox.height))
            surf.fill((0, 0, 0))
            hitoutlinesurf = get_outline_mask(surf, color=(255, 0, 0))
            surf = pygame.Surface((image.get_width(), image.get_height()))
            surf.fill((0, 0, 0))
            outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
            image.blit(outlinesurf, (0, 0))
            image.blit(hitoutlinesurf, (self.rect.width / 2 - self.hitbox.width / 2, self.rect.height/2 - self.hitbox.height/2))

        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
