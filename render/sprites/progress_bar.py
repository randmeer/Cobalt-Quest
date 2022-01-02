import pygame
from utils import img, rta_dual, render_text, rta_dual_height, get_text_rect

class ProgressBar:
    def __init__(self, maxvalue: int, relsize: (float, float), relpos: (float, float), colors=((255, 0, 0), (75, 75, 75)), icon=None, image=None, textanchor="left"):
        self.icon = icon
        self.maxvalue = maxvalue
        self.icon = icon
        self.original_image = image
        self.activecolor, self.passivecolor = colors[0], colors[1]
        self.relsize = relsize
        self.relpos = relpos
        self.rect = pygame.Rect
        self.value = maxvalue
        self.resize()
        self.set(value=self.value)

    def set(self, value, maxvalue=None):
        self.value = value
        if maxvalue is not None:
            self.maxvalue = maxvalue
        if self.original_image:
            surf = self.surf.copy()
            surf.blit(self.passivesurf, (-(self.value / self.maxvalue) * self.surf.get_width(), 0))
            passivesurf = surf
            self.surf.blit(self.original_image, (0, 0))
        else:
            self.surf.fill(self.activecolor)
            passivesurf = self.passivesurf
        self.surf.blit(passivesurf, ((self.value / self.maxvalue) * self.surf.get_width(), 0))
        self.image = pygame.Surface(rta_dual(self.relsize[0] + self.relsize[1]*2, self.relsize[1]), pygame.SRCALPHA)
        self.image.blit(self.surf, rta_dual(self.relsize[1]*2, 0))
        textrect = get_text_rect(str(self.value))
        textrect.topright = (17, 0)
        render_text(self.image, str(self.value), (textrect.x, textrect.y), (255, 255, 255), 5)
        if self.icon:
            self.image.blit(self.icon, rta_dual(self.relsize[1] * 2 - 0.0075, 0))

    def get(self):
        return self.image

    def resize(self):
        if self.original_image:
            self.passivesurf = img.misc["bar"]["empty"]
        else:
            self.passivesurf = pygame.Surface(rta_dual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
            self.passivesurf.fill(self.passivecolor)
        self.surf = pygame.Surface(rta_dual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        if self.icon:
            self.icon = pygame.transform.scale(self.icon, rta_dual(self.relsize[1], self.relsize[1]))
        self.set(self.value)

    def draw(self, surface):
        surface.blit(self.get(), rta_dual_height(self.relpos[0], self.relpos[1]))
