from pygame import Rect

class CameraObject(Rect):

    def __init__(self, height, width, top, left, to_follow=None, no_border=True, scene_size=None):
        Rect.__init__(left, top, width, height)
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

