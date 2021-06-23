import time

import pygame

from utils import globs
from utils.images import empty_texture, damage_texture
from utils.__init__ import relToAbs


class entity(pygame.sprite.Sprite):

    def __init__(self, in_web_speed_multiplier=0.75, max_health=20, health=20, damage_overlay_on=True,
                 immune_to_web=False,
                 damage_cooldown=20, damage=1, reach=20, relposy=0, relposx=0, position=(250, 250),
                 velocity=None, original_image=empty_texture, rotation=0, auto_rotation=True, ghost=False):
        pygame.sprite.Sprite.__init__(self)

        if velocity is None:
            velocity = [25, 25]
        self.original_image = original_image
        self.velocity = velocity
        self.position = position
        self.relposx = relposx
        self.relposy = relposy
        self.reach = reach
        self.damage = damage
        self.damage_cooldown = damage_cooldown
        self.immune_to_web = immune_to_web
        self.damage_overlay_on = damage_overlay_on
        self.health = health
        self.max_health = max_health
        self.in_web_speed_multiplier = in_web_speed_multiplier
        self.rotation = rotation
        self.auto_rotation = auto_rotation
        self.speed = max(velocity)
        self.ghost = ghost

        self.image = self.original_image
        self.hurt_animation_cooldown = 0
        self.damage_taken = 0
        self.last_move_time = time.time()
        self.rect = self.image.get_rect()
        self.rect.center = (globs.height / 2, globs.height / 2)

    def move(self, webgroup, main_surf):
        w, h = main_surf.get_size()
        deltatime = time.time() - self.last_move_time
        self.last_move_time = time.time()
        speed_multiplier = 1 * deltatime
        collideweb = pygame.sprite.spritecollideany(self, webgroup)

        if not self.immune_to_web and collideweb:
            speed_multiplier *= self.in_web_speed_multiplier

        self.position = [self.position[0] + (self.velocity[0] * speed_multiplier),
                         self.position[1] + (self.velocity[1] * speed_multiplier)]

        if self.ghost:
            if self.rect.top > h and self.velocity[1] > 0:
                self.position[1] = h - self.rect.height / 2 - 1

            if self.rect.bottom < 0 and self.velocity[1] < 0:
                self.position[1] = 0 + self.rect.width / 2 + 1

            if self.rect.right > w and self.velocity[0] > 0:
                self.position[0] = w - self.rect.width / 2 - 1

            if self.rect.left < 0 and self.velocity[0] < 0:
                self.position[0] = 0 + self.rect.width / 2 + 1

        self.rect.center = self.position
        self.rect.centerx, self.rect.centery = relToAbs(self.relposx), relToAbs(self.relposy)

    def render_image(self):
        if self.damage_overlay_on and self.hurt_animation_cooldown > 0:
            self.original_image = damage_texture
        if self.auto_rotation:
            self.image = pygame.transform.rotate(self.original_image, int(self.rotation))
        else:
            self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, window):
        window.blit(self.image, self.rect)
