from math import pi, atan2, sqrt
import pygame

from utils.images import Texture
from render.sprites.entity import Entity

class Apprentice(Entity):

    def __init__(self, pos, health=None, weapon=None):
        self.priority = 2
        self.position = pos
        Entity.__init__(self, auto_movement=True, position=pos)
        if health is not None:
            self.health = health
        self.tex_up = Texture("resources/textures/apprentice_animation_up.png")
        self.tex_down = Texture("resources/textures/apprentice_animation_down.png")
        self.tex_right = Texture("resources/textures/apprentice_animation_right.png")
        self.tex_left = Texture("resources/textures/apprentice_animation_left.png")
        self.tex_idle = Texture("resources/textures/apprentice_animation_idle.png")
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.velocity = 5

    def update(self, webs, blocks, particles):
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()

        self.move(webs=webs, blocks=blocks, particles=particles)
