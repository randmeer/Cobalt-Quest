from utils.texture import Texture
from render.sprites.entity import Entity
from render.sprites.projectile.fireball import Fireball
from utils import img, conv_deg_rad, angle_deg

class Apprentice(Entity):

    def __init__(self, particles, pos, health=None, weapon=None, floorjson=None):
        self.priority = 2
        Entity.__init__(self, particles, auto_movement=True, position=pos, floorjson=floorjson)
        self.weapon = weapon
        if health is not None:
            self.health = health
        else:
            self.health = 100
        self.tex_up = Texture(img.entity["apprentice_up"], 0.2)
        self.tex_down = Texture(img.entity["apprentice_down"], 0.2)
        self.tex_right = Texture(img.entity["apprentice_right"], 0.2)
        self.tex_left = Texture(img.entity["apprentice_left"], 0.2)
        self.tex_idle = Texture(img.entity["apprentice_idle"], 0.4)
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
