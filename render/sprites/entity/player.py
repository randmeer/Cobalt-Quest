from math import pi, atan2
import pygame

from utils.images import Texture
from render.sprites.entity import Entity
from utils import get_setting, rta_dual_height

class Player(Entity):

    def __init__(self, pos):
        self.position = pos
        Entity.__init__(self)
        self.playeruptex = Texture("resources/textures/player_animation_up.png")
        self.playerdowntex = Texture("resources/textures/player_animation_down.png")
        self.playerrighttex = Texture("resources/textures/player_animation_right.png")
        self.playerlefttex = Texture("resources/textures/player_animation_left.png")
        self.playeridletex = Texture("resources/textures/player_animation_idle.png")

    def update(self, webgroup, scene, blocks):
        self.offset = [0, 0]
        velocity = self.velocity
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity /= 2

        self.image = self.playeridletex.get()
        self.rect = self.image.get_rect()

        if key[pygame.K_s]:
            self.offset[1] += velocity
            self.image = self.playerdowntex.get()
        if key[pygame.K_w]:
            self.offset[1] -= velocity
            self.image = self.playeruptex.get()
        if key[pygame.K_d]:
            self.offset[0] += velocity
            self.image = self.playerrighttex.get()
        if key[pygame.K_a]:
            self.offset[0] -= velocity
            self.image = self.playerlefttex.get()

        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        # init_rot = (180 / pi) * -atan2(rel_x, rel_y) - 180
        # self.rotation = -init_rot

        self.move(webgroup=webgroup, scene=scene, blocks=blocks)
        #if self.rect.collidelist(blocks) == []:
        #    self.undo_move()
        #    print("undid move")
        for i in blocks:
            if self.hitbox.colliderect(i.rect):
                self.undo_move()
                print("undid move")

        #self.render_image()
