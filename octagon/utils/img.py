import os
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
