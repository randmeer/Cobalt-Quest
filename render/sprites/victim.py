import math
import random

import pygame

from utils import globs, __init__
from utils.images import damage_texture, ichkeksi_texture
from utils.__init__ import atr_height, rta_height, rta_dual

# noinspection DuplicatedCode
class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.testsurface = pygame.Surface((50, 50))
        self.original_image = ichkeksi_texture
        self.damage = damage_texture
        self.image = pygame.transform.scale(ichkeksi_texture, (rta_dual(0.1, 0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.direction = random.randint(1, 4)
        self.onscreen = True
        self.velocity = globs.savegame
        self.health = globs.victimhealthpointsmax
        self.breakcooldown = 0
        self.relposx = self.relposy = 0
        self.tookdamage = False
        self.damage_animation_cooldown = 10

    @staticmethod
    def summon():
        self = Victim()
        if self.onscreen:
            position = random.randint(rta_height(0.1), rta_height(0.9))

            if self.direction == 1:
                self.rect.center = (position, rta_height(0.1) * -1)
                self.relposx = atr_height(position - rta_height(0.05))
                self.relposy = atr_height(rta_height(0.1) * -1 - rta_height(0.05))

            elif self.direction == 3:
                self.rect.center = (position, rta_height(1.1))
                self.relposx = atr_height(position - rta_height(0.05))
                self.relposy = atr_height(rta_height(1.1) - rta_height(0.05))

            elif self.direction == 2:
                self.rect.center = (rta_height(1.1), position)
                self.relposx = atr_height(rta_height(1.1) - rta_height(0.05))
                self.relposy = atr_height(position - rta_height(0.05))

            elif self.direction == 4:
                self.rect.center = (rta_height(0.1) * -1, position)
                self.relposx = atr_height(rta_height(0.1) * -1 - rta_height(0.05))
                self.relposy = atr_height(position - rta_height(0.05))
        return self

    def update(self, player, click, webgroup, delta_time):
        if self.onscreen:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideweb = pygame.sprite.spritecollideany(self, webgroup)
            collideplayer = self.rect.colliderect(player.rect)
            collidereach = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)

            if collideweb:
                if self.breakcooldown > globs.victimbreakcooldownmax:
                    collideweb.kill()
                    self.breakcooldown = 0
                self.breakcooldown += 1
                self.velocity = 0.05 * delta_time * globs.savegame
            else:
                self.velocity = 0.1 * delta_time

            if self.direction == 1:
                self.relposy += self.velocity

            elif self.direction == 2:
                self.relposx -= self.velocity

            elif self.direction == 3:
                self.relposy -= self.velocity

            elif self.direction == 4:
                self.relposx += self.velocity

            self.rect.x, self.rect.y = rta_height(self.relposx), rta_height(self.relposy)

            if self.rect.centerx > rta_height(1.1) or self.rect.centerx < rta_height(
                    0.1) * -1 or self.rect.centery > rta_height(1.1) or self.rect.centery < rta_height(0.1) * -1:
                self.kill()
                self.rect = None
                self.onscreen = False
                self.health = -1
                globs.victimsmissed += 1

            if self.damage_animation_cooldown > 0:
                self.damage_animation_cooldown -= 100 * delta_time
            elif self.damage_animation_cooldown < 0:
                self.image = pygame.transform.scale(ichkeksi_texture, (rta_dual(0.1, 0.1)))
                self.damage_animation_cooldown -= 100 * delta_time

            if click and collidemouse and collidereach <= rta_height(player.reach):
                self.damage_animation_cooldown = 5
                surface = pygame.transform.scale(ichkeksi_texture, (rta_dual(0.1, 0.1)))
                surface.blit(pygame.transform.scale(damage_texture, (rta_dual(0.1, 0.1))), (0, 0))
                self.image = surface
                self.health -= 1
                globs.damagesum += 1
                __init__.play_sound('hit')

            if collideplayer and globs.damagecooldown >= globs.maxcooldown:
                globs.playerhealthpoints -= 1
                globs.damagecooldown = 0
                player.tookdamage = True
                __init__.play_sound('hurt')

            if self.health == 0:
                self.kill()
                self.rect = None
                globs.victimskilled += 1
                self.onscreen = False

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (rta_dual(0.1, 0.1)))
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)
        if self.tookdamage:
            window.blit(self.damage, self.rect)
