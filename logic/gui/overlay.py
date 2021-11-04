import pygame
import QuickJSON
import os
import shutil

from distutils.dir_util import copy_tree
from utils import globs, play_sound, set_global_defaults, rta_dual, mp_screen, rta_dual_height, get_setting, get_inventory
from utils.images import images, item_tx, overlays
from render.elements import button, label, image
from render import gui

victory = pygame.transform.scale(images["victory"], globs.SIZE)
defeat = pygame.transform.scale(images["defeat"], globs.SIZE)


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
        mp = mp_screen()
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


def end_screen(window, background, end):
    # TODO: end screen textures
    set_global_defaults()
    img = []
    if end == "victory":
        play_sound('victory')
        img.append(image.Image(image=images["victory"], anchor="center", relpos=(0.5, 0.25)))
    if end == "defeat":
        play_sound('defeat')
        img.append(image.Image(image=images["defeat"], anchor="center", relpos=(0.5, 0.25)))
    end_gui = gui.GUI(background=background, overlay=128, images=img, buttons=[
        button.Button(relsize=(0.413, 0.1), anchor="midtop", text="Back to Menu", relpos=(0.5, 0.525)),
        button.Button(relsize=(0.413, 0.1), anchor="midtop", text="Replay", relpos=(0.5, 0.65))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if end_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.exittomenu = True
                    if end_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.exittomenu = True
        end_gui.draw(window=window)
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

    for i in settings_gui.labelgroup:
        if i.tags[0] == "saves" and i.tags[1] == "saveslist":
            i.render_outline()

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
        mp = mp_screen()
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
        mp = mp_screen()
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


def show_inventory(window, background):
    """
    background should be the current view of the window, not scaled,
    in order for the inventory gui to look like it lays on top of the window
    """
    s = True
    while s:
        s = _show_inventory(window=window, background=background)

def _show_inventory(window, background):
    """
    local function of show_inventory
    to re-run this function, call 'return True'
    to exit this function, call 'return False'
    """
    set_global_defaults()
    play_sound('click')

    # load inventory json
    inventory = QuickJSON.QJSON(f"./data/savegames/{get_setting('current_savegame')}/inventory.json")
    inventory.load()

    # create variables
    labels = []
    images = []

    # tags
    # overlay hotbar ["overlay", "hotbar", slot]
    # overlay tab    ["overlay,  "tab",    slot]
    # item hotbar    ["hotbar",  category, slot, name]
    # item tab       ["tab",     category, slot, name]
    # label hotbar   ["hotbar",  category, slot]
    # label tab      ["tab",     category, slot]

    # add overlays
    slots = []
    for i in range(5):
        for j in range(6):
            slots.append([0.605+j/14.25, 0.25+i/8])
            images.append(image.Image(tags=["overlay", "tab", i*6+j], image=overlays["weapon"][0], relpos=(0.605+j/14.25, 0.25+i/8), h_event=True, h_image=overlays["weapon"][1]))
    for i in range(len(inventory["hotbar"])):
        images.append(image.Image(tags=["overlay", "hotbar", i], image=overlays["unset"][0], relpos=(0.605+i/14.25, 0.925), h_event=True, h_image=overlays["unset"][1]))

    # add items
    for i in range(len(inventory["inventory"])):
        for j in range(len(inventory["inventory"][i][1])):
            if item_tx[inventory["inventory"][i][1][j][1]] is not None:
                images.append(image.Image(tags=["tab", inventory["inventory"][i][0], j, inventory["inventory"][i][1][j][1], inventory["inventory"][i][1][j][2], inventory["inventory"][i][1][j][3]], image=item_tx[inventory["inventory"][i][1][j][1]], relpos=(slots[j])))
                if inventory["inventory"][i][1][j][2] > 0:
                    labels.append(label.Label(tags=["tab", inventory["inventory"][i][0], j], text=str(inventory["inventory"][i][1][j][2]), anchor="topleft", relpos=(slots[j][0]-0.022, slots[j][1]+0.01), color=(255, 255, 255)))
    for i in range(len(inventory["hotbar"])):
        if item_tx[inventory["hotbar"][i][1]] is not None:
            images.append(image.Image(tags=["hotbar", inventory["hotbar"][i][0], i, inventory["hotbar"][i][1], inventory["hotbar"][i][2], inventory["hotbar"][i][3]], image=item_tx[inventory["hotbar"][i][1]], relpos=(0.605+i/14.25, 0.925)))
            for j in images:
                if j.tags[0] == "overlay" and j.tags[1] == "hotbar" and j.tags[2] == i:
                    j.image, j.h_image = overlays[inventory["hotbar"][i][0]]
            if inventory["hotbar"][i][2] > 0:
                labels.append(label.Label(tags=["hotbar", inventory["hotbar"][i][0], i], text=str(inventory["hotbar"][i][2]), anchor="topleft", relpos=(0.605+i/14.25-0.022, 0.925+0.005), color=(255, 255, 255)))

    # create gui
    inv_gui = gui.GUI(background=background, overlay=200, labels=labels, images=images, buttons=[
        button.Button(tags=["weapon", ""], anchor="center", relsize=(0.17, 0.1), text="WEAPON", relpos=(0.1, 0.1)),
        button.Button(tags=["armor", ""], anchor="center", relsize=(0.17, 0.1), text="ARMOR", relpos=(0.3, 0.1)),
        button.Button(tags=["tool", ""], anchor="center", relsize=(0.17, 0.1), text="TOOL", relpos=(0.5, 0.1)),
        button.Button(tags=["food", ""], anchor="center", relsize=(0.17, 0.1), text="FOOD", relpos=(0.7, 0.1)),
        button.Button(tags=["orb", ""], anchor="center", relsize=(0.17, 0.1), text="ORBS", relpos=(0.9, 0.1)),
        button.Button(tags=["", ""], anchor="bottomleft", relsize=(0.4, 0.1), text="SAVE AND RETURN", relpos=(0.05, 0.95))])
    inv_gui.buttongroup[0].set_pressed(press=True)
    current_tab = "weapon"
    target = None
    target_label = None

    def set_current_tab():
        for i in inv_gui.imagegroup:
            i.set_visible(visible=True)
            if i.tags[0] == "tab" and i.tags[1] != current_tab:
                i.set_visible(visible=False)
            if i.tags[0] == "overlay" and i.tags[1] == "tab":
                i.image, i.h_image = overlays[current_tab]
        for i in inv_gui.labelgroup:
            i.set_visible(visible=True)
            if i.tags[0] == "tab" and i.tags[1] != current_tab:
                i.set_visible(visible=False)
    set_current_tab()

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        mp = mp_screen()
        if target is not None:
            target.rect.center = mp
            if target_label is not None:
                target_label.rect.topleft = (target.rect.centerx-6, target.rect.centery+1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if inv_gui.buttongroup[5].rect.collidepoint(mp):
                        run = False
                    for i in range(5):
                        if inv_gui.buttongroup[i].rect.collidepoint(mp) and target is None:  # a tab button is pressed and no item is held
                            for j in range(5):
                                inv_gui.buttongroup[j].set_pressed(press=False)  # set all tab buttons not pressed
                            inv_gui.buttongroup[i].set_pressed(press=True)  # set clicked tab button pressed
                            current_tab = inv_gui.buttongroup[i].tags[0]  # update current tab
                            set_current_tab()
                            play_sound('click')

                    for ovlay in inv_gui.imagegroup:
                        if ovlay.rect.collidepoint(mp):
                            if ovlay.tags[0] == "overlay":
                                # THE CLICKED SLOT IS INSIDE THE TAB
                                if ovlay.tags[1] == "tab":
                                    unsuccessful = True
                                    # THERE IS AN ITEM ON THE CLICKED SLOT
                                    for item in inv_gui.imagegroup:
                                        if item.tags[0] == "tab" and item.tags[1] == current_tab and item.tags[2] == ovlay.tags[2] and item.rect.center == ovlay.rect.center:
                                            # THERE IS NO ITEM HELD
                                            if target is None:
                                                # pick up item
                                                target = item
                                                for labl in inv_gui.labelgroup:
                                                    if labl.tags[0] == "tab" and labl.tags[1] == current_tab and labl.tags[2] == ovlay.tags[2]:
                                                        target_label = labl
                                            # THERE IS AN ITEM HELD
                                            else:
                                                # THE ITEM HELD IS FROM THIS TAB
                                                if target.tags[1] == current_tab:
                                                    # switch places
                                                    potential_label = None
                                                    for labl in inv_gui.labelgroup:
                                                        if labl.tags[0] == "tab" and labl.tags[1] == current_tab and labl.tags[2] == ovlay.tags[2] and labl.rect.topleft == (ovlay.rect.centerx-6, ovlay.rect.centery+1):
                                                            potential_label = labl
                                                    if target_label is not None:
                                                        target_label.rect.topleft = (ovlay.rect.centerx-6, ovlay.rect.centery+1)
                                                        target_label.tags[2] = ovlay.tags[2]
                                                        target_label.tags[0] = ovlay.tags[1]
                                                    target.rect.center = item.rect.center
                                                    target.tags[2] = item.tags[2]
                                                    target.tags[0] = item.tags[0]
                                                    target_label = potential_label
                                                    target = item
                                                # THE ITEM HELD IS NOT FROM THIS TAB
                                                else:
                                                    pass
                                            unsuccessful = False
                                            break
                                    # THERE IS NO ITEM ON THE CLICKED SLOT
                                    if unsuccessful:
                                        # THERE IS NO ITEM HELD
                                        if target is None:
                                            # do nothing
                                            pass
                                        # THERE IS AN ITEM HELD
                                        else:
                                            # THE ITEM HELD IS FROM THIS TAB
                                            if target.tags[1] == current_tab:
                                                # put down item
                                                if target_label is not None:
                                                    target_label.rect.topleft = (ovlay.rect.centerx-6, ovlay.rect.centery+1)
                                                    target_label.tags[2] = ovlay.tags[2]
                                                    target_label.tags[0] = ovlay.tags[1]
                                                target.rect.center = ovlay.rect.center
                                                target.tags[2] = ovlay.tags[2]
                                                target.tags[0] = ovlay.tags[1]
                                                target_label = None
                                                target = None
                                            # THE ITEM HELD IS NOT FROM THIS TAB
                                            else:
                                                # do nothing
                                                pass
                                # THE CLICKED SLOT IS INSIDE THE HOTBAR
                                elif ovlay.tags[1] == "hotbar":
                                    unsuccessful = True
                                    # THERE IS AN ITEM ON THE CLICKED SLOT
                                    for item in inv_gui.imagegroup:
                                        if item.tags[0] == "hotbar" and item.tags[2] == ovlay.tags[2] and item.rect.center == ovlay.rect.center:
                                            # THERE IS NO ITEM HELD
                                            if target is None:
                                                # pick up item
                                                print("pickup")
                                                ovlay.image, ovlay.h_image = overlays["unset"]
                                                target = item
                                                for labl in inv_gui.labelgroup:
                                                    if labl.tags[0] == "hotbar" and labl.tags[2] == ovlay.tags[2]:
                                                        target_label = labl
                                            # THERE IS AN ITEM HELD
                                            else:
                                                # switch places
                                                potential_label = None
                                                for labl in inv_gui.labelgroup:
                                                    if labl.tags[0] == "hotbar" and labl.tags[2] == ovlay.tags[2] and labl.rect.topleft == (ovlay.rect.centerx-6, ovlay.rect.centery+1):
                                                        potential_label = labl
                                                if target_label is not None:
                                                    target_label.rect.topleft = (ovlay.rect.centerx-6, ovlay.rect.centery+1)
                                                    target_label.tags[2] = ovlay.tags[2]
                                                    target_label.tags[0] = ovlay.tags[1]
                                                target.rect.center = item.rect.center
                                                target.tags[2] = item.tags[2]
                                                target.tags[0] = item.tags[0]
                                                ovlay.image, ovlay.h_image = overlays[target.tags[1]]
                                                target_label = potential_label
                                                target = item
                                            unsuccessful = False
                                            break
                                    # THERE IS NO ITEM ON THE CLICKED SLOT
                                    if unsuccessful:
                                        # THERE IS NO ITEM HELD
                                        if target is None:
                                            # do nothing
                                            pass
                                        # THERE IS AN ITEM HELD
                                        else:
                                            # put down item
                                            if target_label is not None:
                                                target_label.rect.topleft = (ovlay.rect.centerx-6, ovlay.rect.centery+1)
                                                target_label.tags[2] = ovlay.tags[2]
                                                target_label.tags[0] = ovlay.tags[1]
                                            target.rect.center = ovlay.rect.center
                                            target.tags[2] = ovlay.tags[2]
                                            target.tags[0] = ovlay.tags[1]
                                            ovlay.image, ovlay.h_image = overlays[target.tags[1]]
                                            target_label = None
                                            target = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_e:
                    run = False
        if globs.quitgame:
            run = False
        if run:
            inv_gui.draw(window=window)

    # change & save inventory json
    for i in range(len(inventory["inventory"])):
        for j in range(len(inventory["inventory"][i][1])):
            inventory["inventory"][i][1][j][0] = inventory["inventory"][i][0]
            inventory["inventory"][i][1][j][1] = "unset"
            inventory["inventory"][i][1][j][2] = 0
            inventory["inventory"][i][1][j][3] = 0
    for i in range(len(inventory["hotbar"])):
        inventory["hotbar"][i][0] = "unset"
        inventory["hotbar"][i][1] = "unset"
        inventory["hotbar"][i][2] = 0
        inventory["hotbar"][i][3] = 0

    for i in inv_gui.imagegroup:
        if i.tags[0] == "tab":  # the image is an item inside the tab area
            for j in range(5):
                if i.tags[1] == inventory["inventory"][j][0]:  # the images belongs to the the category inv["inv"][j][0]
                    inventory["inventory"][j][1][i.tags[2]] = [i.tags[1], i.tags[3], i.tags[4], i.tags[5]]  # set item in inventory json
        elif i.tags[0] == "hotbar":
            inventory["hotbar"][i.tags[2]] = [i.tags[1], i.tags[3], i.tags[4], i.tags[5]]
    inventory.save()
    play_sound('click')
    return False


def stats(window, background):
    set_global_defaults()
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
                if event.button == globs.LEFT:
                    for i in stats_gui.buttongroup:
                        if i.rect.collidepoint(mp):
                            if i.tags[0] == "return":
                                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        stats_gui.draw(window=window)
    play_sound('click')
