import pygame

from octagon.utils import play_sound, img
from octagon.utils.texture import Texture
from octagon.sprites.entity import Entity
from octagon.sprites.particle import entity


class Player(Entity):
    def __init__(self, particles, pos, health=100, mana=100):
        self.priority = 1
        self.mana = mana
        self.max_mana = 100
        self.position = pos
        self.velocity = 25
        self.dashing = 0
        Entity.__init__(self, particles, position=pos, health=health)
        self.tex_up = Texture(img.entity["player_up"], 0.1)
        self.tex_down = Texture(img.entity["player_down"], 0.1)
        self.tex_right = Texture(img.entity["player_right"], 0.1)
        self.tex_left = Texture(img.entity["player_left"], 0.1)
        self.tex_idle = Texture(img.entity["player_idle"], 0.4)
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.dash_emitter = entity.Dash(pos=(self.hitbox.center[0], self.hitbox.center[1]), priority=self.priority + 1)
        self.dash_emitter.emitting = False
        particles.append(self.dash_emitter)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        if self.health <= 0: return
        self.offset = [0, 0]
        velocity = self.velocity
        if self.dashing > 0:
            velocity = 200
            self.dashing -= delta_time
            self.dash_emitter.update_emitter([self.hitbox.center[0], self.hitbox.center[1]])
        else:
            self.dash_emitter.emitting = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity /= 2

        self.image = self.tex_idle.get()

        if key[pygame.K_s]:
            self.offset[1] += velocity
            self.image = self.tex_down.get()
        if key[pygame.K_w]:
            self.offset[1] -= velocity
            self.image = self.tex_up.get()
        if key[pygame.K_d]:
            self.offset[0] += velocity
            self.image = self.tex_right.get()
        if key[pygame.K_a]:
            self.offset[0] -= velocity
            self.image = self.tex_left.get()
        self.entity_update(blocks=blocks, particles=particles, delta_time=delta_time, entitys=[], player=player)
        if self.offset != [0, 0]:
            play_sound('step')

    def dash(self):
        play_sound('swing')
        self.dash_emitter.emitting = True
        self.dashing = 0.1
        self.mana -= 20
