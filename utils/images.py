import os
import pygame

tex_dir = './resources/textures/'

pygame.display.init()

images = {}

for i in os.listdir(tex_dir):
    splitup = os.path.splitext(i)
    if splitup[1] == ".png":
        img = pygame.image.load(tex_dir + i).convert_alpha()
        images[splitup[0]] = img

for i in images:
    print(i)


background_dungeon_tx = {
    "northern_plains": pygame.image.load(tex_dir + "bg_dg_northern_plains.png").convert_alpha(),
    "southern_plains": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "tundra": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "meadow": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "snowy_tundra": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "desert": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "mushroom_island": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "steppe": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "ocean": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "volcano_island": pygame.image.load(tex_dir + "background.png").convert_alpha()
}

map_dungeon_tx = {
    "northern_plains": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "southern_plains": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "tundra": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "meadow": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "snowy_tundra": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "desert": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "mushroom_island": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "steppe": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "ocean": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
    "volcano_island": {
        0: images["map_dg_northern_plains"],
        1: images["map_dg_northern_plains"],
        2: images["map_dg_northern_plains"],
    },
}

block_tx = {
    1: images["cobblestone"],
    2: images["stone_bricks"]
}

item_ol = {
    "weapon": images["weapon"],
    "armor": images["armor"],
    "tool": images["tool"],
    "food": images["food"],
    "orb": images["orb"],
    "unset": images["overlay_empty"]
}

overlays = {}
for i in item_ol:
    img = item_ol[i]
    img.set_alpha(150)
    h_img = img.copy()
    h_img.set_alpha(200)
    overlays[i] = img, h_img

item_tx = {
    "dagger": images["dagger"],
    "katana": images["cross"],            # X
    "bow": images["bow"],
    "shuriken": images["shuriken"],
    "arrow": images["arrow"],
    "unset": None,
    "rande": images["rande"]
}
