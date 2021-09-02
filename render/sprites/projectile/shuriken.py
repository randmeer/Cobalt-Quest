from utils.images import item_tx
from render.sprites.projectile import Projectile
from render.sprites import particle_cloud

class Shuriken(Projectile):
    def __init__(self, pos, radians, velocity=3, exploding=False):
        Projectile.__init__(self, pos=pos, radians=radians, rotating=True, rotation_increment=360, velocity=velocity, exploding=exploding, image=item_tx["shuriken"])

    def update(self, delta_time, blocks, entitys, particles):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles)
        if self.exploding:
            particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=5,
                                                          particlesize=(1, 1), color=(200, 100, 0), density=1,
                                                          velocity=50,
                                                          distribution=0.7, colorvariation=5))
