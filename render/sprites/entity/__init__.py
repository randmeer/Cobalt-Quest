import time

import pygame

from utils import globs, rta_height, dual_rect_anchor, get_outline_mask
from utils.images import empty_tx, damage_tx


class Entity(pygame.sprite.Sprite):

    def __init__(self, in_web_speed_multiplier=0.75, max_health=20, health=20, damage_overlay_on=True,
                 immune_to_web=False,
                 damage_cooldown=20, damage=1, reach=20, relposy=0, relposx=0, position=(0, 0),
                 original_image=empty_tx, rotation=0, auto_rotation=True, ghost=False,
                 hitboxsize=(16, 16), hitboxanchor="midbottom"):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = original_image
        self.offset = [0, 0]
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
        self.speed_multiplier = None
        self.rotation = rotation
        self.auto_rotation = auto_rotation
        #self.speed = max(velocity)
        self.velocity = 25
        #self.ghost = ghost

        self.image = self.original_image
        self.hurt_animation_cooldown = 0
        self.damage_taken = 0
        self.last_move_time = time.time()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.hitbox = pygame.Rect((0, 0), (16, 16))
        self.hitboxanchor = hitboxanchor

    def check_block_collision(self, blocks):
        pass

    def move(self, webgroup, scene, blocks):
        w, h = scene.get_size()
        deltatime = time.time() - self.last_move_time
        self.last_move_time = time.time()
        self.speed_multiplier = 1 * deltatime
        collideweb = pygame.sprite.spritecollideany(self, webgroup)

        if not self.immune_to_web and collideweb:
            self.speed_multiplier *= self.in_web_speed_multiplier

        self.position = [self.position[0] + (self.offset[0] * self.speed_multiplier),
                         self.position[1] + (self.offset[1] * self.speed_multiplier)]

        # if self.ghost:
        #     if self.rect.top > h and self.offset[1] > 0:
        #         self.position[1] = h - self.rect.height / 2 - 1

        #     if self.rect.bottom < 0 and self.offset[1] < 0:
        #         self.position[1] = 0 + self.rect.width / 2 + 1

        #     if self.rect.right > w and self.offset[0] > 0:
        #         self.position[0] = w - self.rect.width / 2 - 1

        #     if self.rect.left < 0 and self.offset[0] < 0:
        #         self.position[0] = 0 + self.rect.width / 2 + 1
        pos = (round(self.position[0]), round(self.position[1]))
        self.rect.center = self.position
        dual_rect_anchor(self.hitbox, self.rect, self.hitboxanchor)
        if globs.debug:
            surf = pygame.Surface((self.hitbox.width, self.hitbox.height))
            surf.fill((0, 0, 0))
            hitoutlinesurf = get_outline_mask(surf, color=(255, 0, 0))
            surf = pygame.Surface((self.image.get_width(), self.image.get_height()))
            surf.fill((0, 0, 0))
            outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
            self.image.blit(outlinesurf, (0, 0))
            self.image.blit(hitoutlinesurf, (self.rect.width/2 - self.hitbox.width/2, self.rect.height-self.hitbox.height))

    def undo_move(self):
        self.position = [self.position[0] - (self.offset[0] * self.speed_multiplier),
                         self.position[1] - (self.offset[1] * self.speed_multiplier)]
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom

    def render_image(self):
        if self.damage_overlay_on and self.hurt_animation_cooldown > 0:
            self.original_image = damage_tx
        if self.auto_rotation:
            self.image = pygame.transform.rotate(self.original_image, int(self.rotation))
        else:
            self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x+surface.get_width()/2, self.rect.y+surface.get_height()/2))
        #print(self.rect.x, self.rect.y)