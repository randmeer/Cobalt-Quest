import pygame
import os
from distutils.dir_util import copy_tree
from shutil import rmtree
from octagon.utils import img, var, get_setting, set_setting, mp_screen, play_sound, save_settings
from octagon.gui import label, button, GUI

from game import globs
from game.overlay.alert import Alert


# TODO: rework as OOP

def show_saves(window, background):
    """
    background should be the current view of the window, not scaled,
    in order for the settings gui to look like it lays on top of the window
    """
    s = True
    while s:
        s = _show_saves(window=window, background=background)


def _show_saves(window, background):
    """
    local function of show_settings
    to re-run this function, call 'return True'
    to exit this function, call 'return False'
    """

    # dear future self, have fun trying to understand this
    play_sound('click')

    saves = os.listdir("./data/savegames")
    labels = []

    # saves tab labels
    for i in range(len(saves)):
        labels.append(label.Label(tags=["saves", "saveslist"], text=saves[i], relpos=(0.05, 0.2+0.05*i+0.02*i+0.1), anchor="topleft", color=var.GRAYSHADES[2]))
    if len(saves) == 0:
        labels.append(label.Label(tags=["saves", "nosaves"], text="NO SAVES YET", relpos=(0.05, 0.2 + 0.05 * 0 + 0.02 * 0 + 0.1), anchor="topleft", color=var.GRAYSHADES[1]))
    labels.append(label.Label(tags=["saves", ""], text="SELECT SAVEGAME", relpos=(0.05, 0.2), anchor="topleft", color=var.GRAYSHADES[0]))
    labels.append(label.Label(tags=["saves", ""], text="CREATE NEW SAVEGAME", relpos=(0.5, 0.2), anchor="topleft", color=var.GRAYSHADES[0]))
    labels.append(label.Label(tags=["saves", "input"], text="NAME: ", relpos=(0.5, 0.3), anchor="topleft", color=var.GRAYSHADES[2]))
    labels.append(label.Label(tags=["saves", "create"], text="CREATE", relpos=(0.5, 0.4), anchor="topleft", h_event=True, h_color=var.GRAYSHADES[4], color=var.GRAYSHADES[2]))
    labels.append(label.Label(tags=["saves", "delete"], text="DELETE SAVEGAME", relpos=(0.55, 0.6), anchor="topleft", h_event=True, h_color=var.REDSHADES[3], color=var.REDSHADES[2]))
    labels.append(label.Label(tags=["saves", "unselect"], text="UNSELECT SAVEGAME", relpos=(0.55, 0.7), anchor="topleft", h_event=True, h_color=var.GRAYSHADES[2], color=var.GRAYSHADES[0]))


    settings_gui = GUI(background=background, overlay=200, labels=labels, buttons=[
        button.Button(tags=["saves", ""], anchor="center", relsize=(0.2, 0.1), text="SAVES", relpos=(0.15, 0.1)),
        button.Button(tags=["", ""], anchor="topleft", relsize=(0.35, 0.09), text="SAVE AND RETURN", relpos=(0.6, 0.85))])

    for i in settings_gui.labelgroup:
        if i.tags[0] == "saves" and i.tags[1] == "saveslist":
            i.render_outline()
        elif i.tags[0] == "video" and i.tags[1] == "packlist":
            i.render_outline()

    for i in settings_gui.labelgroup:
        if i.tags[0] == "saves" and i.text == get_setting("current_savegame"):
            i.set_outline(outline=True)
        elif i.tags[0] == "video" and i.text == get_setting("resourcepack"):
            i.set_outline(outline=True)

    settings_gui.buttongroup[0].set_pressed(press=True)
    current_tab = "saves"

    def set_current_tab():
        for i in settings_gui.labelgroup:
            i.set_visible(visible=True)
            if i.tags[0] != current_tab:
                i.set_visible(visible=False)
    set_current_tab()

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    if settings_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False

                    # button click events
                    # for i in range(4):
                    #     if settings_gui.buttongroup[i].rect.collidepoint(mp):
                    #         for j in range(4):
                    #             settings_gui.buttongroup[j].set_pressed(press=False)
                    #         settings_gui.buttongroup[i].set_pressed(press=True)
                    #         current_tab = settings_gui.buttongroup[i].tags[0]
                    #         set_current_tab()
                    #         play_sound('click')

                    # label click events
                    for i in settings_gui.labelgroup:
                        if i.rect.collidepoint(mp) and i.visible:

                            # clicked label is from saves.saveslist
                            if i.tags[0] == "saves" and i.tags[1] == "saveslist":
                                for j in settings_gui.labelgroup:
                                    if j.tags[0] == "saves" and j.tags[1] == "saveslist":
                                        j.set_outline(outline=False)
                                i.set_outline(outline=True)
                                set_setting("current_savegame", i.text)
                                play_sound('click')

                            # clicked label is saves.unselect
                            if i.tags[0] == "saves" and i.tags[1] == "unselect":
                                set_setting('current_savegame', "")
                                return True

                            # clicked label is saves.create
                            if i.tags[0] == "saves" and i.tags[1] == "create":
                                for j in settings_gui.labelgroup:
                                    if j.tags[0] == "saves" and j.tags[1] == "input":
                                        if j.text != "NAME: ":
                                            copy_tree("./resources/savegame", f"./data/savegames/{j.text[6:]}")
                                            set_setting('current_savegame', j.text[6:])
                                            alert(window=window, background=settings_gui.get_surface(), message=[f"SUCCESSFULLY CREATED '{j.text[6:]}'."])
                                            return True
                                        else:
                                            alert(window=window, background=settings_gui.get_surface(), message=["PLEASE INPUT A NAME", "FOR YOUR SAVEGAME FIRST"])

                            # clicked label is saves.delete
                            if i.tags[0] == "saves" and i.tags[1] == "delete":
                                if get_setting("current_savegame") == "":
                                    alert(window=window, background=settings_gui.get_surface(), message=["PLEASE SELECT A SAVEGAME FIRST"])
                                else:
                                    del_bool = alert(window=window, background=settings_gui.get_surface(), question=True, question_keyword="DELETE", message=[f"ARE YOU SURE YOU WANT TO DELETE", f"THE SAVEGAME '{get_setting('current_savegame')}'"])
                                    if del_bool:
                                        rmtree(f"./data/savegames/{get_setting('current_savegame')}")
                                        set_setting("current_savegame", "")
                                        return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                for i in settings_gui.labelgroup:
                    if i.tags[0] == "saves" and i.tags[1] == "input":
                        if i.visible:
                            key_str = pygame.key.name(event.key)
                            i.text_input(key_str=key_str, fix_chars=6, max_chars=16)
        if globs.quitgame:
            run = False
        if run:
            settings_gui.draw(window=window)

    save_settings()
    play_sound('click')
    return False
