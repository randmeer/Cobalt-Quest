import pygame

from octagon.utils import render_text, get_text_rect, gradient_rect, rta_dual, rta_width, rta_height, set_anchor_point, var


class Button(pygame.sprite.Sprite):
    def __init__(self, relsize, text, relpos, textcolor=(57, 74, 80), textsize=5, visible=True, border=1, textanchor="center", anchor="topleft", gradients=False, tags=None,
                 bordergradientcolors=((255, 141, 141), (141, 187, 255)), bordercolor=var.GRAYSHADES[3],
                 bordergradientcolors_hover=((255, 141, 141), (141, 187, 255)), bordercolor_hover=var.GRAYSHADES[4],
                 bordergradientcolors_press=((255, 200, 200), (200, 200, 255)), bordercolor_press=var.GRAYSHADES[1],
                 innergradientcolors=((255, 141, 141), (141, 187, 255)), innercolor=var.GRAYSHADES[1],
                 innergradientcolors_hover=((255, 141, 141), (141, 187, 255)), innercolor_hover=var.GRAYSHADES[2],
                 innergradientcolors_press=((255, 200, 200), (200, 200, 255)), innercolor_press=var.GRAYSHADES[3]):
        pygame.sprite.Sprite.__init__(self)
        self.relw, self.relh = relsize[0], relsize[1]
        self.relposx, self.relposy = relpos[0], relpos[1]
        self.text = text
        self.textcolor = textcolor
        self.textanchor = textanchor
        self.textsize = textsize
        self.anchor = anchor
        self.hover = self.press = False
        self.visible = visible

        if tags is None:
            self.tags = []
        else:
            self.tags = tags

        size = rta_dual(self.relw, self.relh)
        self.surface = pygame.Surface(size)
        self.hoversurface = pygame.Surface(size)
        self.presssurface = pygame.Surface(size)
        self.innerarea = pygame.Surface((rta_width(self.relw) - border * 2, rta_height(self.relh) - border * 2))

        if gradients:
            self.surface.blit(gradient_rect(self.surface.get_width(), self.surface.get_height(), bordergradientcolors), (0, 0))
            self.hoversurface.blit(gradient_rect(self.hoversurface.get_width(), self.hoversurface.get_height(), bordergradientcolors_hover), (0, 0))
            self.presssurface.blit(gradient_rect(self.presssurface.get_width(), self.presssurface.get_height(), bordergradientcolors_press), (0, 0))
            self.innerarea.blit(gradient_rect(self.innerarea.get_width(), self.innerarea.get_height(), innergradientcolors), (0, 0))
            self.surface.blit(self.innerarea, (border, border))
            self.innerarea.blit(gradient_rect(self.innerarea.get_width(), self.innerarea.get_height(), innergradientcolors_hover), (0, 0))
            self.hoversurface.blit(self.innerarea, (border, border))
            self.innerarea.blit(gradient_rect(self.innerarea.get_width(), self.innerarea.get_height(), innergradientcolors_press), (0, 0))
            self.presssurface.blit(self.innerarea, (border, border))
        else:
            self.surface.fill(bordercolor)
            self.hoversurface.fill(bordercolor_hover)
            self.presssurface.fill(bordercolor_press)
            self.innerarea.fill(innercolor)
            self.surface.blit(self.innerarea, (border, border))
            self.innerarea.fill(innercolor_hover)
            self.hoversurface.blit(self.innerarea, (border, border))
            self.innerarea.fill(innercolor_press)
            self.presssurface.blit(self.innerarea, (border, border))

        self.image = self.surface
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = rta_width(relpos[0]), rta_height(relpos[1])
        pos = rta_dual(self.relposx, self.relposy)
        set_anchor_point(self.rect, pos, self.anchor)

        render_text(window=self.surface, text=self.text, pos=self.textposition(), color=self.textcolor, size=self.textsize)
        render_text(window=self.hoversurface, text=self.text, pos=self.textposition(), color=self.textcolor, size=self.textsize)
        render_text(window=self.presssurface, text=self.text, pos=self.textposition(), color=self.textcolor, size=self.textsize)

    def textposition(self):
        textrect = get_text_rect(self.text, self.textsize)
        size = (rta_width(self.relw), rta_height(self.relh))
        if self.textanchor == "center":
            return size[0]/2-textrect.width/2, size[1]/2-textrect.height/2
        elif self.textanchor == "right":
            return size[0]-textrect.width, size[1]/2-textrect.height/2
        elif self.textanchor == "left":
            return 0, size[1]/2-textrect.height/2

    def update(self):
        if self.press:
            self.image = self.presssurface
        elif self.rect.collidepoint((pygame.mouse.get_pos()[0] / (var.res_size[0] / var.SIZE[0]),
                                     pygame.mouse.get_pos()[1] / (var.res_size[1] / var.SIZE[1]))) or self.hover:
            self.image = self.hoversurface
        else:
            self.image = self.surface

    def set_hovered(self, hover):
        self.hover = hover

    def set_pressed(self, press):
        self.press = press

    def set_visible(self, visible):
        self.visible = visible

    def draw(self, surface):
        if not self.visible:
            return
        surface.blit(self.image, self.rect)
        # render_text(window=surface, text=self.text, pos=self.textrect, color=self.textcolor, size=self.textsize)
