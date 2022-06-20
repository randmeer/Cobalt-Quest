import pygame
import pygame.gfxdraw
from pygame.math import Vector2

from octagon.utils import var, img
from octagon.utils.static import tuple_factor, tuple_add, tuple_subtract, hypo, xor, vector_from_points, sign


def rect_to_scene(position, env):
    return position[0] + env.sidelength / 2, position[1] + env.sidelength / 2


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
        self.objects, self.objects_to_blit = [], []
        self.surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.camera = Camera()

        # LIGHTING
        """
        # calculate edge points
        self.edges = []
        size = self.env.envjson["size"] * 2
        blocks = list(self.env.envjson["blocks"])
        for i in range(size + 1):
            for j in range(size + 1):
                count = 0
                block = ()
                if j < size and i < size and blocks[i][j] != 0:  # bottom right
                    count += 1
                    block = (j, i)
                if j > 0 and i < size and blocks[i][j - 1] != 0:  # bottom left
                    count += 1
                    block = (j-1, i)
                if j < size and i > 0 and blocks[i - 1][j] != 0:  # top right
                    count += 1
                    block = (j, i-1)
                if j > 0 and i > 0 and blocks[i - 1][j - 1] != 0:  # top left
                    count += 1
                    block = (j - 1, i - 1)
                if count == 1:
                    self.edges.append([(j, i), block])
        """
    def update(self):
        self.objects = self.env.entities + self.env.projectiles + self.env.melee + self.env.particles
        self.objects.append(self.env.player)
        for i in self.objects:
            i.update()
        self.objects += self.env.blocks
        self.camera.update()
        self.objects_to_blit = self.camera.get_objects(objects=self.objects)
        self.objects = []

    def draw(self, surface):
        if var.hard_debug:
            self.surface.fill((0, 0, 0, 0))
        else:
            self.surface.fill((0, 0, 0, 0), pygame.Rect(
                self.camera.rect.centerx + self.env.sidelength / 2 - self.camera.rect.width / 2,
                self.camera.rect.centery + self.env.sidelength / 2 - self.camera.rect.height / 2,
                self.camera.rect.width, self.camera.rect.height))

        for i in range(3, -1, -1):
            for j in self.objects_to_blit:
                if j.priority == i:
                    j.draw(surface=self.surface)

        # LIGHTING
        """
        player = (self.env.player.hitbox.centerx + self.surface.get_width() / 2, self.env.player.hitbox.centery + self.surface.get_height() / 2)

        important_edges = []

        for i in self.edges:
            edge = tuple_factor(i[0], 16)
            block = tuple_add(tuple_factor(i[1], 16), (8, 8))

            ### DEBUG
            pygame.draw.circle(self.surface, (255, 0, 0), edge, 2)
            pygame.draw.circle(self.surface, (0, 255, 0), block, 2)
            pygame.draw.line(self.surface, (255, 255, 255), edge, block)
            ### DEBUG

            if xor(abs(edge[0]-player[0]) < abs(block[0]-player[0]), abs(edge[1]-player[1]) < abs(block[1]-player[1])) and vector_from_points(edge, player).length() < 100:
                important_edges.append([edge, block])

        for i in important_edges:
            # two points: edge, player
            edge = i[0]
            block = i[1]

            # vector from edge to player:
            delta = vector_from_points(edge, player)

            # unit vector:
            unit = delta.normalize()

            # print(hypo(unit[0], unit[1]))

            stuff = tuple_add(edge, tuple_factor(unit, 100))

            pygame.draw.line(self.surface, (255, 255, 255), edge, stuff)

            third = list(block)
            third[0] += sign(third[0] - edge[0]) * 50
            third[1] += sign(third[1] - edge[1]) * 50

            pygame.gfxdraw.filled_trigon(self.surface, int(edge[0]), int(edge[1]), int(stuff[0]), int(stuff[1]),
                                         int(third[0]), int(third[1]), (255, 0, 0), )

            # pygame.gfxdraw.filled_trigon(self.surface, int(edge[0]), int(edge[1]), int(stuff[0]), int(stuff[1]), int(edge[0]+100), int(edge[1]), (0, 0, 0, 128))
        """

        if var.hard_debug:
            surf = pygame.transform.scale(self.surface, (surface.get_height(), surface.get_height()))
            surface.blit(surf, (0, 0))
        else:
            self.rect.center = (-self.camera.rect.centerx + surface.get_width() / 2, -self.camera.rect.centery + surface.get_height() / 2)
            surface.blit(self.surface, self.rect)
