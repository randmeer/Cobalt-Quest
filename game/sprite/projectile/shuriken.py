from octagon.utils import img
from octagon.utils.static import angle_deg, conv_deg_rad
from octagon.environment.object.projectile import Projectile

from game.sprite.particle.explosion import ExplosionPts


class Shuriken(Projectile):
    def __init__(self, env, args=None):

        # arguments
        # [i.hitbox.centerx, i.hitbox.centery], i.radians, [enchantments]

        if args is None:
            args = [None, None, ["explosion"]]

        pos = args[0]
        radians = args[1]
        self.enchantments = args[2]

        exploding = False
        for i in self.enchantments:
            if i == "explosion":
                exploding = True

        if pos is None and env.cooldown > 0:
            return
        # shuriken was thrown by player -> get data from env
        if pos is None and radians is None:
            pos = env.player.hitbox.center
            radians = conv_deg_rad(angle_deg(pos, env.mousepos))
            env.hud.use_slot()
            env.cooldown = 0.5

        Projectile.__init__(self, env=env, pos=pos, radians=radians, rotating=True, rotation_increment=360,
                            velocity=3, exploding=exploding, image=img.item["shuriken"], explosion_particles=ExplosionPts)

    def update(self):
        self.projectile_update()

    def save(self):
        if self.collided:
            return False
        else:
            return [[self.hitbox.centerx, self.hitbox.centery], self.radians, self.enchantments]
