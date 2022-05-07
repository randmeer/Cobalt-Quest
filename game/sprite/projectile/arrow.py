from octagon.utils import img
from octagon.utils.static import angle_deg, conv_deg_rad
from octagon.sprites.projectile import Projectile


class Arrow(Projectile):
    def __init__(self, env, pos=None, radians=None):
        if pos is None and env.cooldown > 0:
            return

        # TODO: search for arrows in inventory, if there are none return, if there are any, use 1
        # That could be implemented into the hud object?
        env.cooldown = 0.5
        if not pos:
            pos = env.player.hitbox.center
        if not radians:
            radians = conv_deg_rad(angle_deg(pos, env.mousepos))
        Projectile.__init__(self, env=env, pos=pos, radians=radians, velocity=7, image=img.item["arrow"])

    def update(self):
        self.projectile_update()
