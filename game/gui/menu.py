from octagon.utils import var
from octagon.utils import img
from octagon import gui

from game import globs
from game.overlay import settings, alert, inventory, statistics


class Menu(gui.GUI):
    def __init__(self, window):
        super().__init__(window)
        self.add_button(text="Singleplayer", relpos=(0.5, 0.4), anchor="midtop", relsize=(0.5, 0.09), id="singleplayer")
        self.add_button(text="Multiplayer", relpos=(0.5, 0.52), anchor="midtop", relsize=(0.5, 0.09), id="multiplayer")
        self.add_button(text="Settings", relpos=(0.5, 0.64), anchor="midtop", relsize=(0.5, 0.09), id="settings")
        self.add_image(surface=img.misc["logo"], relpos=(0.5, 0.2), anchor="center")
        self.add_label(text=f"VERSION {globs.VERSION}", relpos=(0.01, 0.98), anchor="bottomleft", color=var.GRAYSHADES[5])
        self.add_label(text="RANDE STUDIOS", relpos=(0.01, 0.94), anchor="bottomleft", color=var.GRAYSHADES[5])
        self.add_leftclick_events(self.singleplayer, self.multiplayer, self.settings)

    def singleplayer(self):
        self.exit("singleplayer")

    def multiplayer(self):
        self.show_overlay(alert.Alert, {"message": "MULTIPLAYER IS NOT AVAILABLE YET"})

    def settings(self):
        self.show_overlay(settings.Settings)

