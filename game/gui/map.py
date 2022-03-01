import pygame

from octagon.utils import mp_screen, play_sound, img
from octagon.gui import button, image
from octagon import gui
from octagon.utils.texture import Texture

from game import globs


def show_map(window):
    globs.set_global_defaults()

    # TODO: make the map's dungeons clickable
    # create the lvl buttons and use a uneccessary complicated alorithm to align them in a 3x3 grid
    levelbuttons = []
    lvlrelposy = 0.23
    for i in range(9):
        lvlrelposx = 0.05 + 0.31 * (i - ((int(i / 3)) * 3))
        if i == 3 or i == 6:
            lvlrelposy += 0.25
        levelbutton = button.Button(relsize=(0.28, 0.22), text=f"LVL {i}", relpos=(lvlrelposx, lvlrelposy))
        levelbuttons.append(levelbutton)

    map = Texture(img.misc["map"]["map"], 0.1)
    map_gui = gui.GUI(background=img.misc["map"]["northern_plains"], overlay=160, buttons=[
        button.Button(anchor="topleft", relsize=(0.4, 0.1), text="BACK TO MENU", relpos=(0.05, 0.05)), levelbuttons[0]], images=[
        image.Image(image=map.get(), anchor="center", relpos=(0.5, 0.5))])

    clock = pygame.time.Clock()
    run = True
    selected_rect = None

    # main game loop
    while run:
        clock.tick(60)
        mp = mp_screen()
        map_gui.imagegroup[0].image = map.get()
        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            # mouse event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if map_gui.imagegroup[0].rect.collidepoint(mp):
                        selected_rect = map_gui.imagegroup[0].rect
                        offset = (mp_screen()[0] - selected_rect.topleft[0],
                                  mp_screen()[1] - selected_rect.topleft[1])
                    if map_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.menu = True
                    if map_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.dungeon = True
                        globs.dungeon_str = "northern_plains"
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected_rect = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_rect:
                    selected_rect.topleft = (mp_screen()[0] - offset[0], mp_screen()[1] - offset[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.menu = True
        map_gui.draw(window=window)
    play_sound('click')
