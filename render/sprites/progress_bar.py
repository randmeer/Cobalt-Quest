import pygame
from utils.__init__ import rta_dual, rta_height, renderText, rta_dual_height

class ProgressBar:
    def __init__(self, icon, maxvalue: int, colors: ((int, int, int), (int, int, int)), relsize: (float, float), relpos: (float, float), textanchor="left"):
        self.icon = icon
        self.maxvalue = maxvalue
        self.activecolor, self.passivecolor = colors[0], colors[1]
        self.relsize = relsize
        self.relpos = relpos
        self.rect = pygame.Rect
        self.value = 50
        self.resize()
        self.set(value=self.value)

    def set(self, value):
        self.value = value
        self.surf.fill(self.activecolor)
        self.surf.blit(self.passivesurf, ((self.value / self.maxvalue) * self.surf.get_width(), 0))
        self.image = pygame.Surface(rta_dual(self.relsize[0] + self.relsize[1]*1.5, self.relsize[1]), pygame.SRCALPHA)
        self.image.blit(self.surf, rta_dual(self.relsize[1]*1.5, 0))
        renderText(self.image, str(self.value), (0, 0), (255, 255, 255), 5)
        #self.image.blit(self.icon, rta_dual(self.relsize[1] * 2 - 0.0075, 0))

    def get(self):
        return self.image

    def resize(self):
        self.passivesurf = pygame.Surface(rta_dual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        self.passivesurf.fill(self.passivecolor)
        self.surf = pygame.Surface(rta_dual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        #self.icon = pygame.transform.scale(self.icon, rta_dual(self.relsize[1], self.relsize[1]))
        self.set(self.value)

    def draw(self, surface):
        surface.blit(self.get(), rta_dual_height(self.relpos[0], self.relpos[1]))
