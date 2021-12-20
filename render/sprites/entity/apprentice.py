from utils.texture import Texture
from render.sprites.entity import Entity
from render.sprites.projectile.fireball import Fireball

from utils import conv_deg_rad, angle_deg

class Apprentice(Entity):

    def __init__(self, particles, pos, health=None, weapon=None, floorjson=None):
        self.priority = 2
        Entity.__init__(self, particles, auto_movement=True, position=pos, floorjson=floorjson)
        self.weapon = weapon
        if health is not None:
            self.health = health
        else:
            self.health = 100
        self.tex_up = Texture("apprentice_animation_up")
        self.tex_down = Texture("apprentice_animation_down")
        self.tex_right = Texture("apprentice_animation_right")
        self.tex_left = Texture("apprentice_animation_left")
        self.tex_idle = Texture("apprentice_animation_idle")
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.velocity = 25
        self.attackcooldown = 1

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        self.entity_update(blocks=blocks, particles=particles, delta_time=delta_time, entitys=entitys, player=player)
        #if self.attackcooldown < 0:
        #    projectiles.append(Fireball(pos=self.hitbox.center, radians=conv_deg_rad(angle_deg(self.hitbox.center, player.hitbox.center))))
        #    self.attackcooldown = 10
        #self.attackcooldown -= delta_time
