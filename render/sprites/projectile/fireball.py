from utils.images import images
from render.sprites.projectile import Projectile
from render.sprites import particle_cloud

class Fireball(Projectile):
    def __init__(self, pos, sender="entity", homing=False, homing_target=None, radians=0, velocity=1.5):
        Projectile.__init__(self, pos=pos, radians=radians, rotating=True, velocity=velocity, image=images["fireball"],
                            homing=homing, homing_target=homing_target, sender=sender, exploding=True)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=5,
                                                      particlesize=(1, 1), color=(200, 100, 0), density=1,
                                                      velocity=30,
                                                      distribution=0.7, colorvariation=5))
        particles.append(particle_cloud.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=5,
                                                      particlesize=(1, 1), color=(220, 20, 0), density=1,
                                                      velocity=100,
                                                      distribution=0.7, colorvariation=20))
