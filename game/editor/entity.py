import random
import pygame

from octagon.utils import dual_rect_anchor, set_anchor_point, debug_outlines, mask_overlay, cord_to_block, var, img
from octagon.utils.img import Texture
from octagon.sprites.entity import Entity

from game.sprite.particle.entity import Damage, Dash, Footstep

import random
import pygame

from octagon.utils.img import Texture
from octagon.utils import dual_rect_anchor, set_anchor_point, debug_outlines, mask_overlay, cord_to_block, var
from octagon.utils.static import vector_from_points, list_round


class EditorEntity(pygame.sprite.Sprite):
    def __init__(self, env, priority=2, max_health=100, health=100, damage_overlay_on=True, immune_to_web=False,
                 hurt_cooldown=0.5, position=(0, 0), rotation=0, velocity=25, hitboxsize=(16, 16), hitboxanchor="midbottom",
                 automove=False, automove_type='wander', automove_target=None,
                 footstep_particle: type = None, death_particles: list[type] = None, damage_particle: type = None,
                 animation_textures: list[Texture] = None):
        pygame.sprite.Sprite.__init__(self)
        self.env = env
        self.tex_down = self.tex_up = self.tex_left = self.tex_right = self.tex_idle = None
        self.priority = priority
        self.position = list(position)
        self.hc = 0
        self.hc_max = hurt_cooldown
        self.hc_ani = 0.25
        self.immune_to_web = immune_to_web
        self.damage_overlay_on = damage_overlay_on
        self.health = health
        self.max_health = max_health
        self.rotation = rotation
        self.velocity = velocity

        self.tex_up = animation_textures[0]
        self.tex_down = animation_textures[1]
        self.tex_right = animation_textures[2]
        self.tex_left = animation_textures[3]
        self.tex_idle = animation_textures[4]
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect((0, 0), hitboxsize)
        self.hitboxanchor = hitboxanchor

        self.move_vector = None
        self.auto_move = automove
        self.am_type = automove_type
        self.FootstepPt = footstep_particle
        self.DeathPt = death_particles
        self.DamagePt = damage_particle

    def save():
        pass

    def _move_update_rect(self):
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def draw(self, surface):
        image = self.image
        if var.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect, anchor=self.hitboxanchor)
            pygame.draw.circle(surface, (255, 0, 0), (surface.get_width() / 2, surface.get_height() / 2), 2)

        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))

class Player(EditorEntity):
    def __init__(self, env, pos, health=100, mana=100):
        EditorEntity.__init__(self, env, priority=1, position=pos, health=health, velocity=50, max_health=100,
                        footstep_particle=Footstep, damage_particle=Damage, hitboxsize=(12, 16), hitboxanchor="midbottom",
                        animation_textures=[
                            Texture(img.entity["player_up"], 0.1),
                            Texture(img.entity["player_down"], 0.1),
                            Texture(img.entity["player_right"], 0.1),
                            Texture(img.entity["player_left"], 0.1),
                            Texture(img.entity["player_idle"], 0.4)
                        ])
        self.mana = mana
        self.max_mana = 100
        self.dashing = 0

    def update(self):
        self.entity_update()



class Apprentice(EditorEntity):

    def __init__(self, env, args=None):

        # args
        # [i.position[0], i.position[1]], i.health, i.weapon, target

        pos = args[0]
        health = args[1]
        weapon = args[2]
        target = args[3]

        EditorEntity.__init__(self, env=env, priority=2, automove=True, position=pos, automove_target=target, velocity=25,
                        footstep_particle=Footstep, death_particles=[], damage_particle=Damage,
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
        self.entity_update()
        #if self.attackcooldown < 0:
        #    projectiles.append(Fireball(pos=self.hitbox.center, radians=conv_deg_rad(angle_deg(self.hitbox.center, player.hitbox.center))))
        #    self.attackcooldown = 10
        #self.attackcooldown -= delta_time

    def save(self):
        return [[self.position[0], self.position[1]], self.health, self.weapon, None]