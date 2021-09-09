import pygame
from utils import rta_dual, render_text, rta_dual_height, get_text_rect
from utils.images import images

class ProgressBar:
    def __init__(self, icon, maxvalue: int, colors: ((int, int, int), (int, int, int)), relsize: (float, float), relpos: (float, float), has_image=False, image_str="", textanchor="left"):
        self.icon = icon
        self.maxvalue = maxvalue
        self.has_image = has_image
        self.image_str = image_str
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
        if self.has_image:
            surf = self.surf.copy()
            surf.blit(self.passivesurf, (-(self.value / self.maxvalue) * self.surf.get_width(), 0))
            passivesurf = surf
            self.surf.blit(images[self.image_str], (0, 0))
        else:
            self.surf.fill(self.activecolor)
            passivesurf = self.passivesurf
        self.surf.blit(passivesurf, ((self.value / self.maxvalue) * self.surf.get_width(), 0))
        self.image = pygame.Surface(rta_dual(self.relsize[0] + self.relsize[1]*2, self.relsize[1]), pygame.SRCALPHA)
        self.image.blit(self.surf, rta_dual(self.relsize[1]*2, 0))
        textrect = get_text_rect(str(self.value))
        textrect.topright = (17, 0)
        print(textrect.topleft)
        render_text(self.image, str(self.value), (textrect.x, textrect.y), (255, 255, 255), 5)
        #self.image.blit(self.icon, rta_dual(self.relsize[1] * 2 - 0.0075, 0))

    def get(self):
        return self.image

    def resize(self):
        if self.has_image:
            self.passivesurf = images["bar_empty"]
        else:
            self.passivesurf = pygame.Surface(rta_dual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
            self.passivesurf.fill(self.passivecolor)
        self.surf = pygame.Surface(rta_dual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        #self.icon = pygame.transform.scale(self.icon, rta_dual(self.relsize[1], self.relsize[1]))
        self.set(self.value)

    def draw(self, surface):
        surface.blit(self.get(), rta_dual_height(self.relpos[0], self.relpos[1]))
