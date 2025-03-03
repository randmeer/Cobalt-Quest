from octagon.environment.object.attack import Attack
from octagon.utils.img import Texture
from octagon.utils import img


class Swing(Attack):
    def __init__(self, env):
        if env.cooldown > 0:
            return
        env.cooldown += 0.5
        Attack.__init__(self, env=env, image=Texture(image=img.misc["attack"]["swing"], frametime=0.025, single_run=True, set_height=16))
        self.damage = 20


class Stab(Attack):
    def __init__(self, env):
        if env.cooldown > 0:
            return
        env.cooldown += 0.25
        Attack.__init__(self, env=env, offset=90, image=Texture(image=img.misc["attack"]["stab"], frametime=0.025, single_run=True, set_height=8))
        self.damage = 10
