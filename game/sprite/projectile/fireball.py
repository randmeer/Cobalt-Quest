from octagon.utils import img
from octagon.environment.object.projectile import Projectile

from game.sprite.particle.explosion import ExplosionPts


class Fireball(Projectile):
    def __init__(self, particles, pos, radians, sender="entity", homing=False, homing_target=None,  velocity=1.5):
        Projectile.__init__(self, particles=particles, pos=pos, radians=radians, rotating=True, velocity=velocity, image=
        img.item["fireball"], homing=homing, homing_target=homing_target, sender=sender, exploding=True, explosion_particles=ExplosionPts)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
