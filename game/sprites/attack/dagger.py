from octagon.sprites.attack import Attack
from octagon.utils.texture import Texture
from octagon.utils import img


class Swing(Attack):
    def __init__(self, mousepos, playerpos):
        Attack.__init__(self, mousepos=mousepos, playerpos=playerpos, image=Texture(image=img.misc["attack"]["swing"], frametime=0.025, single_run=True, set_height=16))
        self.damage = 10


class Stab(Attack):
    def __init__(self, mousepos, playerpos):
        Attack.__init__(self, mousepos=mousepos, playerpos=playerpos, offset=90, image=Texture(image=img.misc["attack"]["stab"], frametime=0.025, single_run=True, set_height=8))
        self.damage = 5
