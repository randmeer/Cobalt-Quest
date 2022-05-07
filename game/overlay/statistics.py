import pygame

from octagon.utils import mp_screen, get_setting, get_inventory, var, play_sound
from octagon.gui import button, label
from octagon import gui

from game import globs


def stats(window, background):
    globs.set_global_defaults()
    play_sound('click')
    stats_gui = gui.GUI(background=background, overlay=192, buttons=[
        button.Button(tags=["return"], anchor="bottomleft", relsize=(0.4, 0.1), text="SAVE AND RETURN", relpos=(0.05, 0.95))], labels=[
        label.Label(tags=["title"], text=f"STATISTICS FOR SAVEGAME [{get_setting('current_savegame')}]:", relpos=(0.05, 0.05), anchor="topleft"),
        label.Label(tags=["deaths"], text=f"DEATHS: {get_inventory('deaths')}", relpos=(0.05, 0.15), anchor="topleft")
    ])
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
                    for i in stats_gui.buttongroup:
                        if i.rect.collidepoint(mp):
                            if i.tags[0] == "return":
                                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        stats_gui.draw(window=window)
    play_sound('click')
