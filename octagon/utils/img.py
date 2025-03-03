import os
import time

import pygame
import QuickJSON

from octagon.utils import get_setting

pygame.display.init()

entity = {}
block = {}
item = {}
misc = {}
particle_json = {}
block_json = {}


def _load(path):
    imgdict = {}
    tex_dir = './resources/resourcepacks/' + get_setting('resourcepack') + path
    for i in os.listdir(tex_dir):
        splitup = os.path.splitext(i)
        if os.path.isdir(tex_dir + "/" + str(i) + "/"):
            imgdict[i] = _load(path + i + "/")
        elif splitup[1] == ".png":
            img = pygame.image.load(tex_dir + i).convert_alpha()
            imgdict[splitup[0]] = img
    return imgdict


def load():
    global entity
    global block
    global item
    global misc
    global particle_json
    global block_json
    entity = _load("/entity/")
    block = _load("/block/")
    item = _load("/item/")
    misc = _load("/misc/")
    for i in misc["inventory"]:
        o_img = misc["inventory"][i]
        o_img.set_alpha(150)
        h_img = o_img.copy()
        h_img.set_alpha(200)
        misc["inventory"][i] = o_img, h_img
    particle_json = QuickJSON.QJSON(f"./resources/resourcepacks/{get_setting('resourcepack')}/particles.json")
    particle_json.load()
    block_json = QuickJSON.QJSON(f"./resources/resourcepacks/{get_setting('resourcepack')}/blocks.json")
    block_json.load()


load()

blockname = {
    1: "cobblestone",
    2: "stone_brick",
    3: "torch",

}

"""
block texturing process
+------------+-------------------------------+-------------------+-----------------------+-------------------+
|neighbors   |   bit-array                   |              int  |   lookup table        |   texture index   |
|            |                               |                   |                       |                   |
|0 1 1       |                               |                   |                       |                   |
|0 x 0       |   [0, 1, 1, 0, 1, 1, 1, 0]    |   110             |   blockalign[110]     |   2               |
|1 1 1       |                               |                   |                       |                   |
+------------+-------------------------------+-------------------+-----------------------+-------------------+
"""

blockalign = [1, 5, 1, 5, 7, 13, 7, 9, 1, 5, 1, 5, 7, 13, 7, 9, 4, 3, 4, 3, 12, 31, 12, 24, 4, 3, 4, 3, 8, 25, 8, 19, 1,
              5, 1, 5, 7, 13, 7, 9, 1, 5, 1, 5, 7, 13, 7, 9, 4, 3, 4, 3, 12, 31, 12, 24, 4, 3, 4, 3, 8, 25, 8, 19, 6,
              15, 6, 15, 2, 29, 2, 23, 6, 15, 6, 15, 2, 29, 2, 23, 14, 30, 14, 30, 28, 46, 28, 44, 14, 30, 14, 30, 20,
              45, 20, 39, 6, 15, 6, 15, 2, 29, 2, 23, 6, 15, 6, 15, 2, 29, 2, 23, 10, 27, 10, 27, 21, 43, 21, 41, 10,
              27, 10, 27, 16, 37, 16, 35, 1, 5, 1, 5, 7, 13, 7, 9, 1, 5, 1, 5, 7, 13, 7, 9, 4, 3, 4, 3, 12, 31, 12, 24,
              4, 3, 4, 3, 8, 25, 8, 19, 1, 5, 1, 5, 7, 13, 7, 9, 1, 5, 1, 5, 7, 13, 7, 9, 4, 3, 4, 3, 12, 31, 12, 24,
              4, 3, 4, 3, 8, 25, 8, 19, 6, 11, 6, 11, 2, 22, 2, 17, 6, 11, 6, 11, 2, 22, 2, 17, 14, 26, 14, 26, 28, 42,
              28, 36, 14, 26, 14, 26, 20, 40, 20, 34, 6, 11, 6, 11, 2, 22, 2, 17, 6, 11, 6, 11, 2, 22, 2, 17, 10, 18,
              10, 18, 21, 38, 21, 32, 10, 18, 10, 18, 16, 33, 16, 0]


