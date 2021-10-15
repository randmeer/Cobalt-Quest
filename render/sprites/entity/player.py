import pygame

from utils import play_sound
from utils.texture import Texture
from render.sprites.entity import Entity
from render.sprites import particle_cloud

class Player(Entity):

    def __init__(self, pos, health=100, mana=100):
        self.priority = 1
        self.mana = mana
        self.max_mana = 100
        self.position = pos
        self.velocity = 25
        self.dashing = 0
        Entity.__init__(self, position=pos, health=health)
        self.tex_up = Texture("player_animation_up")
        self.tex_down = Texture("player_animation_down")
        self.tex_right = Texture("player_animation_right")
        self.tex_left = Texture("player_animation_left")
        self.tex_idle = Texture("player_animation_idle")
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

    def update(self, blocks, particles, projectiles, player, delta_time, entitys, melee):
        if self.health <= 0: return
        self.offset = [0, 0]
        if self.dashing > 0:
            velocity = 200
            self.dashing -= delta_time
            particles.append(
                particle_cloud.ParticleCloud(center=(self.hitbox.center[0], self.hitbox.center[1]), radius=7,
                                             particlesize=(1, 1), color=(100, 100, 255), density=10, velocity=20,
                                             colorvariation=20, priority=self.priority + 1))

        else:
            velocity = self.velocity
        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity /= 2

        # following code would move the player the same distance even with 2 keys pressed at the same time
        # but it feels kinda weird so commented it for now

        # keys = 0
        # if key[pygame.K_s]:
        #     keys += 1
        # if key[pygame.K_w]:
        #     keys += 1
        # if key[pygame.K_d]:
        #     keys += 1
        # if key[pygame.K_a]:
        #     keys += 1
        # if keys >= 2:
        #     velocity = self.velocity/math.sqrt(self.velocity)
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
        self.entity_update(blocks=blocks, particles=particles, delta_time=delta_time, entitys=[], melee=[])
        if self.offset != [0, 0]:
            play_sound('step')

    def dash(self):
        play_sound('swing')
        self.dashing = 0.1
        self.mana -= 20
