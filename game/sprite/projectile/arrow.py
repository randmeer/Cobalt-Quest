from octagon.utils import img
from octagon.utils.static import angle_deg, conv_deg_rad
from octagon.environment.object.projectile import Projectile

from game.sprite.particle.explosion import ExplosionPts


class Arrow(Projectile):
    def __init__(self, env, args=None):

        # arguments
        # [i.hitbox.centerx, i.hitbox.centery], i.radians, [enchantments]

        if args is None:
            args = [None, None, []]

        pos = args[0]
        radians = args[1]
        self.enchantments = args[2]

        exploding = False
        for i in self.enchantments:
            if i == "explosion":
                exploding = True

        if pos is None and env.cooldown > 0:
            return

        # TODO: search for arrows in inventory, if there are none return, if there are any, use 1
        # That could be implemented into the hud object?

        env.cooldown = 0.5
        if not pos:
            pos = env.player.hitbox.center
        if not radians:
            radians = conv_deg_rad(angle_deg(pos, env.mousepos))
        Projectile.__init__(self, env=env, pos=pos, radians=radians, velocity=7, image=img.item["arrow"], explosion_particles=ExplosionPts, exploding=exploding)

    def update(self):
        self.projectile_update()

    def save(self):
        if self.collided:
            return False
        else:
            return [[self.hitbox.centerx, self.hitbox.centery], self.radians, self.enchantments]
