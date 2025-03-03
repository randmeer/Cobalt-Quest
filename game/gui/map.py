import pygame

from octagon.utils import mp_screen, img, play_sound
from octagon.utils.static import tuple_subtract, tuple_add
from octagon.gui import GUI
from octagon.utils.img import Texture

from game import globs


class Map(GUI):
    def __init__(self, window):
        super().__init__(window)

        self.add_button(text="go", id="go")
        self.add_leftclick_events(self.go)
        self.add_keypress_function(self.keypress)

    def go(self):
        globs.dungeon_str = "northern_plains"
        self.exit("dungeon")

    def keypress(self, key):
        if key == pygame.K_ESCAPE:
            self.exit("back")


'''
def show_map(window):
    play_sound('click')

    northern_plains = button.Button(relsize=(0.06, 0.1), text="", relpos=(0.25, 0.4), visible=False)
    map = Texture(img.misc["map"]["map"], 0.1)
    leftclick_label = label.Label(text="LEFT CLICK: VISIT DUNGEON", relpos=(0.05, 0.9), anchor="bottomleft", color=(57, 74, 80))
    rightclick_label = label.Label(text="RIGHT CLICK: MOVE MAP", relpos=(0.05, 0.95), anchor="bottomleft", color=(57, 74, 80))
    map_gui = gui.GUI(background=img.misc["background"]["dungeon"], overlay=160, labels=[leftclick_label, rightclick_label],
                      buttons=[button.Button(anchor="topleft", relsize=(0.4, 0.1), text="BACK TO MENU", relpos=(0.05, 0.05)), northern_plains],
                      images=[image.Image(image=map.get(), anchor="center", relpos=(0.5, 0.5))])

    selected_rect = None

    northern_plains_offset = tuple_subtract(northern_plains.rect.topleft, map_gui.imagegroup[0].rect.topleft)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        mp = mp_screen()
        map_gui.imagegroup[0].image = map.get()
        # event iteration
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if map_gui.buttongroup[0].rect.collidepoint(mp):
                        return
                    if map_gui.buttongroup[1].rect.collidepoint(mp):
                        # northern plains dungeon
                        globs.dungeon_str = "northern_plains"
                        return "dungeon"
                if event.button == 3:
                    if map_gui.imagegroup[0].rect.collidepoint(mp):
                        # map
                        selected_rect = map_gui.imagegroup[0].rect
                        offset = (mp_screen()[0] - selected_rect.topleft[0], mp_screen()[1] - selected_rect.topleft[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    selected_rect = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_rect:
                    selected_rect.topleft = (mp_screen()[0] - offset[0], mp_screen()[1] - offset[1])
                    northern_plains.rect.topleft = tuple_add(selected_rect.topleft, northern_plains_offset)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        map_gui.draw(window=window)

'''