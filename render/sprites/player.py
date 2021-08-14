from math import pi, atan2

import pygame

from utils import globs
from utils.__init__ import getSetting, relToAbs, rta_dual


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skin = getSetting('skin')
        self.update_skin()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (globs.height / 2, globs.height / 2)
        self.velocity = 0.0
        self.position = (0, 0)
        self.relposx = self.relposy = 0.5
        self.reach = 0.25
        self.hurtanimationcooldown = 0
        self.tookdamage = False
        self.angle = 0

    def update(self, webgroup, delta_time):
        collideweb = pygame.sprite.spritecollideany(self, webgroup)
        w, h = pygame.display.get_surface().get_size()

        if collideweb:
            self.velocity = 0.1 * delta_time
        else:
            self.velocity = 0.2 * delta_time

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            self.velocity = 0.1 * delta_time

        if key[pygame.K_s] and self.rect.bottom < h:
            self.relposy += self.velocity
        if key[pygame.K_w] and self.rect.top > 0:
            self.relposy -= self.velocity
        if key[pygame.K_d] and self.rect.right < w:
            self.relposx += self.velocity
        if key[pygame.K_a] and self.rect.left > 0:
            self.relposx -= self.velocity

        self.position = self.rect.center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / pi) * -atan2(rel_y, rel_x) - 90

        if self.tookdamage:
            self.tookdamage = False
            self.hurtanimationcooldown = 10
            self.original_image.blit(pygame.transform.scale(damage_image, (rta_dual(0.1, 0.1))), (0, 0))

        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.position)

        if self.hurtanimationcooldown > 0:
            self.hurtanimationcooldown -= 100 * delta_time
        else:
            self.update_skin()

        self.rect.centerx, self.rect.centery = relToAbs(self.relposx), relToAbs(self.relposy)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def update_skin(self):
        self.skin = getSetting('skin')
        if self.skin == '3lia03':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(elia_texture, (relToAbs(0.1), relToAbs(0.1))))
        elif self.skin == 'Rande':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(rande_texture, (relToAbs(0.1), relToAbs(0.1))))
