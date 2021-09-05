from utils.texture import Texture
from render.sprites.entity import Entity
from render.sprites.projectile.fireball import Fireball

from utils import conv_deg_rad, angle_deg

class Apprentice(Entity):

    def __init__(self, pos, health=None, weapon=None):
        Entity.__init__(self, auto_movement=True, position=pos)
        self.priority = 2
        self.weapon = weapon
        if health is not None:
            self.health = health
        else:
            self.health = 100
        self.tex_up = Texture("resources/textures/apprentice_animation_up.png")
        self.tex_down = Texture("resources/textures/apprentice_animation_down.png")
        self.tex_right = Texture("resources/textures/apprentice_animation_right.png")
        self.tex_left = Texture("resources/textures/apprentice_animation_left.png")
        self.tex_idle = Texture("resources/textures/apprentice_animation_idle.png")
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.velocity = 5
        self.attackcooldown = 1

    def update(self, webs, blocks, particles, projectiles, player, delta_time):
        if self.dead: return
        self.entity_update(webs=webs, blocks=blocks, particles=particles, delta_time=delta_time)
        if self.attackcooldown < 0:
            projectiles.append(Fireball(pos=self.hitbox.center, radians=conv_deg_rad(angle_deg(self.hitbox.center, player.hitbox.center))))
            self.attackcooldown = 10
        self.attackcooldown -= delta_time
