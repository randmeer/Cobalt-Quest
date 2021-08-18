import pygame
import QuickJSON
import os

from distutils.dir_util import copy_tree
from utils import globs, play_sound, set_global_defaults, rta_dual, mousepos
from utils.images import overlay_tx, victory_tx, defeat_tx
from render.elements import button, label
from render import gui


def pause_screen(window, background):
    play_sound('click')
    set_global_defaults()

    pause_gui = gui.GUI(background=background, overlay=128, buttons=[
        button.Button(anchor="center", relwidth=0.4, relheight=0.1, text="RESUME", relpos=(0.5, 0.44)),
        button.Button(anchor="center", relwidth=0.4, relheight=0.1, text="BAck TO MENU", relpos=(0.5, 0.62)),
        button.Button(anchor="bottomright", relwidth=0.4, relheight=0.1, text="SETTINGS", relpos=(0.95, 0.95))])

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
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, text="Back to Menu", relpos=(0.05, 0.44))
    replay_button = button.Button(relwidth=0.9, relheight=0.15, text="Replay", relpos=(0.05, 0.62))
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
    set_global_defaults()
    play_sound('click')

    settings = QuickJSON.QJSON("./data/settings.json")
    settings.load()
    saves = os.listdir("./data/savegames")

    #
    labels = []

    # saves tab labels
    for i in range(len(saves)):
        labels.append(label.Label(tags=["saves", "saveslist"], text=saves[i], relpos=(0.05, 0.2+0.05*i+0.02*i+0.1), anchor="topleft", color=globs.GRAYSHADES[1]))
    labels.append(label.Label(tags=["saves", ""], text="SELECT SAVEGAME", relpos=(0.05, 0.2), anchor="topleft"))
    labels.append(label.Label(tags=["saves", "createbutton"], text="CREATE NEW SAVEGAME", relpos=(0.5, 0.2), anchor="topleft", hoverevent=True, hovercolor=globs.GRAYSHADES[1]))
    labels.append(label.Label(tags=["saves", "create", "input"], text="NAME: ", relpos=(0.5, 0.3), anchor="topleft", color=globs.GRAYSHADES[1], visible=False))
    labels.append(label.Label(tags=["saves", "create", "savebutton"], text="CREATE", relpos=(0.5, 0.4), anchor="topleft", hoverevent=True, hovercolor=globs.GRAYSHADES[1], visible=False))

    # audio tab labels

    # video tab labels

    settings_gui = gui.GUI(background=background, overlay=128, labels=labels, buttons=[
        button.Button(anchor="center", relwidth=0.2, relheight=0.1, text="SAVES", relpos=(0.15, 0.1)),
        button.Button(anchor="center", relwidth=0.2, relheight=0.1, text="AUDIO", relpos=(0.3875, 0.1)),
        button.Button(anchor="center", relwidth=0.2, relheight=0.1, text="VIDEO", relpos=(0.6135, 0.1)),
        button.Button(anchor="center", relwidth=0.2, relheight=0.1, text="TAB XY", relpos=(0.85, 0.1)),
        button.Button(anchor="bottomright", relwidth=0.4, relheight=0.1, text="SAVE AND RETURN", relpos=(0.95, 0.95))])

    settings_gui.buttongroup[0].set_pressed(press=True)
    for i in settings_gui.labelgroup:
        if i.tags[0] == "saves" and i.text == settings["current_savegame"]:
            i.set_outline(outline=True)
    current_tab = "SAVES"

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
                    if settings_gui.buttongroup[4].rect.collidepoint(mp):
                        run = False
                    for i in range(4):
                        if settings_gui.buttongroup[i].rect.collidepoint(mp):
                            for j in range(4):
                                settings_gui.buttongroup[j].set_pressed(press=False)
                            settings_gui.buttongroup[i].set_pressed(press=True)
                            current_tab = settings_gui.buttongroup[i].text.lower()
                            for j in settings_gui.labelgroup:
                                j.set_visible(visible=True)
                                if j.tags[0] != current_tab:
                                    j.set_visible(visible=False)
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
                                # clicked label is saves.createbutton
                                if i.tags[0] == "saves" and i.tags[1] == "createbutton":
                                    for j in settings_gui.labelgroup:
                                        if j.tags[0] == "saves" and j.tags[1] == "create":
                                            j.set_visible(visible=True)
                                    play_sound('click')
                                # clicked label is saves.create.savebutton
                                if i.tags[0] == "saves" and i.tags[1] == "create" and i.tags[2] == "savebutton":
                                    print("savebutton")
                                    for j in settings_gui.labelgroup:
                                        if j.tags[0] == "saves" and j.tags[1] == "create" and j.tags[2] == "input":
                                            if j.text != "NAME: ":
                                                copy_tree("./resources/dungeons", f"./data/savegames/{j.text[6:]}")
                                                settings["current_savegame"] = j.text[6:]
                                                settings.save()
                                                alert(window=window, background=settings_gui.get_surface(), message=[f"SUCCESSFULLY CREATED '{j.text[6:]}'.", "RE-ENTER SETTINGS TO", "SEE YOUR NEW SAVES LIST"])
                                                run = False
                                                show_settings(window=window, background=background)
                                            else:
                                                alert(window=window, background=settings_gui.get_surface(), message=["PLEASE INPUT A NAME FOR YOUR SAVEGAME"])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                for i in settings_gui.labelgroup:
                    if i.tags[0] == "saves" and i.tags[1] == "create" and i.tags[2] == "input":
                        if i.visible:
                            key_str = pygame.key.name(event.key)
                            i.text_input(key_str=key_str, fix_chars=6, max_chars=16)
        if run:
            settings_gui.draw(window=window)

    settings.save()
    play_sound('click')


def alert(window, background, message, color=(0, 0, 0)):
    set_global_defaults()
    play_sound('alert')
    labels = []
    for i in range(len(message)):
        labels.append(label.Label(text=message[i], relpos=(0.5, 0.1*i+0.4-0.1*len(message)), anchor="center"))

    alert_gui = gui.GUI(background=background, overlay=200, labels=labels, overlaycolor=color,
                        buttons=[button.Button(anchor="center", relwidth=0.1, relheight=0.1, text="OK", relpos=(0.5, 0.6))])
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
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if alert_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
    play_sound('click')
