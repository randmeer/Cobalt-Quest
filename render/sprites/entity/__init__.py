import random
import pygame

from utils import globs, dual_rect_anchor, debug_outlines, mask_overlay
from render.sprites import particle_cloud

class Entity(pygame.sprite.Sprite):

    def __init__(self, in_web_speed_multiplier=0.75, max_health=20, health=20, damage_overlay_on=True,
                 immune_to_web=False, hurt_cooldown=0.5, position=(0, 0), rotation=0, auto_rotation=True,
                 hitboxsize=(16, 16), hitboxanchor="midbottom", auto_movement=False, auto_distance_max=2000):
        pygame.sprite.Sprite.__init__(self)
        self.dead = False
        self.tex_down = self.tex_up = self.tex_left = self.tex_right = self.tex_idle = None
        self.offset = [0, 0]
        self.position = position
        self.hc = 0
        self.hc_max = hurt_cooldown
        self.hc_ani = 0.25
        self.immune_to_web = immune_to_web
        self.damage_overlay_on = damage_overlay_on
        self.health = health
        self.max_health = max_health
        self.in_web_speed_multiplier = in_web_speed_multiplier
        self.speed_multiplier = None
        self.rotation = rotation
        self.auto_rotation = auto_rotation
        self.velocity = 25
        self.hitbox = pygame.Rect((0, 0), hitboxsize)
        self.hitboxanchor = hitboxanchor
        self.auto_move = auto_movement
        if self.auto_move:
            self.auto_direction = 0
            self.auto_distance = 0
            self.auto_distance_max = auto_distance_max

    def damage_overlay(self):
        if self.damage_overlay_on:
            pass

    def entity_update(self, webs, blocks, particles, delta_time):
        self.rect = self.image.get_rect()
        self.move(webs=webs, blocks=blocks, particles=particles, delta_time=delta_time)
        if self.health <= 0:
            self.dead = True
            particles.append(particle_cloud.ParticleCloud(center=self.hitbox.center, spawnregion=(self.hitbox.width/2, self.hitbox.height/2), radius=self.hitbox.height, particlesize=(1, 1), color=(255, 50, 0), density=40, velocity=50, colorvariation=20, priority=3, distribution=0.5))
            particles.append(particle_cloud.ParticleCloud(center=self.hitbox.center, radius=self.hitbox.height/1.5, particlesize=(2, 2), color=(100, 10, 0), density=30, velocity=30, colorvariation=20, priority=3, distribution=0.5))
        if self.hc >= 0:
            self.hc -= delta_time

        if self.hc > self.hc_max - self.hc_ani:
            self.image = mask_overlay(image=self.image)

    def damage(self, damage, particles, pos=None):
        if pos is None:
            pos = self.hitbox.center
        if self.hc < 0:
            self.health -= damage
            self.hc = self.hc_max
        particles.append(particle_cloud.ParticleCloud(center=pos, radius=6, particlesize=(1, 1), color=(200, 20, 0), density=30, velocity=20, priority=1, distribution=0.5))

    def check_block_collision(self, blocks):
        # return pygame.sprite.spritecollideany(self, blocks)
        for i in blocks:
            if self.hitbox.colliderect(i.rect):
                return True

    def _undo_move(self, direction):
        if direction == "x" or direction == "xy":
            self.position = [self.position[0] - (self.offset[0] * self.speed_multiplier), self.position[1]]
        if direction == "y" or direction == "xy":
            self.position = [self.position[0], self.position[1] - (self.offset[1] * self.speed_multiplier)]
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def _move(self, direction):
        if direction == "x" or direction == "xy":
            self.position = [self.position[0] + (self.offset[0] * self.speed_multiplier), self.position[1]]
        if direction == "y" or direction == "xy":
            self.position = [self.position[0], self.position[1] + (self.offset[1] * self.speed_multiplier)]
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def move(self, webs, blocks, particles, delta_time):
        self.speed_multiplier = delta_time
        collideweb = pygame.sprite.spritecollideany(self, webs)

        if not self.immune_to_web and collideweb:
            self.speed_multiplier *= self.in_web_speed_multiplier

        if self.auto_move:
            self.image = self.tex_idle.get()
            self.offset = [0, 0]
            if self.auto_distance <= 0:
                self.auto_direction = random.randrange(4)
                self.auto_distance = random.randrange(self.auto_distance_max)
            self.offset = [0, 0]
            velocity = self.velocity
            if self.auto_direction == 0:
                self.offset[1] += velocity
                self.image = self.tex_down.get()
            if self.auto_direction == 1:
                self.offset[1] -= velocity
                self.image = self.tex_up.get()
            if self.auto_direction == 2:
                self.offset[0] += velocity
                self.image = self.tex_right.get()
            if self.auto_direction == 3:
                self.offset[0] -= velocity
                self.image = self.tex_left.get()
            self.auto_distance -= velocity
            self._move("xy")
            if self.check_block_collision(blocks):
                self._undo_move("xy")
                self.auto_direction = random.randrange(4)
        else:
            self._move("x")
            if self.check_block_collision(blocks):
                self._undo_move("x")
            self._move("y")
            if self.check_block_collision(blocks):
                self._undo_move("y")

        dual_rect_anchor(self.hitbox, self.rect, self.hitboxanchor)
        if self.offset != [0, 0]:
            particles.append(particle_cloud.ParticleCloud(center=(self.hitbox.midbottom[0], self.hitbox.midbottom[1]-2), radius=3, particlesize=(2, 2), color=(40, 20, 20), density=1, velocity=20, colorvariation=10, priority=self.priority+1))

    def draw(self, surface):
        if self.dead: return
        image = self.image
        if globs.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect, anchor="midbottom")
        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
