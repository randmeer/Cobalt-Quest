import math
#from math import pi, atan2, sqrt
import pygame

import utils
from utils import mp_scene, angle_deg, hypo, conv_deg_rad, sign
from utils.images import Texture
from render.sprites.entity import Entity
from render.sprites import particle_cloud

class Player(Entity):

    def __init__(self, pos):
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
        self.swing = False
        self.swing_timer = 0
        self.swing_target = (0, 0)
        self.swing_rot = 0

    def start_swing(self, scene):
        if not self.swing:
            mp = mp_scene(scene=scene)
            self.swing = True
            self.swing_deg = angle_deg(self.hitbox.center, mp)
            self.swing_rad = conv_deg_rad(self.swing_deg)
            dx = math.sin(self.swing_rad)
            dy = math.cos(self.swing_rad)
            self.swing_target = (self.position[0]+dx*20, self.position[1]-dy*20)
            self.swing_image = Texture("resources/textures/swing.png", single_run=True, set_height=16)
            self.images = []
            self.images.append([None, None])
            self.images[0][0] = pygame.transform.rotate(self.swing_image.get(), -self.swing_deg)
            self.images[0][1] = self.images[0][0].get_rect()
            self.images[0][1].center = self.swing_target

    def update(self, webs, blocks, particles, delta_time):
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

        self.move(webs=webs, blocks=blocks)
        if self.offset != [0, 0]:
            particles.append(particle_cloud.ParticleCloud(center=self.hitbox.midbottom, radius=3, particlesize=(2, 2), color=(40, 20, 20), density=2, velocity=30, colorvariation=10))
            utils.play_sound('step')
        if self.swing:
            if self.swing_image.get() == False:
                self.swing = False
                self.images = []
            else:
                self.images[0][0] = pygame.transform.rotate(self.swing_image.get(), -self.swing_deg)
