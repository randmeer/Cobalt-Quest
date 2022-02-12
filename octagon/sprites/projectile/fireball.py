from octagon.utils import img
from octagon.sprites.projectile import Projectile


class Fireball(Projectile):
    def __init__(self, particles,  pos, sender="entity", homing=False, homing_target=None, radians=0, velocity=1.5):
        Projectile.__init__(self, particles=particles, pos=pos, radians=radians, rotating=True, velocity=velocity, image=
        img.item["fireball"], homing=homing, homing_target=homing_target, sender=sender, exploding=True)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
