import pygame

from octagon.utils import var
from octagon import gui


class TitleScreen(gui.GUI):
    def __init__(self, window):
        super().__init__(window, overlay_alpha=192)
        self.add_label(text="PRESS ANY KEY TO START", relpos=(0.5, 0.5), anchor="center", color=var.WHITE)
        self.add_leftclick_function(self.leftclick)
        self.add_keypress_function(self.keypress)
        self.silent = True

    def leftclick(self, pos):
        self.exit("menu")

    def keypress(self, key):
        if not (key == var.COMMAND or key == pygame.K_q or key == var.ALT or key == var.KEY_F4 or key == pygame.K_ESCAPE):
            self.exit("menu")

