import random

from octagon.environment.object.attack import Attack
from octagon.utils.img import Texture
from octagon.utils import img


class Punch(Attack):
    def __init__(self, env):
        punch = random.choice(["punch_left", "punch_right"])
        Attack.__init__(self, env=env, offset=90, image=Texture(image=img.misc["attack"][punch], frametime=0.025, single_run=True, set_height=8))
        self.damage = 5


class Block(Attack):
    def __init__(self, env):
        # TODO: block animation
        Attack.__init__(self, env=env, offset=90, image=Texture(image=img.misc["attack"]["block"], frametime=0.025, single_run=True, set_height=8))
        self.damage = 0
