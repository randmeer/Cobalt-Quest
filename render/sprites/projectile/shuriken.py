from utils import img
from render.sprites.projectile import Projectile

class Shuriken(Projectile):
    def __init__(self, particles, pos, radians, velocity=3, exploding=False):
        Projectile.__init__(self, particles=particles, pos=pos, radians=radians, rotating=True, rotation_increment=360, velocity=velocity, exploding=exploding, image=img.item["shuriken"])

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
        self.spark_emitter.update_emitter([self.rect.centerx, self.rect.centery])
        if self.collided:
            self.spark_emitter.stop_emitting()
