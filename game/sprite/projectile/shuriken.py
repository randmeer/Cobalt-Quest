from octagon.utils import img
from octagon.utils.static import angle_deg, conv_deg_rad
from octagon.sprites.projectile import Projectile

from game.sprite.particle.explosion import ExplosionPts


class Shuriken(Projectile):
    def __init__(self, env, pos=None, radians=None, exploding=False):
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
