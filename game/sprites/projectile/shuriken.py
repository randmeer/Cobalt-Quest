from octagon.utils import img
from octagon.sprites.projectile import Projectile

from game.sprites.particle.explosion import ExplosionPts


class Shuriken(Projectile):
    def __init__(self, particles, pos, radians, velocity=3, exploding=False):
        Projectile.__init__(self, particles=particles, pos=pos, radians=radians, rotating=True, rotation_increment=360,
                            velocity=velocity, exploding=exploding, image=img.item["shuriken"], explosion_particles=ExplosionPts)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
