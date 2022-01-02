import pygame
import QuickJSON

from utils import globs, img, mp_screen, set_global_defaults, play_sound, get_setting
from render.elements import button, image, label
from render import gui

def show_dungeon(window, dungeon):
    set_global_defaults()

    blueprint = QuickJSON.QJSON(f"./data/savegames/{get_setting('current_savegame')}/dungeons/{dungeon}/blueprint.json")
    blueprint.load()

    name = blueprint["display_name"]
    floors = blueprint["floors"]
    labels = []
    selected_floor = ""
    for i in range(len(floors)):
        color1, color2, hcolor = (199, 207, 204), (87, 114, 119), (235, 237, 233)
        if not floors[str(list(floors.keys())[i])]["unlocked"]:
            color1, color2, hcolor = (200, 100, 100), (100, 50, 50), (255, 100, 100)
        labels.append(label.Label(text=floors[str(list(floors.keys())[i])]["display_name"].upper(), relpos=(0.045, 0.25+0.15*i), anchor="tl", color=color1, h_event=True, h_color=hcolor, outlinecolor=(235, 237, 233), default_outlined=True))
        labels.append(label.Label(text="PROGRESS: " + str(floors[str(list(floors.keys())[i])]["progress"]) + "%", relpos=(0.1, 0.25+0.15*i + 0.05), anchor="tl", color=color2))
    labels.append(label.Label(text=name.upper(), relpos=(0.045, 0.08), anchor="topleft", color=(235, 237, 233), textsize=10))

    dungeon_gui = gui.GUI(background=img.misc["background"]["dungeon"], overlay=128, labels=labels,
                          buttons=[button.Button(anchor="br", relsize=(0.2, 0.1), text="PLAY", relpos=(0.95, 0.95)),
                                   button.Button(anchor="br", relsize=(0.2, 0.1), text="CANCEL", relpos=(0.7, 0.95))],
                          images=[image.Image(image=img.misc["map"][dungeon], anchor="topleft", relpos=(0.5, 0.25))])
    for i in dungeon_gui.labelgroup:
        i.set_outline(outline=False)
    dungeon_gui.labelgroup[0].set_outline(outline=True)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        if globs.quitgame:
            run = False
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    for i in range(len(floors)):
                        # *2 because only every second label is a floor title
                        if dungeon_gui.labelgroup[i*2].rect.collidepoint(mp):
                            selected_floor = str(list(floors.keys())[i])
                            play_sound('click')
                            for j in dungeon_gui.labelgroup:
                                j.set_outline(outline=False)
                            dungeon_gui.labelgroup[i*2].set_outline(outline=True)
                    if dungeon_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.floor = True
                        globs.floor_str = selected_floor
                    if dungeon_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.map = True
                        globs.floor_str = selected_floor
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.map = True
        dungeon_gui.draw(window=window)
    play_sound('click')
