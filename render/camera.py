import pygame
import QuickJSON
from pygame.surface import Surface
from utils import globs
from render.sprites import block
from render.sprites.entity import player
from utils.images import scene_test_tx

class Camera:
    def __init__(self):
        self.rect = pygame.Rect((0, 0), globs.SIZE)

    def follow(self, target=None):
        if target is None:
            self.rect.center = (0, 0)
        else:
            self.rect.center = target.rect.center

    def get_objects(self, objects=None):
        obj_list = []
        if objects is None:
            objects = []
        for i in objects:
            if i.rect.colliderect(self.rect):
                obj_list.append(i)
                print("colliding rect detected")
        return obj_list


class Scene:
    # def __init__(self, path, flags=None, depth=None, masks=None):
    def __init__(self, path, sidelength):
        # a size 20 floor is 2*20 blocks long, with every block having 16 pixels
        self.surface = None
        self.rect = None
        self.sidelength = sidelength
        self.objects = []
        self.objects_toblit = []

        # self.blocks = []
        # self.entitys = []

        # Surface.__init__(self.sidelength, flags, depth, masks)
        self.camera = Camera()
        print("[Scene Class] initialized class")

    def update(self, player_, blocks=None, entitys=None, ):
        if entitys is None:
            entitys = []
        if blocks is None:
            blocks = []
        for i in blocks:
            self.objects.append(i)
        for i in entitys:
            self.objects.append(i)
        self.camera.follow(target=player_)
        self.objects_toblit = self.camera.get_objects(objects=self.objects)
        print("[Scene Class] loaded scene json")

    def draw(self, surface):
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        self.surface.blit(scene_test_tx, (0, 0))

        pygame.draw.circle(surface=self.surface, color=(255, 255, 0), center=(0, 0), radius=5)

        for i in self.objects_toblit:
            i.draw(surface=self.surface)

        self.rect = self.surface.get_rect()
        self.rect.center = self.camera.rect.center
        surface.blit(self.surface, (self.rect.x+globs.SIZE[0]/2, self.rect.y+globs.SIZE[1]/2))
        #print(self.rect)
        #print("[Scene Class] drew Scene")

