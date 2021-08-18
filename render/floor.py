import pygame
from typing import Sequence, Union, List, Optional
from pygame.surface import Surface

import utils

class CameraObject(pygame.Rect):

    def __init__(self, height, width, top, left, to_follow=None, no_border=True, scene_size=None):
        pygame.Rect.__init__(left, top, width, height)
        self.to_follow = to_follow
        self.no_border = no_border
        self.scene_size = scene_size

    def follow(self, to_follow=None):
        """
        overrride if necessary
        :param to_follow: rect the camera should follow
        """
        if to_follow is not None:
            self.center = to_follow.center
        if self.to_follow is not None:
            self.center = self.to_follow.center


class CameraScene(Surface):

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
