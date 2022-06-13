import pygame

from octagon.utils import rta_dual, render_text, get_text_rect, set_anchor_point, get_outline_mask, var


class Label(pygame.sprite.Sprite):
    """
    Can be used as a normal label, but offers a variety of
    other usecases, such as buttons, selections, textboxes ect.

    > button: get rect.collidepoint with the label's rect
    > selection: call set_outline() on click
    > textbox: call text_input() on keystroke
    """
    def __init__(self, text, relpos, color=(var.GRAYSHADES[0]), textsize=5, anchor="center", h_event=False,
                 h_color=(var.GRAYSHADES[0]), default_outlined=False, h_outlined=False, outlinecolor=(
            var.GRAYSHADES[0]),
                 visible=True, tags=None):
        pygame.sprite.Sprite.__init__(self)
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
        self.text = text
        self.color = color
        self.hovercolor = h_color
        self.hoverevent = h_event
        self.textsize = textsize
        self.relpos = relpos
        self.anchor = anchor
        self.surface = self.clone = self.outlinesurf = pygame.Surface
        self.hoverbool = self.outlinebool = False
        self.visible = visible
        self.default_outlined = default_outlined
        self.hoveroutlined = h_outlined
        self.outlinecolor = outlinecolor
        self.surface = None
        self.hoversurf = None
        self.outlinesurf = None
        self.render()
        if self.hoverevent:
            self.render_hover()
        if self.default_outlined or self.hoveroutlined:
            self.render_outline()

    def render(self):
        self.rect = get_text_rect(self.text, self.textsize)
        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        render_text(window=self.surface, text=self.text, pos=(0, 0), color=self.color, size=self.textsize)
        pos = rta_dual(self.relpos[0], self.relpos[1])
        set_anchor_point(self.rect, pos, self.anchor)
        self.image = self.surface

    def render_hover(self):
        self.hoversurf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        render_text(window=self.hoversurf, text=self.text, pos=(0, 0), color=self.hovercolor, size=self.textsize)

    def render_outline(self):
        self.clone = pygame.Surface((self.surface.get_width() + 4, self.surface.get_height() + 4))
        self.clone.fill((0, 0, 0))
        self.outlinesurf = pygame.Surface((0, 0))
        self.outlinesurf = get_outline_mask(self.clone)

    def set_outline(self, outline):
        self.default_outlined = outline

    def set_visible(self, visible):
        self.visible = visible

    def update(self):
        self.hoverbool = self.outlinebool = False
        self.image = self.surface
        if self.hoverevent:
            if self.rect.collidepoint((pygame.mouse.get_pos()[0] / (var.res_size[0] / var.SIZE[0]), pygame.mouse.get_pos()[1] / (
                    var.res_size[1] / var.SIZE[1]))):
                if self.hoveroutlined:
                    self.hoverbool = self.outlinebool = True
                else:
                    self.hoverbool = True
                    self.image = self.hoversurf
        if self.default_outlined:
            self.outlinebool = True

    def draw(self, surface):
        if not self.visible:
            return
        if self.outlinebool:
            surface.blit(self.outlinesurf, (self.rect.x-2, self.rect.y-2))
        surface.blit(self.image, self.rect)

    def text_input(self, key_str, fix_chars, max_chars):
        if key_str == "backspace":
            if not len(self.text) <= fix_chars:
                self.text = self.text[:-1]
        if not len(self.text) >= fix_chars+max_chars:
            if key_str == "space":
                self.text = self.text + " "
            elif key_str == "left shift" or key_str == "right shift" or key_str == "tab" or key_str == "caps lock" or key_str == "left meta" \
                    or key_str == "right meta" or key_str == "left alt" or key_str == "right alt" or key_str == "left ctrl" or key_str == "right ctrl" \
                    or key_str == "return" or key_str == "up" or key_str == "down" or key_str == "left" or key_str == "right" or key_str == "backspace":
                pass
            else:
                key = pygame.key.get_pressed()
                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
                    key_str = key_str.upper()
                    if key_str == "9":
                        key_str = "("
                    elif key_str == "0":
                        key_str = ")"
                    elif key_str == "-":
                        key_str = "_"
                self.text = self.text + key_str
        self.render()

