import pygame
import pygame.gfxdraw

from octagon.utils import var, img, render_text


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

    def convert_debug(self, position):
        return position[0] + self.env.sidelength//2, position[1] + self.env.sidelength//2

    def convert(self, position):
        return position[0] - self.env.player.rect.center[0] + var.SIZE[0]//2, position[1] - self.env.player.rect.center[1] + var.SIZE[1]//2

    def __init__(self, env):
        self.env = env
        self.debug_surface, rect = None, None
        self.sidelength = env.sidelength
        self.objects, self.objects_toblit = [], []
        self.debug_surface = pygame.Surface((self.sidelength, self.sidelength), pygame.SRCALPHA)
        self.light_surface = pygame.Surface(var.SIZE, pygame.SRCALPHA)
        self.do_lighting = False
        self.camera = Camera()
        self.env.surface = self.debug_surface.subsurface(self.camera.rect)

    def update(self):
        self.objects = self.env.entities + self.env.projectiles + self.env.melee + self.env.particles
        self.objects.append(self.env.player)
        for i in self.objects:
            i.update()
        self.objects += self.env.blocks
        self.camera.update()
        self.objects_toblit = self.camera.get_objects(objects=self.objects)
        self.objects = []

    def render_objects(self, surface, coordinate_conversion):
        for i in range(3, -1, -1):
            for j in self.objects_toblit:
                if j.priority == i:
                    j.draw(surface, coordinate_conversion)

    def render_background(self, surface, coordinate_conversion):
        x, y = self.camera.rect.center
        x -= var.SIZE[0] // 2
        y -= var.SIZE[1] // 2
        x = var.SIZE[0] * (x // var.SIZE[0])
        y = var.SIZE[1] * (y // var.SIZE[1])
        posx, posy = coordinate_conversion((x, y))
        surface.blit(img.misc["background"]["game"], (posx, posy))
        surface.blit(img.misc["background"]["game"], (posx, posy + 144))
        surface.blit(img.misc["background"]["game"], (posx + 256, posy))
        surface.blit(img.misc["background"]["game"], (posx + 256, posy + 144))

    def render_lighting(self, surface):
        if not self.do_lighting:
            return
        surface.blit(self.light_surface, (0, 0))
        self.light_surface.fill((0, 0, 0, 128))

    def light_point(self, position, size, coordinate_conversion):
        if not self.do_lighting:
            return
        gradient = pygame.transform.scale(img.misc["radial_gradient"], size)
        rect = gradient.get_rect()
        rect.center = position
        self.light_surface.blit(gradient, coordinate_conversion(rect.topleft), special_flags=pygame.BLEND_RGBA_SUB)

    def render_camera(self, surface):
        # background
        self.render_background(surface, self.convert)

        # objects
        self.render_objects(surface, self.convert)

        # lighting
        self.render_lighting(surface)

    def draw(self, surface):
        if var.debug_scene:
            self.debug_surface.fill((0, 0, 0))
            self.render_background(self.debug_surface, self.convert_debug)

            # objects
            self.render_objects(self.debug_surface, self.convert_debug)

            # draw debug subsurface
            surface.fill((0, 0, 0))
            subsurface_surf = pygame.Surface(var.SIZE, pygame.SRCALPHA)
            subsurface_surf.blit(self.debug_surface, (0 - self.camera.rect.topleft[0] - self.env.sidelength//2, 0 - self.camera.rect.topleft[1] - self.env.sidelength//2))
            surface.blit(subsurface_surf, (surface.get_height() + 20, 20))
            render_text(window=surface, text="DEBUG SUBSURFACE", pos=(surface.get_height() + 20, var.SIZE[1] + 20), color=var.WHITE, size=20)

            # draw camera view
            camera_surf = pygame.Surface(var.SIZE, pygame.SRCALPHA)
            self.render_camera(camera_surf)
            surface.blit(camera_surf, (surface.get_height()+20, var.SIZE[1]+50))
            render_text(window=surface, text="CAMERA RENDER", pos=(surface.get_height()+20, var.SIZE[1]*2 + 50), color=var.WHITE, size=20)

            # check if surfaces match
            match = True
            if subsurface_surf.get_size() != camera_surf.get_size():
                match = False
            else:
                for i in range(camera_surf.get_width()):
                    for j in range(camera_surf.get_height()):
                        if subsurface_surf.get_at((i, j)) != camera_surf.get_at((i, j)):
                            match = False
            render_text(window=surface, text="SURFACES MATCH: " + str(match), pos=(surface.get_height()+20, surface.get_height()-40), color=var.WHITE, size=20)

            # display debug information
            render_text(window=surface, text="RENDER_ALL: " + str(var.render_all), pos=(surface.get_height()+20, surface.get_height()-120), color=var.WHITE, size=20)
            render_text(window=surface, text="SOFT_DEBUG: " + str(var.show_hitboxes), pos=(surface.get_height() + 20, surface.get_height() - 160), color=var.WHITE, size=20)
            render_text(window=surface, text="DO_LIGHTING: " + str(self.do_lighting), pos=(surface.get_height()+20, surface.get_height()-200), color=var.WHITE, size=20)

            # draw camera edges
            pygame.draw.polygon(self.debug_surface, var.WHITE, [self.convert_debug(self.camera.rect.topleft), self.convert_debug(self.camera.rect.bottomleft),
                                                                self.convert_debug(self.camera.rect.bottomright), self.convert_debug(self.camera.rect.topright)], 1)

            # draw debug surface
            surf = pygame.transform.scale(self.debug_surface, (surface.get_height(), surface.get_height()))
            surface.blit(surf, (0, 0))

        else:
            self.render_camera(surface)
