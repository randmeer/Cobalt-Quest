import pygame
from utils.__init__ import relToAbsDual2, relToAbsHeight, renderText, getTextRect

class ProgressBar:
    def __init__(self, icon, maxvalue: int, colors: ((int, int, int), (int, int, int)), relsize: (float, float), textanchor="left"):
        self.icon = icon
        self.maxvalue = maxvalue
        self.activecolor, self.passivecolor = colors[0], colors[1]
        self.relsize = relsize
        self.rect = pygame.Rect
        self.value = 50
        self.resize()
        self.set(value=self.value)

    def set(self, value):
        self.value = value
        self.surf.fill(self.activecolor)
        self.surf.blit(self.passivesurf, ((self.value / self.maxvalue) * self.surf.get_width(), 0))
        self.image = pygame.Surface(relToAbsDual2(self.relsize[0]+self.relsize[1]*3, self.relsize[1]), pygame.SRCALPHA)
        self.image.blit(self.surf, relToAbsDual2(self.relsize[1]*3, 0))
        renderText(self.image, str(self.value), (0, 0), (255, 255, 255), relToAbsHeight(self.relsize[1]*1.25))
        # the factor 1.25 resizes the text to use the full height of the surface.
        # this should be calculated with a getTextRect and not hardcoded, but well, i'm lazy
        self.image.blit(self.icon, relToAbsDual2(self.relsize[1]*2-0.0075, 0))

    def get(self):
        return self.image

    def resize(self):
        self.passivesurf = pygame.Surface(relToAbsDual2(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        self.passivesurf.fill(self.passivecolor)
        self.surf = pygame.Surface(relToAbsDual2(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        self.icon = pygame.transform.scale(self.icon, relToAbsDual2(self.relsize[1], self.relsize[1]))
        self.set(self.value)
