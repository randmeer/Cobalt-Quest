import pygame

from utils import globs

class GUI:
    """
    is used to create a surface with a given background and buttons & images on it,
    preferrably handeled by a script in logic.gui
    """
    def __init__(self, background, buttons=None, labels=None, images=None, overlay=None, overlaycolor=(0, 0, 0)):
        self.background = background
        self.hasbuttons = self.haslabels = self.hasimages = False
        if buttons is not None:
            self.hasbuttons = True
            self.buttongroup = []
            for i in buttons:
                self.buttongroup.append(i)
        if labels is not None:
            self.haslabels = True
            self.labelgroup = []
            for i in labels:
                self.labelgroup.append(i)
        if images is not None:
            self.hasimages = True
            self.imagegroup = []
            for i in images:
                self.imagegroup.append(i)

        if overlay is not None:
            self.overlay = True
            self.overlay_alpha = overlay
            self.overlaycolor = overlaycolor
        else:
            self.overlay = False

    def get_surface(self):
        og_surf = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
        og_surf.blit(self.background, (0, 0))
        if self.overlay:
            overlay = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
            overlay.fill(self.overlaycolor)
            overlay.set_alpha(self.overlay_alpha)
            og_surf.blit(overlay, (0, 0))
        if self.hasbuttons:
            for i in self.buttongroup:
                i.update()
                i.draw(surface=og_surf)
        if self.hasimages:
            for i in self.imagegroup:
                i.update()
                i.draw(surface=og_surf)
        if self.haslabels:
            for i in self.labelgroup:
                i.update()
                i.draw(surface=og_surf)
        return og_surf

    def draw(self, window):
        og_surf = self.get_surface()
        surf = pygame.transform.scale(og_surf, globs.res_size)
        window.blit(surf, (0, 0))
        pygame.display.update()
