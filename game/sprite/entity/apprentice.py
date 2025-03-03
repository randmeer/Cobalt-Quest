from octagon.utils.img import Texture
from octagon.environment.object.entity import Entity
from octagon.utils import img

from game.sprite.particle.entity import Footstep, Die1, Die2, Damage, ManaDrop


class Apprentice(Entity):

    def __init__(self, env, args=None):

        # args
        # [i.position[0], i.position[1]], i.health, i.weapon, target

        pos = args[0]
        health = args[1]
        weapon = args[2]
        target = args[3]

        Entity.__init__(self, env=env, priority=2, automove=True, position=pos, automove_target=target, velocity=25,
                        footstep_particle=Footstep, death_particles=[Die1, Die2, ManaDrop], damage_particle=Damage,
                        animation_textures=[Texture(img.entity["apprentice_up"], 0.2),
                                            Texture(img.entity["apprentice_down"], 0.2),
                                            Texture(img.entity["apprentice_right"], 0.2),
                                            Texture(img.entity["apprentice_left"], 0.2),
                                            Texture(img.entity["apprentice_idle"], 0.4)])
        self.weapon = weapon
        if health is not None:
            self.health = health
        else:
            self.health = 100
        self.velocity = 25
        self.attackcooldown = 1

    def update(self):
        self.move()
        self.entity_update()
        #if self.attackcooldown < 0:
        #    projectiles.append(Fireball(pos=self.hitbox.center, radians=conv_deg_rad(angle_deg(self.hitbox.center, player.hitbox.center))))
        #    self.attackcooldown = 10
        #self.attackcooldown -= delta_time

    def save(self):
        if self.auto_move:
            target = self.am_path[len(self.am_path)-1]
        else:
            target = None
        return [[self.position[0], self.position[1]], self.health, self.weapon, target]