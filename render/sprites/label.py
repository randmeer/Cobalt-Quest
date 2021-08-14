import pygame
from utils.__init__ import rta_dual, renderText, getTextRect

class Label(pygame.sprite.Sprite):

    def __init__(self, text, relpos, textcolor=(75, 75, 75), reltextsize=0.1, anchor="center"):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.textcolor = textcolor
        self.reltextsize = reltextsize
        self.relpos = relpos
        self.anchor = anchor
        self.update()

    def update(self):
        #self.textsize = relToAbs(self.reltextsize)
        self.textsize = 5
        self.textrect = getTextRect(self.text, self.textsize)
        self.surface = pygame.Surface((self.textrect.width, self.textrect.height))
        self.surface = pygame.Surface.convert_alpha(self.surface)
        renderText(window=self.surface, text=self.text, position=(0, 0), color=self.textcolor, size=self.textsize)
        self.image = self.surface

        if self.anchor == "topcenter":
            self.textrect.midbottom = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "bottomcenter":
            self.textrect.midbottom = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "leftcenter":
            self.textrect.midleft = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "rightcenter":
            self.textrect.midright = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "topleft":
            self.textrect.topleft = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "topright":
            self.textrect.topright = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "bottomleft":
            self.textrect.bottomleft = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "bottomright":
            self.textrect.bottomright = rta_dual(self.relpos[0], self.relpos[1])
        elif self.anchor == "center":
            self.textrect.center = rta_dual(self.relpos[0], self.relpos[1])

    def draw(self, surface):
        surface.blit(self.image, self.textrect)
