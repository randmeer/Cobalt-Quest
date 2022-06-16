import random
import pygame

from octagon.utils import dual_rect_anchor, set_anchor_point, debug_outlines, mask_overlay, cord_to_block, var, img
from octagon.utils.img import Texture
from octagon.sprites.entity import Entity

from game.sprite.particle.entity import Damage, Dash, Footstep

class EditorEntity(Entity):

    def __init__(self, env, priority=2, max_health=100, health=100, damage_overlay_on=True, immune_to_web=False,
                 hurt_cooldown=0.5, position=(0, 0), rotation=0, velocity=25, hitboxsize=(16, 16), hitboxanchor="midbottom", 
                 footstep_particle: type = None, death_particles: tuple[type, type] = None, damage_particle: type = None):
        Entity.__init__(self, env, priority=priority, max_health=max_health, health=health, damage_overlay_on=damage_overlay_on, immune_to_web=immune_to_web,
                 hurt_cooldown=hurt_cooldown, position=position, rotation=rotation, velocity=velocity, hitboxsize=hitboxsize, hitboxanchor=hitboxanchor, 
                 footstep_particle = footstep_particle, death_particles = death_particles, damage_particle = damage_particle)
        self.env = env
        self.tex_down = self.tex_up = self.tex_left = self.tex_right = self.tex_idle = None
        self.priority = priority
        self.offset = [0, 0]
        self.position = list(position)
        self.hc = 0
        self.hc_max = hurt_cooldown
        self.hc_ani = 0.25
        self.immune_to_web = immune_to_web
        self.damage_overlay_on = damage_overlay_on
        self.health = health
        self.max_health = max_health
        self.speed_multiplier = 1
        self.rotation = rotation
        self.velocity = velocity
        self.hitbox = pygame.Rect((0, 0), hitboxsize)
        self.hitboxanchor = hitboxanchor
        self.FootstepPt = footstep_particle
        if self.FootstepPt is not None:
            self.footstep_emitter = self.FootstepPt(env=self.env, pos=(self.hitbox.midbottom[0], self.hitbox.midbottom[1] - 2), priority=self.priority + 1)
            self.env.particles.append(self.footstep_emitter)
        self.DeathPt = death_particles
        self.DamagePt = damage_particle

    def _automove(self):
        raise Eception("cannot automove editor entity")


    def _am_settarget(self):
        raise Eception("cannot amtarget editor entity")


    def _am_newpath(self, target=None):
        raise Eception("cannot newpath editor entity")

class Player(EditorEntity):
    def __init__(self, env, pos, health=100, mana=100):
        EditorEntity.__init__(self, env, priority=1, position=pos, health=health, velocity=25, max_health=100,
                        footstep_particle=Footstep, damage_particle=Damage)
        self.mana = mana
        self.max_mana = 100
        self.dashing = 0
        self.tex_up = Texture(img.entity["player_up"], 0.1)
        self.tex_down = Texture(img.entity["player_down"], 0.1)
        self.tex_right = Texture(img.entity["player_right"], 0.1)
        self.tex_left = Texture(img.entity["player_left"], 0.1)
        self.tex_idle = Texture(img.entity["player_idle"], 0.4)
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

    def update(self):
        if self.health <= 0: return
        self.image = self.tex_idle.get()
        self.entity_update()
        if self.offset != [0, 0]:
            play_sound('step')

    def dash(self):
        pass

    def add1mana(self):
        if not self.mana >= self.max_mana:
            self.mana += 1

    def addmana(self, amount):
        if self.mana + amount > self.max_mana:
            self.mana = self.max_mana
            return False
        else:
            self.mana += amount
            return True

    def submanga(self, amount):
        if self.mana - amount < 0:
            return False
        else:
            self.mana -= amount
            return True


class Apprentice(EditorEntity):

    def __init__(self, env, pos, health=None, weapon=None, target=None):
        EditorEntity.__init__(self, env=env, priority=2, position=pos)
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

    def update(self):
        self.entity_update()