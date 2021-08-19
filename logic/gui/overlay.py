import pygame
import QuickJSON
import os
import shutil

from distutils.dir_util import copy_tree
from utils import globs, play_sound, set_global_defaults, rta_dual, mousepos
from utils.images import overlay_tx, victory_tx, defeat_tx
from render.elements import button, label
from render import gui


def pause_screen(window, background):
    play_sound('click')
    set_global_defaults()

    pause_gui = gui.GUI(background=background, overlay=128, buttons=[
        button.Button(anchor="center", relsize=(0.4, 0.1), text="RESUME", relpos=(0.5, 0.44)),
        button.Button(anchor="center", relsize=(0.4, 0.1), text="BAck TO MENU", relpos=(0.5, 0.62)),
        button.Button(anchor="bottomright", relsize=(0.4, 0.1), text="SETTINGS", relpos=(0.95, 0.95))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if pause_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                    if pause_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.exittomenu = True
                    if pause_gui.buttongroup[2].rect.collidepoint(mp):
                        show_settings(window=window, background=background)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        pause_gui.draw(window=window)
        if globs.exittomenu:
            run = False
    play_sound('click')


def end_screen(window, mainsurf, end):
    # THIS IS OUTDATED WATCH OUT AAAAAAAAA
    set_global_defaults()
    if end == "victory":
        play_sound('victory')
    if end == "defeat":
        play_sound('defeat')
    victory = pygame.transform.scale(victory_tx, (rta_dual(1, 1)))
    defeat = pygame.transform.scale(defeat_tx, (rta_dual(1, 1)))
    overlay = pygame.transform.scale(overlay_tx, (rta_dual(1, 1)))
    buttongroup = pygame.sprite.Group()
    backtomenu_button = button.Button(relsize=(0.9, 0.15), text="Back to Menu", relpos=(0.05, 0.44))
    replay_button = button.Button(relsize=(0.9, 0.15), text="Replay", relpos=(0.05, 0.62))
    buttongroup.add(backtomenu_button, replay_button)
    overlay.set_alpha(2)
    window.blit(overlay, (0, 0))
    main_surface = pygame.Surface(rta_dual(1, 1))
    if end == "victory":
        main_surface.blit(victory, (0, 0))
    elif end == "defeat":
        main_surface.blit(defeat, (0, 0))
    main_surface.set_alpha(20)
    clock = pygame.time.Clock()
    i = 0
    run = True
    while run:
        clock.tick(60)
        mousepos = pygame.mouse.get_pos()
        i += 1
        if i < 32:
            window.blit(main_surface, (0, 0))
            pygame.display.update()
        elif i == 32:
            main_surface.set_alpha(255)
            window.blit(main_surface, (0, 0))
            for x in buttongroup:
                x.update()
                x.draw(window=window)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN and i > 64:
                if event.button == globs.LEFT:
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globs.exittomenu = True
                        globs.exittomenu = True
                    if replay_button.rect.collidepoint(mousepos):
                        run = False
                        globs.dungeon = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.exittomenu = True
        for x in buttongroup:
            x.update()
            x.draw(window=window)
        pygame.display.update()
    play_sound('click')

def show_settings(window, background):
    """
    background should be the current view of the window, not scaled,
    in order for the settings gui to look like it lays on top of the window
    """
    s = True
    while s:
        s = _show_settings(window=window, background=background)


def _show_settings(window, background):
    """
    local function of show_settings
    to re-run this function, call 'return True'
    to exit this function, call 'return False'
    """

    # dear future self, have fun trying to understand this
    set_global_defaults()
    play_sound('click')

    settings = QuickJSON.QJSON("./data/settings.json")
    settings.load()
    saves = os.listdir("./data/savegames")
    labels = []

    # saves tab labels
    for i in range(len(saves)):
        labels.append(label.Label(tags=["saves", "saveslist"], text=saves[i], relpos=(0.05, 0.2+0.05*i+0.02*i+0.1), anchor="topleft", color=globs.GRAYSHADES[2]))
    if len(saves) == 0:
        labels.append(label.Label(tags=["saves", "nosaves"], text="NO SAVES YET", relpos=(0.05, 0.2 + 0.05 * 0 + 0.02 * 0 + 0.1), anchor="topleft", color=globs.GRAYSHADES[1]))
    labels.append(label.Label(tags=["saves", ""], text="SELECT SAVEGAME", relpos=(0.05, 0.2), anchor="topleft", color=globs.GRAYSHADES[0]))
    labels.append(label.Label(tags=["saves", ""], text="CREATE NEW SAVEGAME", relpos=(0.5, 0.2), anchor="topleft", color=globs.GRAYSHADES[0]))
    labels.append(label.Label(tags=["saves", "input"], text="NAME: ", relpos=(0.5, 0.3), anchor="topleft", color=globs.GRAYSHADES[2]))
    labels.append(label.Label(tags=["saves", "create"], text="CREATE", relpos=(0.5, 0.4), anchor="topleft", h_event=True, h_color=globs.GRAYSHADES[4], color=globs.GRAYSHADES[2]))
    labels.append(label.Label(tags=["saves", "delete"], text="DELETE SAVEGAME", relpos=(0.55, 0.6), anchor="topleft", h_event=True, h_color=globs.REDSHADES[3], color=globs.REDSHADES[2]))
    labels.append(label.Label(tags=["saves", "unselect"], text="UNSELECT SAVEGAME", relpos=(0.55, 0.7), anchor="topleft", h_event=True, h_color=globs.GRAYSHADES[2], color=globs.GRAYSHADES[0]))

    # audio tab labels
    labels.append(label.Label(tags=["audio"], text="VOLUME:", relpos=(0.05, 0.2), anchor="topleft"))
    labels.append(label.Label(tags=["audio"], text="BACKGROUND MUSIC:", relpos=(0.05, 0.3), anchor="topleft"))

    # video tab labels
    labels.append(label.Label(tags=["video"], text="RESOLUTION:", relpos=(0.05, 0.2), anchor="topleft"))
    labels.append(label.Label(tags=["video"], text="ASPECT RATIO:", relpos=(0.05, 0.3), anchor="topleft"))
    labels.append(label.Label(tags=["video"], text="PARTICLES:", relpos=(0.05, 0.4), anchor="topleft"))
    labels.append(label.Label(tags=["video"], text="ASPECT RATIO:", relpos=(0.05, 0.3), anchor="topleft"))

    # general tab labels
    labels.append(label.Label(tags=["general"], text="RELOAD SETTINGS GUI", relpos=(0.05, 0.2), anchor="topleft"))

    settings_gui = gui.GUI(background=background, overlay=200, labels=labels, buttons=[
        button.Button(tags=["saves", ""], anchor="center", relsize=(0.2, 0.1), text="SAVES", relpos=(0.15, 0.1)),
        button.Button(tags=["audio", ""], anchor="center", relsize=(0.2, 0.1), text="AUDIO", relpos=(0.3875, 0.1)),
        button.Button(tags=["video", ""], anchor="center", relsize=(0.2, 0.1), text="VIDEO", relpos=(0.6135, 0.1)),
        button.Button(tags=["general", ""], anchor="center", relsize=(0.2, 0.1), text="GENERAL", relpos=(0.85, 0.1)),
        button.Button(tags=["", ""], anchor="bottomright", relsize=(0.4, 0.1), text="SAVE AND RETURN", relpos=(0.95, 0.95))])

    settings_gui.buttongroup[0].set_pressed(press=True)
    for i in settings_gui.labelgroup:
        if i.tags[0] == "saves" and i.text == settings["current_savegame"]:
            i.set_outline(outline=True)
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
        clock.tick(60)
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if settings_gui.buttongroup[4].rect.collidepoint(mp):
                        run = False
                    for i in range(4):
                        if settings_gui.buttongroup[i].rect.collidepoint(mp):
                            for j in range(4):
                                settings_gui.buttongroup[j].set_pressed(press=False)
                            settings_gui.buttongroup[i].set_pressed(press=True)
                            current_tab = settings_gui.buttongroup[i].tags[0]
                            set_current_tab()
                            play_sound('click')
                    # label click events
                    for i in settings_gui.labelgroup:
                        if i.rect.collidepoint(mp):
                            if i.visible:
                                # clicked label is from saves.saveslist
                                if i.tags[0] == "saves" and i.tags[1] == "saveslist":
                                    for j in settings_gui.labelgroup:
                                        if j.tags[0] == "saves" and j.tags[1] == "saveslist":
                                            j.set_outline(outline=False)
                                    i.set_outline(outline=True)
                                    settings["current_savegame"] = i.text
                                    play_sound('click')
                                # clicked label is saves.unselect
                                if i.tags[0] == "saves" and i.tags[1] == "unselect":
                                    settings["current_savegame"] = ""
                                    settings.save()
                                    return True

                                # clicked label is saves.create
                                if i.tags[0] == "saves" and i.tags[1] == "create":
                                    for j in settings_gui.labelgroup:
                                        if j.tags[0] == "saves" and j.tags[1] == "input":
                                            if j.text != "NAME: ":
                                                copy_tree("./resources/savegame_template", f"./data/savegames/{j.text[6:]}")
                                                settings["current_savegame"] = j.text[6:]
                                                settings.save()
                                                alert(window=window, background=settings_gui.get_surface(), message=[f"SUCCESSFULLY CREATED '{j.text[6:]}'."])
                                                return True
                                            else:
                                                alert(window=window, background=settings_gui.get_surface(), message=["PLEASE INPUT A NAME", "FOR YOUR SAVEGAME FIRST"])

                                # clicked label is saves.delete
                                if i.tags[0] == "saves" and i.tags[1] == "delete":
                                    if settings["current_savegame"] == "":
                                        alert(window=window, background=settings_gui.get_surface(), message=["PLEASE SELECT A SAVEGAME FIRST"])
                                    else:
                                        del_bool = alert(window=window, background=settings_gui.get_surface(), question=True, question_keyword="DELETE", message=[f"ARE YOU SURE YOU WANT TO DELETE", f"THE SAVEGAME '{settings['current_savegame']}'"])
                                        if del_bool:
                                            shutil.rmtree(f"./data/savegames/{settings['current_savegame']}")
                                            settings["current_savegame"] = ""
                                            settings.save()
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

    settings.save()
    play_sound('click')
    return False


def alert(window, background, message, color=(0, 0, 0), question=False, question_keyword="OK"):
    set_global_defaults()
    play_sound('alert')
    labels = []
    buttons = []
    for i in range(len(message)):
        labels.append(label.Label(text=message[i], relpos=(0.5, 0.1*i+0.5-0.1*len(message)), anchor="center"))

    if question:
        buttons.append(button.Button(anchor="center", relsize=(0.2, 0.1), text=question_keyword, relpos=(0.35, 0.6)))
        buttons.append(button.Button(anchor="center", relsize=(0.2, 0.1), text="CANCEL", relpos=(0.65, 0.6)))
    else:
        buttons.append(button.Button(anchor="center", relsize=(0.1, 0.1), text="OK", relpos=(0.5, 0.6)))

    alert_gui = gui.GUI(background=background, overlay=200, labels=labels, overlaycolor=color, buttons=buttons)
    alert_gui.draw(window=window)
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if alert_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        if question:
                            play_sound('click')
                            return True
                    if question:
                        if alert_gui.buttongroup[1].rect.collidepoint(mp):
                            play_sound('click')
                            return False
        alert_gui.draw(window=window)
    play_sound('click')
