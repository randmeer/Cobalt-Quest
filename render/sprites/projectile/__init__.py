import math
import pygame

from utils import play_sound, globs, conv_rad_deg, debug_outlines
from render.sprites import particle_cloud

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, pos, radians, hitbox=(3, 3), rotating=False, rotation_increment=0, velocity=3, exploding=False, damage=10):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 3
        self.dead = False
        self.collided = False
        self.damage=10
        self.exploding = exploding
        self.rotating = rotating
        self.rot_increment = rotation_increment
        self.rot_angle = 0
        self.despawn_seconds = 4
        self.pos, self.radians, self.velocity = pos, radians, velocity
        self.original_image = image
        self.image = self.original_image
        if not self.rotating:
            self.image = pygame.transform.rotate(self.original_image, -conv_rad_deg(self.radians)+45)
        self.rect = self.image.get_rect()
        self.dx = math.sin(self.radians)
        self.dy = math.cos(self.radians)
        self.dxtotal, self.dytotal = 0, 0
        self.hitbox = pygame.Rect((0, 0), hitbox)

        self.projectile_update(0, blocks=[], particles=[], entitys=[])

    def projectile_update(self, delta_time, blocks, entitys, particles):
        if self.dead: return
        if self.collided:
            self.post_collision_update(delta_time=delta_time)
            return

        for i in blocks:
            if self.hitbox.colliderect(i.rect):
                self.collide(particles=particles, sound="blockplace")
                return
        for i in entitys:
            if self.hitbox.colliderect(i.hitbox):
                self.collide(particles=particles, sound="hit")
                i.damage(damage=self.damage, particles=particles, pos=self.hitbox.center)
                self.despawn_seconds = 1
                return

        if self.rotating:
            self.image = pygame.transform.rotate(self.original_image, self.rot_angle)
            self.rot_angle += 4
            if self.rot_angle > 360:
                self.rot_angle = 0
            self.rect = self.image.get_rect()

        self.rect.center = (self.pos[0] + self.dxtotal, self.pos[1] + self.dytotal)
        self.hitbox.center = self.rect.center
        self.dxtotal += self.dx * self.velocity * 50 * delta_time
        self.dytotal -= self.dy * self.velocity * 50 * delta_time

    def collide(self, particles, sound):
        if self.exploding:
            play_sound('explosion')
            self.explode(particles=particles)
            self.dead = True
        else:
            play_sound(sound)

        self.collided = True

    def post_collision_update(self, delta_time):
        self.despawn_seconds -= delta_time
        if self.despawn_seconds < 0:
            self.dead = True

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
        image = self.image
        if globs.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect)
        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
