import pygame
from utils import globs, renderText, getTextRect, gradientRect, rta_dual, rta_width, rta_height, set_anchor_point

class Button(pygame.sprite.Sprite):
    def __init__(self, relwidth, relheight, textcontent, relpos, textcolor=(75, 75, 75), reltextsize=0.1,
                 border=1, bordercolor=(255, 255, 255), innercolor=(194, 205, 209), textanchor="center",
                 hovergradient=((255, 141, 141), (141, 187, 255)), hovercolor=(214, 225, 229), anchor="topleft"):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface(rta_dual(relwidth, relheight))
        self.surface.fill(bordercolor)
        self.innerarea = pygame.Surface((rta_width(relwidth) - border * 2, rta_height(relheight) - border * 2))
        self.innerarea.fill(innercolor)
        self.surface.blit(self.innerarea, (border, border))
        self.image = self.surface
        self.hoversurface = pygame.Surface(rta_dual(relwidth, relheight))
        self.hoversurface.blit(gradientRect(self.hoversurface.get_width(), self.hoversurface.get_height(), hovergradient[0], hovergradient[1]), (0, 0))
        self.innerarea.fill(hovercolor)
        self.hoversurface.blit(self.innerarea, (border, border))
        self.text = textcontent
        self.textcolor = textcolor
        self.reltextsize = reltextsize
        #self.textsize = relToAbsHeight(reltextsize)
        self.textsize = 5
        self.rect = self.surface.get_rect()
        self.relposx, self.relposy = relpos[0], relpos[1]
        self.relwidth, self.relheight = relwidth, relheight
        self.rect.x, self.rect.y = rta_width(relpos[0]), rta_height(relpos[1])
        self.textrect = getTextRect(textcontent, self.textsize)
        self.textanchor = textanchor
        self.anchor = anchor
        self.textanchorupdate()

    def textanchorupdate(self):
        if self.textanchor == "center":
            self.textrect.center = self.rect.center
        elif self.textanchor == "right":
            self.textrect.centery = self.rect.centery
            self.textrect.right = self.rect.right
        elif self.textanchor == "left":
            self.textrect.centery = self.rect.centery
            self.textrect.left = self.rect.left

    def update(self):
        self.image = pygame.transform.scale(self.surface, rta_dual(self.relwidth, self.relheight))
        self.rect = self.image.get_rect()
        pos = rta_dual(self.relposx, self.relposy)
        set_anchor_point(self.rect, pos, self.anchor)
        #self.textsize = relToAbsHeight(self.reltextsize)
        self.textsize = 5
        self.textrect = getTextRect(self.text, self.textsize)
        self.textanchorupdate()
        if self.rect.collidepoint((pygame.mouse.get_pos()[0] / (globs.res_size[0]/globs.SIZE[0]), pygame.mouse.get_pos()[1] / (globs.res_size[1]/globs.SIZE[1]))):
            self.sethover()

    def sethover(self):
        self.image = pygame.transform.scale(self.hoversurface, rta_dual(self.relwidth, self.relheight))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        renderText(window=surface, text=self.text, position=self.textrect, color=self.textcolor, size=self.textsize)
