from math import pi, atan2, sqrt
import pygame

from utils.images import Texture
from render.sprites.entity import Entity

class Player(Entity):

    def __init__(self, pos):
        self.position = pos
        Entity.__init__(self)
        self.tex_up = Texture("resources/textures/player_animation_up.png")
        self.tex_down = Texture("resources/textures/player_animation_down.png")
        self.tex_right = Texture("resources/textures/player_animation_right.png")
        self.tex_left = Texture("resources/textures/player_animation_left.png")
        self.tex_idle = Texture("resources/textures/player_animation_idle.png")
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

    def update(self, webs, blocks):
        self.offset = [0, 0]
        velocity = self.velocity
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity /= 2

        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()

        # following code would move the player the same distance even with 2 keys pressed at the same time
        # but it feels kinda weird so commented it for now

        # keys = 0
        # if key[pygame.K_s]:
        #     keys += 1
        # if key[pygame.K_w]:
        #     keys += 1
        # if key[pygame.K_d]:
        #     keys += 1
        # if key[pygame.K_a]:
        #     keys += 1
        # if keys >= 2:
        #     velocity = self.velocity/math.sqrt(self.velocity)

        if key[pygame.K_s]:
            self.offset[1] += velocity
            self.image = self.tex_down.get()
        if key[pygame.K_w]:
            self.offset[1] -= velocity
            self.image = self.tex_up.get()
        if key[pygame.K_d]:
            self.offset[0] += velocity
            self.image = self.tex_right.get()
        if key[pygame.K_a]:
            self.offset[0] -= velocity
            self.image = self.tex_left.get()
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        # init_rot = (180 / pi) * -atan2(rel_x, rel_y) - 180
        # self.rotation = -init_rot

        self.move(webs=webs, blocks=blocks)




        #self.render_image()
