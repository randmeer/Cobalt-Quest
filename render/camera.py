import pygame

from utils import globs
from utils.images import scene_test_tx

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
    # def __init__(self, path, flags=None, depth=None, masks=None):
    def __init__(self, path, sidelength):
        self.surface = None
        self.rect = None
        self.sidelength = sidelength
        self.objects = []
        self.objects_toblit = []
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        # Surface.__init__(self.sidelength, flags, depth, masks)
        self.camera = Camera()
        print("[Scene] initialized Scene")

    def update(self, playerentity, blocks=None, entitys=None, particles=None, othersprites=None):
        if entitys is None:
            entitys = []
        if blocks is None:
            blocks = []
        if particles is None:
            particles = []
        if othersprites is None:
            othersprites = []
        for i in blocks:
            self.objects.append(i)
        for i in entitys:
            self.objects.append(i)
        for i in particles:
            self.objects.append(i)
        for i in othersprites:
            self.objects.append(i)
        self.camera.update()
        self.objects_toblit = self.camera.get_objects(objects=self.objects)
        self.objects_toblit.append(playerentity)
        self.objects = []

    def draw(self, surface):
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        if globs.hard_debug:
            self.surface.blit(scene_test_tx, (0, 0))

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

