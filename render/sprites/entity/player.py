from math import pi, atan2
import pygame

from utils.images import rande_tx, Elia03_tx, empty_tx
from render.sprites.entity import Entity
from utils import get_setting, rta_dual_height

class Player(Entity):

    def __init__(self, pos):
        self.position = pos
        Entity.__init__(self, original_image=empty_tx)

    def update(self, webgroup, scene) -> None:
        self.velocity = [0, 0]
        speed = self.speed
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            speed /= 2

        if key[pygame.K_s]:
            self.velocity[1] += speed
        if key[pygame.K_w]:
            self.velocity[1] -= speed
        if key[pygame.K_d]:
            self.velocity[0] += speed
        if key[pygame.K_a]:
            self.velocity[0] -= speed

        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        # init_rot = (180 / pi) * -atan2(rel_x, rel_y) - 180
        # self.rotation = -init_rot
        self.move(webgroup=webgroup, scene=scene)
        self.render_image()
