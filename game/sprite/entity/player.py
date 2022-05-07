import pygame

from octagon.utils import img, play_sound
from octagon.utils.img import Texture
from octagon.sprites.entity import Entity

from game.sprite.particle.entity import Damage, Dash, Footstep


class Player(Entity):
    def __init__(self, env, pos, health=100, mana=100):
        Entity.__init__(self, env, priority=1, position=pos, health=health, velocity=25, max_health=100,
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
        self.dash_emitter = Dash(env=self.env, pos=(self.hitbox.center[0], self.hitbox.center[1]), priority=self.priority + 1)
        self.dash_emitter.emitting = False
        self.env.particles.append(self.dash_emitter)

    def update(self):
        if self.health <= 0: return
        self.offset = [0, 0]
        velocity = self.velocity
        if self.dashing > 0:
            velocity = 200
            self.dashing -= self.env.delta_time
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
        self.entity_update()
        if self.offset != [0, 0]:
            play_sound('step')

    def dash(self):
        if self.submanga(20):
            play_sound('swing')
            self.dash_emitter.emitting = True
            self.dashing = 0.1

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
