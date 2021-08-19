from math import pi, atan2
import pygame

from utils.images import rande_tx, Elia03_tx, empty_tx
from render.sprites.entity import Entity
from utils import get_setting, rta_dual_height


# noinspection DuplicatedCode
class Player(Entity):

    def __init__(self, pos):
        self.position = pos
        Entity.__init__(self, original_image=empty_tx)
        self.skin = get_setting('skin')
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
        self.skin = get_setting('skin')
        if self.skin == '3lia03':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(Elia03_tx, rta_dual_height(0.1, 0.1)))
        elif self.skin == 'Rande':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(rande_tx, rta_dual_height(0.1, 0.1)))