def get_neighbors(blockgrid, blockpos):
    inp = [0, 0, 0, 0, 0, 0, 0, 0]
    i = blockpos[0]
    j = blockpos[1]
    center = blockgrid[i][j]
    l = len(blockgrid[0]) - 1
    if i != 0 and j != 0 and blockgrid[i - 1][j - 1] == center:
        inp[0] = 1
    if i != 0 and blockgrid[i - 1][j] == center:
        inp[1] = 1
    if i != 0 and j != l and blockgrid[i - 1][j + 1] == center:
        inp[2] = 1
    if j != l and blockgrid[i][j + 1] == center:
        inp[3] = 1
    if i != l and j != l and blockgrid[i + 1][j + 1] == center:
        inp[4] = 1
    if i != l and blockgrid[i + 1][j] == center:
        inp[5] = 1
    if i != l and j != 0 and blockgrid[i + 1][j - 1] == center:
        inp[6] = 1
    if j != 0 and blockgrid[i][j - 1] == center:
        inp[7] = 1
    return inp


class BlockTexture:
    def __init__(self, blockgrid, blockpos, frametime=0.2):
        self.blockcode = blockgrid[blockpos[0]][blockpos[1]]
        self.name = blockname[self.blockcode]
        self.image = block[self.name].copy()
        surface = pygame.Surface((16, self.image.get_height()), pygame.SRCALPHA)

        if block_json[self.name][1] or block_json[self.name][2]:
            neighbors = get_neighbors(blockgrid, blockpos)
            neighbors_int = sum(j << i for i, j in enumerate(reversed(neighbors)))
            self.align = blockalign[neighbors_int]

        if block_json[self.name][1]:
            # surface.blit(self.image, (0, 0))
            for i in range(self.image.get_height() // 16):
                temp = pygame.Surface((16, 16), pygame.SRCALPHA)
                temp.blit(self.image, (-self.align * 16, i * 16))
                surface.blit(temp, (0, i * 16))
        else:
            surface = self.image

        if block_json[self.name][2] is not False:
            # overlay = block["block_overlay"].copy()
            # pygame.transform.threshold(dest_surface=overlay, surface=block["block_overlay"], \
            #       search_color=(0, 0, 0, 255), threshold=(0, 0, 0, 0), set_color=[255, 0, 0])

            var = pygame.PixelArray(block["block_overlay"])
            var.replace((0, 0, 0), tuple(block_json[self.name][2]))
            del var
            for i in range(surface.get_height() // 16):
                surface.blit(block["block_overlay"], (-self.align*16, i * 16))

        self.texture = Texture(surface, frametime, False, 16)

    def get(self):
        return self.texture.get()


class Texture:
    def __init__(self, image, frametime, single_run=False, set_height=False):
        self.init_time = time.time()
        self.default_time = frametime
        self.single_run = single_run
        self.iterations = 0
        self.image = None
        self.stop = False
        self.seth_bool = False
        if set_height:
            self.seth_bool = True
            self.seth_value = set_height

        self.image = image
        self.height, self.width = self.image.get_height(), self.image.get_width()

        if self.seth_bool:
            self.frame_count = self.height // self.seth_value
        else:
            self.frame_count = self.height // self.width

        self.single_loop_time = self.frame_count * self.default_time

        if self.seth_bool:
            self.images = [self.image.subsurface((0, self.seth_value * i, self.width, self.seth_value)) for i in
                           range(self.frame_count)]
        else:
            self.images = [self.image.subsurface((0, self.width * i, self.width, self.width)) for i in
                           range(self.frame_count)]

        self.frame_list = [{"index": i, "time": self.default_time} for i in range(self.frame_count)]

    def get(self):
        if self.frame_count == 1:
            return self.images[0]
        if self.stop:
            return False
        now = time.time()
        delta_time = now - self.init_time
        delta_time %= self.single_loop_time

        for i in range(len(self.frame_list)):
            if delta_time - self.frame_list[i]['time'] <= 0:
                if self.single_run:
                    iters = self.iterations
                    self.iterations = i
                    if i < iters:
                        self.stop = True
                        return False
                return self.images[self.frame_list[i]['index']]
            delta_time -= self.frame_list[i]['time']
