import pygame

from octagon.utils import get_setting, var
from octagon import gui

from game import globs


class Singleplayer(gui.GUI):
    def __init__(self, window):
        super().__init__(window)
        self.add_button(text="Map", relpos=(0.045, 0.285), relsize=(0.2, 0.09), id="map")
        self.add_button(text="Shop", relpos=(0.26, 0.285), relsize=(0.2, 0.09), id="shop")
        self.add_button(text="Inventory", relpos=(0.045, 0.40), relsize=(0.415, 0.09), id="inventory")
        self.add_button(text="Mods", relpos=(0.045, 0.52), relsize=(0.2, 0.09), id="mods")
        self.add_button(text="Stats", relpos=(0.26, 0.52), relsize=(0.2, 0.09), id="stats")
        self.add_button(text="Back to Menu", relpos=(0.045, 0.64), relsize=(0.415, 0.09), id="back")
        self.add_button(text="Manage Saves", relpos=(0.6, 0.85), relsize=(0.35, 0.09), id="saves")
        self.add_label(text=f"VERSION {globs.VERSION}", relpos=(0.01, 0.98), anchor="bottomleft", color=var.GRAYSHADES[5])
        self.add_label(text="RANDE STUDIOS", relpos=(0.01, 0.94), anchor="bottomleft", color=var.GRAYSHADES[5])
        self.add_label(text="SELECT SAVEGAME", relpos=(0.6, 0.1), anchor="bottomleft", color=var.WHITE)
        self.add_label(text="SINGLEPLAYER", relpos=(0.045, 0.08), anchor="topleft", color=var.WHITE, double_size=True)
        self.add_keypress_function(self.keypress)
        self.add_leftclick_events(self.map, self.shop, self.inventory, self.mods, self.back, self.saves)

    def keypress(self, key):
        if key == pygame.K_ESCAPE:
            self.exit('back')

    def map(self):
        if get_setting("current_savegame") == "":
            # alert please select savegame first
            pass
        else:
            self.exit("map")

    def shop(self):
        # alert not available
        pass

    def inventory(self):
        # if savegame selected
            # inventory overlay
        # else
            # alert plase select savegame first
        pass

    def mods(self):
        # alert not available
        pass

    def back(self):
        self.exit('back')

    def saves(self):
        # saves overlay
        pass
