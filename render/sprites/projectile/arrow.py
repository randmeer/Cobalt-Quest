from utils.images import item_tx
from render.sprites.projectile import Projectile

class Arrow(Projectile):
    def __init__(self, pos, radians, velocity=5):
        Projectile.__init__(self, pos=pos, radians=radians, velocity=velocity, image=item_tx["arrow"])

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
