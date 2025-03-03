import pygame
import QuickJSON

from octagon.utils import mp_screen, get_setting, img, var, play_sound
from octagon.gui import GUI

from game import globs

class Dungeon(GUI):
    def __init__(self, window):
        super().__init__(window)
        self.add_button(text="play", id="play")
        self.add_leftclick_events(self.play)
        self.add_keypress_function(self.keypress)

    def play(self):
        globs.floor_str = "entrance"
        self.exit("floor")

    def keypress(self, key):
        if key == pygame.K_ESCAPE:
            self.exit()


'''
def show_dungeon(window):
    play_sound('click')
    dungeon = globs.dungeon_str

    blueprint = QuickJSON.QJSON(f"./data/savegames/{get_setting('current_savegame')}/dungeons/{dungeon}/blueprint.json")
    blueprint.load()

    name = blueprint["display_name"]
    floors = blueprint["floors"]
    labels = []
    images = []
    selected_floor = ""
    globs.floor_str = list(floors.keys())[0]
    for i in range(len(floors)):
        color1, color2, hcolor = (199, 207, 204), (87, 114, 119), (235, 237, 233)
        if not floors[str(list(floors.keys())[i])]["unlocked"]:
            color1, color2, hcolor = (200, 100, 100), (100, 50, 50), (255, 100, 100)
        labels.append(label.Label(text=floors[str(list(floors.keys())[i])]["display_name"].upper(), relpos=(0.045, 0.25+0.15*i), anchor="tl", color=color1, h_event=True, h_color=hcolor, outlinecolor=(235, 237, 233), default_outlined=True))
        labels.append(label.Label(text="PROGRESS: " + str(floors[str(list(floors.keys())[i])]["progress"]) + "%", relpos=(0.1, 0.25+0.15*i + 0.05), anchor="tl", color=color2))
        images.append(image.Image(tags=[list(floors.keys())[i]], image=img.misc["map"][dungeon+"-"+list(floors.keys())[i]], anchor="topleft", relpos=(0.5, 0.25)))

    labels.append(label.Label(text=name.upper(), relpos=(0.045, 0.08), anchor="topleft", color=(235, 237, 233), textsize=10))

    dungeon_gui = gui.GUI(background=img.misc["background"]["dungeon"], overlay=128, labels=labels, images=images,
                          buttons=[button.Button(anchor="br", relsize=(0.2, 0.1), text="PLAY", relpos=(0.95, 0.95)),
                                   button.Button(anchor="br", relsize=(0.2, 0.1), text="CANCEL", relpos=(0.7, 0.95))],)
    for i in dungeon_gui.labelgroup:
        i.set_outline(False)
    for j in dungeon_gui.imagegroup:
        j.set_visible(False)
    dungeon_gui.labelgroup[0].set_outline(True)
    dungeon_gui.imagegroup[0].set_visible(True)

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    for i in range(len(floors)):
                        # *2 because only every second label is a floor title
                        if dungeon_gui.labelgroup[i*2].rect.collidepoint(mp):
                            selected_floor = str(list(floors.keys())[i])
                            globs.floor_str = selected_floor
                            play_sound('click')
                            for j in dungeon_gui.labelgroup:
                                j.set_outline(outline=False)
                            for k in dungeon_gui.imagegroup:
                                if selected_floor == k.tags[0]:
                                    k.set_visible(True)
                                else:
                                    k.set_visible(False)
                            dungeon_gui.labelgroup[i*2].set_outline(outline=True)
                    if dungeon_gui.buttongroup[0].rect.collidepoint(mp):
                        return "floor"
                    if dungeon_gui.buttongroup[1].rect.collidepoint(mp):
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        if globs.quitgame:
            return "quit"
        dungeon_gui.draw(window=window)

'''