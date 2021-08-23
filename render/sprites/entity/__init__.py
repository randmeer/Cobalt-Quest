import time
import random
import pygame

from utils import globs, rta_height, dual_rect_anchor, get_outline_mask
from utils.images import empty_tx, damage_tx


class Entity(pygame.sprite.Sprite):

    def __init__(self, in_web_speed_multiplier=0.75, max_health=20, health=20, damage_overlay_on=True,
                 immune_to_web=False, damage_cooldown=20, damage=1, reach=20, relposy=0, relposx=0, position=(0, 0),
                 rotation=0, auto_rotation=True, hitboxsize=(16, 16), hitboxanchor="midbottom", auto_movement=False,
                 auto_distance_max=2000):
        pygame.sprite.Sprite.__init__(self)
        self.tex_down = self.tex_up = self.tex_left = self.tex_right = self.tex_idle = None
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
        self.velocity = 25
        self.hurt_animation_cooldown = 0
        self.damage_taken = 0
        self.last_move_time = time.time()
        self.hitbox = pygame.Rect((0, 0), hitboxsize)
        self.hitboxanchor = hitboxanchor
        self.auto_move = auto_movement
        if self.auto_move:
            self.auto_direction = 0
            self.auto_distance = 0
            self.auto_distance_max = auto_distance_max

    def check_block_collision(self, blocks):
        for i in blocks:
            if self.hitbox.colliderect(i.rect):
                return True

    def _undo_move(self, direction):
        if direction == "x" or direction == "xy":
            self.position = [self.position[0] - (self.offset[0] * self.speed_multiplier),
                             self.position[1]]
        if direction == "y" or direction == "xy":
            self.position = [self.position[0],
                             self.position[1] - (self.offset[1] * self.speed_multiplier)]
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def _move(self, direction):
        if direction == "x" or direction == "xy":
            self.position = [self.position[0] + (self.offset[0] * self.speed_multiplier),
                             self.position[1]]
        if direction == "y" or direction == "xy":
            self.position = [self.position[0],
                             self.position[1] + (self.offset[1] * self.speed_multiplier)]
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def move(self, webs, blocks):
        deltatime = time.time() - self.last_move_time
        self.last_move_time = time.time()
        self.speed_multiplier = 1 * deltatime
        collideweb = pygame.sprite.spritecollideany(self, webs)

        if not self.immune_to_web and collideweb:
            self.speed_multiplier *= self.in_web_speed_multiplier

        if self.auto_move:
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

    # def render_image(self):
    #    if self.damage_overlay_on and self.hurt_animation_cooldown > 0:
    #        self.original_image = damage_tx
    #    if self.auto_rotation:
    #        self.image = pygame.transform.rotate(self.original_image, int(self.rotation))
    #    else:
    #        self.image = self.original_image
    #    self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface):
        image = self.image.copy()

        if globs.soft_debug:
            surf = pygame.Surface((self.hitbox.width, self.hitbox.height))
            surf.fill((0, 0, 0))
            hitoutlinesurf = get_outline_mask(surf, color=(255, 0, 0))
            surf = pygame.Surface((image.get_width(), image.get_height()))
            surf.fill((0, 0, 0))
            outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
            image.blit(outlinesurf, (0, 0))
            image.blit(hitoutlinesurf, (self.rect.width / 2 - self.hitbox.width / 2, self.rect.height - self.hitbox.height))
            print("hitbox")
        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
        # print(self.rect.x, self.rect.y)
