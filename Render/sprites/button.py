import pygame
from utils.__init__ import relToAbs, relToAbsDual, renderText, getTextRect, gradientRect

class Button(pygame.sprite.Sprite):

    def __init__(self, relwidth, relheight, textcontent, relpos, textcolor=(75, 75, 75), reltextsize=0.1,
                 relborder=0.02, bordercolor=(255, 255, 255), innercolor=(194, 205, 209), anchor="center",
                 hovergradient=((255, 141, 141), (141, 187, 255)), hovercolor=(214, 225, 229)):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface(relToAbsDual(relwidth, relheight))
        self.surface.fill(bordercolor)
        self.innerarea = pygame.Surface(relToAbsDual(relwidth - relborder, relheight - relborder))
        self.innerarea.fill(innercolor)
        self.surface.blit(self.innerarea, (relToAbsDual(relborder / 2, relborder / 2)))
        self.image = self.surface
        self.hoversurface = pygame.Surface(relToAbsDual(relwidth, relheight))
        self.hoversurface.blit(gradientRect(self.hoversurface.get_width(), self.hoversurface.get_height(), hovergradient[0], hovergradient[1]), (0, 0))
        self.innerarea.fill(hovercolor)
        self.hoversurface.blit(self.innerarea, (relToAbsDual(relborder / 2, relborder / 2)))
        self.text = textcontent
        self.textcolor = textcolor
        self.reltextsize = reltextsize
        self.textsize = relToAbs(reltextsize)
        self.rect = self.surface.get_rect()
        self.relposx, self.relposy = relpos[0], relpos[1]
        self.relwidth, self.relheight = relwidth, relheight
        self.rect.x, self.rect.y = relToAbs(relpos[0]), relToAbs(relpos[1])
        self.textrect = getTextRect(textcontent, self.textsize)
        self.anchor = anchor
        if self.anchor == "center":
            self.textrect.center = self.rect.center
        elif self.anchor == "right":
            self.textrect.centery = self.rect.centery
            self.textrect.right = self.rect.right
        elif self.anchor == "left":
            self.textrect.centery = self.rect.centery
            self.textrect.left = self.rect.left

    def update(self):
        self.image = pygame.transform.scale(self.surface, relToAbsDual(self.relwidth, self.relheight))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = relToAbs(self.relposx), relToAbs(self.relposy)
        self.textsize = relToAbs(self.reltextsize)
        self.textrect = getTextRect(self.text, self.textsize)
        if self.anchor == "center":
            self.textrect.center = self.rect.center
        elif self.anchor == "right":
            self.textrect.centery = self.rect.centery
            self.textrect.right = self.rect.right
        elif self.anchor == "left":
            self.textrect.centery = self.rect.centery
            self.textrect.left = self.rect.left
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sethover()

    def sethover(self):
        self.image = pygame.transform.scale(self.hoversurface, relToAbsDual(self.relwidth, self.relheight))

    def draw(self, window):
        window.blit(self.image, self.rect)
        renderText(window=window, text=self.text, position=self.textrect, color=self.textcolor, size=self.textsize)
