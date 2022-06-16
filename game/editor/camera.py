
from octagon.utils import get_setting, img
from octagon.environment import Environment

from game.floor import Floor
from game.editor import hud
from game.editor.entity import EditorEntity
from octagon.environment.camera import Scene as cameraScene
from game import globs
from game.sprite.projectile import shuriken, arrow
from game.sprite.attack import dagger, hands, katana
from game.overlay import pause, inventory, end_screen
from game.editor.entity import Player
from game.editor.entity import Apprentice
from game.sprite.particle import environment
from octagon.utils import mp_screen, img, play_sound
from octagon.utils.static import tuple_subtract, tuple_add, tuple_factor

import time
import pygame
import QuickJSON
import copy
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from octagon.utils import render_text, var, img, cout, mp_scene
from octagon.sprites import block

class Camera:
    def __init__(self):
        self.rect = pygame.Rect((0, 0), var.SIZE)
        self.target = None

    def follow(self, target=None):
        if target is None:
            self.rect.center = (0, 0)
        else:
            self.rect.center = target.center
            self.target = target

    def follow_pos(self, x, y):
        self.target = pygame.sprite.Sprite
        self.target.center = x, y

    def update(self):
        self.rect.center = self.target.center

    def get_objects(self, objects=None):
        obj_list = []
        if objects is None:
            objects = []
        if var.render_all:
            return objects
        else:
            for i in objects:
                if i.rect.colliderect(self.rect):
                    obj_list.append(i)
            return obj_list

class Scene(cameraScene):
    def __init__(self, env):
        self.env = env
        self.surface, rect = None, None
        self.sidelength = env.sidelength
        self.objects, self.objects_toblit = [], []
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.camera = Camera()

    def update(self):
        self.objects = self.env.entities + self.env.projectiles + self.env.melee + self.env.particles
        self.objects.append(self.env.player)
        self.objects += self.env.blocks
        self.camera.update()
        self.objects_toblit = self.camera.get_objects(objects=self.objects)
        self.objects = []

    def draw(self, surface):
        # self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        # self.surface.fill((0, 0, 0, 0))
        self.surface.fill((0, 0, 0, 0), pygame.Rect(self.camera.rect.centerx + self.env.sidelength / 2 - self.camera.rect.width / 2,
                                      self.camera.rect.centery + self.env.sidelength / 2 - self.camera.rect.height / 2,
                                      self.camera.rect.width, self.camera.rect.height))

        for i in range(3, -1, -1):
            for j in self.objects_toblit:
                if j.priority == i:
                    j.draw(surface=self.surface)

        if var.hard_debug:
            surf = pygame.transform.scale(self.surface, (surface.get_height(), surface.get_height()))
            surface.blit(surf, (0, 0))
            return
        # elif self.zoom == 1:
        self.rect.center = (-self.camera.rect.centerx+surface.get_width()/2, -self.camera.rect.centery+surface.get_height()/2)
        surface.blit(self.surface, self.rect)
        # else:
        #     self.rect.center = (-self.camera.target.centerx+surface.get_width()/2, -self.camera.target.centery+surface.get_height()/2)
        #     surf = pygame.transform.scale(self.surface, (surface.get_height()*self.zoom, surface.get_height()*self.zoom))
        #     surface.blit(surf, self.rect.center)
