import pygame

from utils import globs
from utils.images import images
from render.sprites import particle_cloud

class Camera:
    def __init__(self):
        self.rect = pygame.Rect((0, 0), globs.SIZE)
        self.target = None

    def follow(self, target=None):
        if target is None:
            self.rect.center = (0, 0)
        else:
            self.rect.center = target.rect.center
            self.target = target

    def update(self):
        self.rect.center = self.target.rect.center

    def get_objects(self, objects=None):
        obj_list = []
        if objects is None:
            objects = []
        for i in objects:
            if i.rect.colliderect(self.rect):
                obj_list.append(i)
        return obj_list


class Scene:
    def __init__(self, sidelength):
        self.surface, rect = None, None
        self.sidelength = sidelength
        self.objects, self.objects_toblit = [], []
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        self.camera = Camera()

    def update(self, playerentity, delta_time, blocks, entitys, particles, projectiles, melee):
        if not globs.soft_debug:particles.append(particle_cloud.ParticleCloud(center=(self.surface.get_width() / 2, 0), radius=self.surface.get_width(),
                                                          particlesize=(1, 1), color=(255, 0, 0), density=1, spawnregion=(2, self.surface.get_height() / 2),
                                                          velocity=100, priority=0, no_debug=True, distribution=0.5, colorvariation=100))
        self.objects = entitys + projectiles + melee + particles
        self.objects.append(playerentity)
        for i in self.objects:
            i.update(delta_time=delta_time, blocks=blocks, particles=particles, projectiles=projectiles, player=playerentity, entitys=entitys, melee=melee)
        self.objects += blocks
        self.camera.update()
        self.objects_toblit = self.camera.get_objects(objects=self.objects)
        self.objects_toblit.append(playerentity)
        self.objects = []

    def draw(self, surface):
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        if globs.hard_debug:
            self.surface.blit(images["debug_scene"], (0, 0))

        for i in range(3, -1, -1):
            for j in self.objects_toblit:
                if j.priority == i:
                    j.draw(surface=self.surface)
                    #self.objects_toblit.remove(j)

        self.rect = self.surface.get_rect()
        if globs.hard_debug:
            self.rect.center = (0, 0)
            surf = pygame.transform.scale(self.surface, (surface.get_height(), surface.get_height()))
            surface.blit(surf, (0, 0))
        else:
            self.rect.center = (-self.camera.rect.centerx+surface.get_width()/2, -self.camera.rect.centery+surface.get_height()/2)
            surface.blit(self.surface, self.rect)

