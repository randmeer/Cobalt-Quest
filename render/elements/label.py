import pygame
from utils.__init__ import rta_dual, renderText, getTextRect, set_anchor_point

class Label(pygame.sprite.Sprite):

    def __init__(self, text, relpos, textcolor=(75, 75, 75), reltextsize=0.1, anchor="center", font="game"):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.textcolor = textcolor
        self.reltextsize = reltextsize
        self.relpos = relpos
        self.anchor = anchor
        self.font = font
        self.update()

    def update(self):
        #self.textsize = relToAbs(self.reltextsize)
        self.textsize = 5
        self.textrect = getTextRect(self.text, self.textsize)
        self.surface = pygame.Surface((self.textrect.width, self.textrect.height))
        self.surface = pygame.Surface.convert_alpha(self.surface)
        renderText(window=self.surface, text=self.text, position=(0, 0), color=self.textcolor, size=self.textsize, font=self.font)
        self.image = self.surface

        pos = rta_dual(self.relpos[0], self.relpos[1])
        set_anchor_point(self.textrect, pos, self.anchor)

    def draw(self, surface):
        surface.blit(self.image, self.textrect)
