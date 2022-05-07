import random

from octagon.sprites.attack import Attack
from octagon.utils.img import Texture
from octagon.utils import img


class Slash(Attack):
    def __init__(self, env):
        if env.cooldown > 0:
            return
        env.cooldown += 0.5
        slash = random.choice(["slash_left", "slash_right"])
        Attack.__init__(self, env=env, image=Texture(image=img.misc["attack"][slash], frametime=0.025, single_run=True, set_height=20))
        self.damage = 10


class Vortex(Attack):
    def __init__(self, env):
        if env.cooldown > 0:
            return
        env.cooldown += 5
        Attack.__init__(self, env=env, displacement=0, image=Texture(image=img.misc["attack"]["vortex"], frametime=0.025, single_run=True, set_height=50))
        self.damage = 30
