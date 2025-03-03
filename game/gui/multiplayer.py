import pygame

from octagon import gui


class Multiplayer(gui.GUI):
    def __init__(self, window):
        super().__init__(window)
        self.add_keypress_function(self.keypress)

    def keypress(self, key):
        if key == pygame.K_ESCAPE:
            self.exit('back')
