from typing import Sequence, Union, List, Optional

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

import utils

class cameraScene(Surface):

    def __init__(self, size, camera, flags=None, depth=None, masks=None):
        Surface.__init__(size, flags, depth, masks)
        self.camera = camera

    def blit(self, source: Surface, dest: Union[Sequence[float], Rect], area: Optional[Rect] = ...,
             special_flags: int = ...) -> Rect:
        if utils.check_collision(self.camera, source.get_rect()):
            return super().blit(source, dest, area, special_flags)

    def render(self, render_rect=None):
        if render_rect is None:
            render_rect = self.camera
        return self.subsurface(render_rect)
