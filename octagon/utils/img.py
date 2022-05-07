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
particles = {}


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
    global particles
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
    particles = QuickJSON.QJSON(f"./resources/resourcepacks/{get_setting('resourcepack')}/particles.json")
    particles.load()


load()

blockcode = {
    1: "cobblestone",
    2: "stone_bricks"
}


class Texture:
    def __init__(self, image, frametime, single_run=False, set_height=False):
        self.init_time = time.time()
        self.default_time = frametime
        self.single_run = single_run
        self.iterations = 0
        self.image = None
        self.img_str = image
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
            self.images = [self.image.subsurface((0, self.seth_value * i, self.width, self.seth_value)) for i in range(self.frame_count)]
        else:
            self.images = [self.image.subsurface((0, self.width * i, self.width, self.width)) for i in range(self.frame_count)]

        self.frame_list = [{"index": i, "time": self.default_time} for i in range(self.frame_count)]

    def get(self):
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