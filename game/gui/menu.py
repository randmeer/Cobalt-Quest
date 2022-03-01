import pygame

from octagon.utils import mp_screen, play_sound, get_setting, var
from octagon.utils import img
from octagon.gui import button, image, label
from octagon import gui

from game import globs
from game.gui.overlay import show_settings, alert, show_inventory, stats


def show_menu(window):
    globs.set_global_defaults()

    menu_gui = gui.GUI(
        background=img.misc["background"]["menu"], overlay=160,
        buttons=[
            button.Button(tags=["map"], anchor="topleft", relsize=(0.264, 0.1), text="MAP", relpos=(0.225, 0.40)),
            button.Button(tags=["shop"], anchor="topright", relsize=(0.264, 0.1), text="SHOP", relpos=(0.775, 0.40)),
            button.Button(tags=["inventory"], anchor="topleft", relsize=(0.34, 0.1), text="INVENTORY", relpos=(0.225, 0.525)),
            button.Button(tags=["stats"], anchor="topright", relsize=(0.19, 0.1), text="STATS", relpos=(0.775, 0.525)),
            button.Button(tags=["settings"], anchor="topleft", relsize=(0.413, 0.1), text="SETTINGS", relpos=(0.225, 0.65)),
            button.Button(tags=["unset2"], anchor="topright", relsize=(0.116, 0.1), text="?", relpos=(0.775, 0.65))],
        images=[
            image.Image(relpos=(0.5, 0.2), anchor="center", image=img.misc["logo"])],
        labels=[
            label.Label(text=f"VERSION {globs.VERSION}", relpos=(0.01, 0.98), anchor="bottomleft", color=(12, 18, 26)),
            label.Label(text="RANDE STUDIOS", relpos=(0.01, 0.94), anchor="bottomleft", color=(12, 18, 26))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    for i in menu_gui.buttongroup:
                        if i.rect.collidepoint(mp):
                            if i.tags[0] == "map":
                                if get_setting("current_savegame") == "":
                                    alert(window, menu_gui.get_surface(), ["PLEASE SELECT A SAVEGAME FIRST"])
                                else:
                                    run = False
                                    globs.map = True
                            if i.tags[0] == "shop":
                                alert(window, menu_gui.get_surface(), ["THE SHOP IS NOT AVAILABLE YET"])
                            if i.tags[0] == "inventory":
                                if get_setting("current_savegame") == "":
                                    alert(window, menu_gui.get_surface(), ["PLEASE SELECT A SAVEGAME FIRST"])
                                else:
                                    show_inventory(window=window, background=img.misc["background"]["menu"])
                            if i.tags[0] == "settings":
                                show_settings(window=window, background=img.misc["background"]["menu"])
                            if i.tags[0] == "stats":
                                stats(window=window, background=img.misc["background"]["menu"])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.titlescreen = True
        if globs.quitgame:
            run = False
        if run:
            menu_gui.draw(window=window)
    play_sound('click')
