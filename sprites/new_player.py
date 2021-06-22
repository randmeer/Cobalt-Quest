from math import pi, atan2

import pygame

from sprites.entity import entity
from utils import getSetting, relToAbs

elia_texture = pygame.image.load("textures/3lia03.png")
rande_texture = pygame.image.load("textures/rande.png")
damage_image = pygame.image.load("textures/damage.png")
empty_texture = pygame.image.load("textures/empty.png")

# noinspection DuplicatedCode
class Player(entity):

    def __init__(self):

        entity.__init__(self, original_image=empty_texture)
        self.skin = getSetting('skin')
        self.update_skin()

    def update(self, webgroup, main_surface) -> None:
        self.velocity = [0, 0]
        key = pygame.key.get_pressed()

        if key[pygame.K_s]:
            self.velocity[1] += self.speed
        if key[pygame.K_w]:
            self.velocity[1] += -self.speed
        if key[pygame.K_d]:
            self.velocity[0] += self.speed
        if key[pygame.K_a]:
            self.velocity[0] += -self.speed

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        init_rot = (180 / pi) * -atan2(rel_x, rel_y) - 180
        self.rotation = -init_rot
        self.move(webgroup=webgroup, main_surf=main_surface)
        self.render_image()

    def update_skin(self):
        self.skin = getSetting('skin')
        if self.skin == '3lia03':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(elia_texture, (relToAbs(0.1), relToAbs(0.1))))
        elif self.skin == 'Rande':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(rande_texture, (relToAbs(0.1), relToAbs(0.1))))
