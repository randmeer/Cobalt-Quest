import pygame

from octagon.utils import var


class Camera:
    def __init__(self):
        self.rect = pygame.Rect((0, 0), var.SIZE)
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
        if var.render_all:
            return objects
        else:
            for i in objects:
                if i.rect.colliderect(self.rect):
                    obj_list.append(i)
            return obj_list


class Scene:
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
        for i in self.objects:
            i.update()
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
        else:
            self.rect.center = (-self.camera.rect.centerx+surface.get_width()/2, -self.camera.rect.centery+surface.get_height()/2)
            surface.blit(self.surface, self.rect)

