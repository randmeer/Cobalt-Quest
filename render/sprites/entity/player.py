import pygame

from utils import play_sound
from utils.images import Texture
from render.sprites.entity import Entity

class Player(Entity):

    def __init__(self, pos):
        self.priority = 1
        self.position = pos
        Entity.__init__(self, position=pos)
        self.tex_up = Texture("resources/textures/player_animation_up.png")
        self.tex_down = Texture("resources/textures/player_animation_down.png")
        self.tex_right = Texture("resources/textures/player_animation_right.png")
        self.tex_left = Texture("resources/textures/player_animation_left.png")
        self.tex_idle = Texture("resources/textures/player_animation_idle.png")
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

    def update(self, webs, blocks, particles, delta_time):
        if self.dead: return

        self.offset = [0, 0]
        velocity = self.velocity
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity /= 2

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
        self.image = self.tex_idle.get()

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
        self.entity_update(webs=webs, blocks=blocks, particles=particles, delta_time=delta_time)

        if self.offset != [0, 0]:
            play_sound('step')


