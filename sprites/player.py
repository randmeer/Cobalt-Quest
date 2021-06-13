import pygame
from math import pi
from math import atan2
import globals
from utils import getSetting
from utils import relToAbs

elia_texture = pygame.image.load("textures/3lia03.png")
rande_texture = pygame.image.load("textures/rande.png")
damage_image = pygame.image.load("textures/damage.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skin = getSetting('skin')
        self.update_skin()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (globals.WIDTH / 2, globals.HEIGHT / 2)
        self.velocity = 0.0
        self.position = (0, 0)
        self.relposx = 0.5
        self.relposy = 0.5
        self.reach = 0.25

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
        angle = (180 / pi) * -atan2(rel_y, rel_x) - 90

        globals.damage_animation_cooldown -= 1
        if globals.damage_animation_cooldown < 1:
            self.update_skin()
        if globals.player_hurt:
            self.original_image.blit(pygame.Surface.convert_alpha(
                pygame.transform.scale(damage_image, (50, 50))), (0, 0))

        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.position)

        self.rect.centerx = relToAbs(self.relposx)
        self.rect.centery = relToAbs(self.relposy)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def update_skin(self):
        if self.skin == '3lia03':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(elia_texture, (relToAbs(0.1), relToAbs(0.1))))
        elif self.skin == 'Rande':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(rande_texture, (relToAbs(0.1), relToAbs(0.1))))
