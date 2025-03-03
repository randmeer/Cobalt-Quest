import pygame
import QuickJSON

from octagon.utils import img, var, get_setting, mp_screen, play_sound
from octagon.gui import image, label, button, GUI

from game import globs


# TODO: rework as OOP


def show_inventory(window, background, itemdict):
    """
    background should be the current view of the window, not scaled,
    in order for the inventory gui to look like it lays on top of the window
    """
    s = True
    while s:
        s = _show_inventory(window=window, background=background, itemdict=itemdict)


def _show_inventory(window, background, itemdict):
    """
    local function of show_inventory
    to re-run this function, call 'return True'
    to exit this function, call 'return False'
    """
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
    # item hotbar    ["hotbar",  category, slot]
    # item tab       ["tab",     category, slot]
    # label hotbar   ["hotbar",  category, slot]
    # label tab      ["tab",     category, slot]

    # tab overlays
    slots = []  # position of the overlays, later re-used by the images
    for i in range(5):
        for j in range(6):
            slots.append([0.605 + j / 14.25, 0.25 + i / 8])
            _tags = ["overlay", "tab", i * 6 + j]
            _image = img.misc["inventory"]["weapon"][0]
            images.append(image.Image(tags=_tags, image=_image, relpos=(0.605 + j / 14.25, 0.25 + i / 8), h_event=True, h_image=img.misc["inventory"]["weapon"][1]))

    # hotbar overlays
    for i in range(len(inventory["hotbar"])):
        _tags = ["overlay", "hotbar", i]
        _image = img.misc["inventory"]["unset"][0]
        images.append(image.Image(tags=_tags, image=_image, relpos=(0.605 + i / 14.25, 0.925), h_event=True, h_image=img.misc["inventory"]["unset"][1]))


    '''
    # tab images
    for i in range(len(inventory["inventory"])):
        for j in range(len(inventory["inventory"][i][1])):
            if inventory["inventory"][i][1][j][1] != "unset":

                # item
                print(inventory["inventory"][0][1][0][0])
                print(itemdict[inventory["inventory"][0][1][0][0]])

                _tags = ["tab", itemdict[inventory["inventory"][i][1][0][0]][0], j, inventory["inventory"][i][1][j][1], inventory["inventory"][i][1][j][2], inventory["inventory"][i][1][j][3]]
                _image = img.item[inventory["inventory"][i][1][j][0]]
                images.append(image.Image(tags=_tags, image=_image, relpos=(slots[j])))

                # label
                if inventory["inventory"][i][1][j][2] > 0:
                    _tags = ["tab", itemdict[inventory["inventory"][i][0]][0], j]
                    _text = str(inventory["inventory"][i][1][j][2])
                    labels.append(label.Label(tags=_tags, text=_text, anchor="topleft", relpos=(slots[j][0] - 0.022, slots[j][1] + 0.01), color=(255, 255, 255)))

    # hotbar images
    for i in range(len(inventory["hotbar"])):
        if inventory["hotbar"][i][1] != "unset":

            # item
            _tags = ["hotbar", itemdict[inventory["hotbar"][i][0]][0], i, inventory["hotbar"][i][1], inventory["hotbar"][i][2], inventory["hotbar"][i][3]]
            _image = img.item[inventory["hotbar"][i][1]]
            images.append(image.Image(tags=_tags, image=_image, relpos=(0.605 + i / 14.25, 0.925)))

            # item overlay
            for j in images:
                if j.tags[0] == "overlay" and j.tags[1] == "hotbar" and j.tags[2] == i:
                    j.image, j.h_image = img.misc["inventory"][inventory["hotbar"][i][0]]

            # label
            if inventory["hotbar"][i][2] > 0:
                labels.append(label.Label(tags=["hotbar", itemdict[inventory["hotbar"][i][0]][0], i], text=str(inventory["hotbar"][i][2]), anchor="topleft", relpos=(0.605 + i / 14.25 - 0.022, 0.925 + 0.005), color=(255, 255, 255)))
    
    '''

    inv = inventory["inventory"]

    # buttons
    buttons = []
    j = 0
    for i in inventory["inventory"]:
        buttons.append(button.Button(anchor="center", relsize=(0.22, 0.1), text=i, relpos=(0.14+(0.24*j), 0.1)))
        j += 1
    buttons.append(button.Button(anchor="bottomleft", relsize=(0.4, 0.1), text="SAVE AND RETURN", relpos=(0.05, 0.95)))

    # create gui
    inv_gui = GUI(background=background, overlay=200, labels=labels, images=images, buttons=buttons)

    # pre-select the weapons tab
    inv_gui.buttongroup[0].set_pressed(press=True)
    current_tab = "weapon"

    # no item is held
    target = None
    target_label = None

    # set current tab
    def set_current_tab():
        for i in inv_gui.imagegroup:
            i.set_visible(visible=True)
            if i.tags[0] == "tab" and i.tags[1] != current_tab:
                i.set_visible(visible=False)
            if i.tags[0] == "overlay" and i.tags[1] == "tab":
                i.image, i.h_image = img.misc["inventory"][current_tab]
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
        # if target is not None:
        #     target.rect.center = mp
        #     if target_label is not None:
        #         target_label.rect.topleft = (target.rect.centerx - 6, target.rect.centery + 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:

                    # exit button
                    if inv_gui.buttongroup[4].rect.collidepoint(mp):
                        run = False

                    # tab buttons
                    for i in range(4):
                        if inv_gui.buttongroup[i].rect.collidepoint(mp) and target is None:  # a tab button is pressed and no item is held
                            for j in range(4):
                                inv_gui.buttongroup[j].set_pressed(press=False)  # set all tab buttons not pressed
                            inv_gui.buttongroup[i].set_pressed(press=True)  # set clicked tab button pressed
                            # current_tab = inv_gui.buttongroup[i].tags[0]  # update current tab
                            set_current_tab()
                            play_sound('click')

                    #'''
                    
                    # item
                    for ovlay in inv_gui.imagegroup:  # all the images
                        if ovlay.rect.collidepoint(mp):  # the images that collide with the mouse
                            if ovlay.tags[0] == "overlay":  # the overlay that collides with the mouse

                                # the clicked overlay is in the tab area
                                if ovlay.tags[1] == "tab":
                                    unsuccessful = True

                                    # there is an item on the clicked slot
                                    for item in inv_gui.imagegroup:
                                        if item.tags[0] == "tab" and item.tags[1] == current_tab and item.tags[2] == ovlay.tags[2] and item.rect.center == ovlay.rect.center:
                                            # their rects are at the same spot ??? (not sure if needed) ############################## TODO

                                            # there is no item held --> pick up item
                                            if target is None:
                                                target = item
                                                for labl in inv_gui.labelgroup:
                                                    if labl.tags[0] == "tab" and labl.tags[1] == current_tab and \
                                                            labl.tags[2] == ovlay.tags[2]:
                                                        target_label = labl

                                            # there is an item held
                                            else:

                                                # the item is from this tab --> switch places with target
                                                if target.tags[1] == current_tab:
                                                    potential_label = None
                                                    for labl in inv_gui.labelgroup:
                                                        if labl.tags[0] == "tab" and labl.tags[1] == current_tab and labl.tags[2] == ovlay.tags[2] and labl.rect.topleft == (ovlay.rect.centerx - 6, ovlay.rect.centery + 1):
                                                            potential_label = labl
                                                    if target_label is not None:
                                                        target_label.rect.topleft = (
                                                        ovlay.rect.centerx - 6, ovlay.rect.centery + 1)
                                                        target_label.tags[2] = ovlay.tags[2]
                                                        target_label.tags[0] = ovlay.tags[1]
                                                    target.rect.center = item.rect.center
                                                    target.tags[2] = item.tags[2]
                                                    target.tags[0] = item.tags[0]
                                                    target_label = potential_label
                                                    target = item

                                                # the item is not from this tab --> pass
                                                else:
                                                    pass
                                            unsuccessful = False
                                            break

                                    # there is no item on the clicked slot
                                    if unsuccessful:

                                        # there is no item held --> pass
                                        if target is None:
                                            pass

                                        # there is an item held
                                        else:

                                            # the held item is from this tab --> put down item
                                            if target.tags[1] == current_tab:
                                                if target_label is not None:
                                                    target_label.rect.topleft = (
                                                    ovlay.rect.centerx - 6, ovlay.rect.centery + 1)
                                                    target_label.tags[2] = ovlay.tags[2]
                                                    target_label.tags[0] = ovlay.tags[1]
                                                target.rect.center = ovlay.rect.center
                                                target.tags[2] = ovlay.tags[2]
                                                target.tags[0] = ovlay.tags[1]
                                                target_label = None
                                                target = None

                                            # the held item is not from this tab --> pass
                                            else:
                                                pass

                                # the clicked overlay is in the hotbar
                                elif ovlay.tags[1] == "hotbar":
                                    unsuccessful = True

                                    # there is an item on the clicked slot
                                    for item in inv_gui.imagegroup:
                                        if item.tags[0] == "hotbar" and item.tags[2] == ovlay.tags[2] and item.rect.center == ovlay.rect.center:

                                            # there is no item held --> pick up item
                                            if target is None:
                                                ovlay.image, ovlay.h_image = img.misc["inventory"]["unset"]
                                                target = item
                                                for labl in inv_gui.labelgroup:
                                                    if labl.tags[0] == "hotbar" and labl.tags[2] == ovlay.tags[2]:
                                                        target_label = labl

                                            # there is an item held --> switch places
                                            else:
                                                potential_label = None
                                                for labl in inv_gui.labelgroup:
                                                    if labl.tags[0] == "hotbar" and labl.tags[2] == ovlay.tags[
                                                        2] and labl.rect.topleft == (
                                                    ovlay.rect.centerx - 6, ovlay.rect.centery + 1):
                                                        potential_label = labl
                                                if target_label is not None:
                                                    target_label.rect.topleft = (
                                                    ovlay.rect.centerx - 6, ovlay.rect.centery + 1)
                                                    target_label.tags[2] = ovlay.tags[2]
                                                    target_label.tags[0] = ovlay.tags[1]
                                                target.rect.center = item.rect.center
                                                target.tags[2] = item.tags[2]
                                                target.tags[0] = item.tags[0]
                                                ovlay.image, ovlay.h_image = img.misc["inventory"][target.tags[1]]
                                                target_label = potential_label
                                                target = item
                                            unsuccessful = False
                                            break

                                    # there is no item on the clicked slot
                                    if unsuccessful:

                                        # there is no item held --> pass
                                        if target is None:
                                            pass

                                        # there is an item held --> put down item
                                        else:
                                            if target_label is not None:
                                                target_label.rect.topleft = (
                                                ovlay.rect.centerx - 6, ovlay.rect.centery + 1)
                                                target_label.tags[2] = ovlay.tags[2]
                                                target_label.tags[0] = ovlay.tags[1]
                                            target.rect.center = ovlay.rect.center
                                            target.tags[2] = ovlay.tags[2]
                                            target.tags[0] = ovlay.tags[1]
                                            ovlay.image, ovlay.h_image = img.misc["inventory"][target.tags[1]]
                                            target_label = None
                                            target = None
                    #'''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_e:
                    run = False
        if globs.quitgame:
            run = False
        if run:
            inv_gui.draw(window=window)

    """
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
                    inventory["inventory"][j][1][i.tags[2]] = [i.tags[1], i.tags[3], i.tags[4],
                                                               i.tags[5]]  # set item in inventory json
        elif i.tags[0] == "hotbar":
            inventory["hotbar"][i.tags[2]] = [i.tags[1], i.tags[3], i.tags[4], i.tags[5]]
    inventory.save()
    """

    play_sound('click')
    return False
