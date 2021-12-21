from utils.images import images
from render.sprites.projectile import Projectile

class Fireball(Projectile):
    def __init__(self, particles,  pos, sender="entity", homing=False, homing_target=None, radians=0, velocity=1.5):
        Projectile.__init__(self, particles=particles, pos=pos, radians=radians, rotating=True, velocity=velocity, image=images["fireball"],
                            homing=homing, homing_target=homing_target, sender=sender, exploding=True)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.projectile_update(delta_time=delta_time, blocks=blocks, entitys=entitys, particles=particles, player=player, projectiles=projectiles, melee=melee)
        # TODO: use emitters for this
        # particles.append(particle.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=5,
        #                                               particlesize=1, color=(200, 100, 0), density=1,
        #                                               velocity=0.1,
        #                                               distribution=0.7, colorvariation=5))
        # particles.append(particle.ParticleCloud(center=(self.rect.centerx, self.rect.centery), radius=5,
        #                                               particlesize=1, color=(220, 20, 0), density=1,
        #                                               velocity=0.2,
        #                                               distribution=0.7, colorvariation=20))
