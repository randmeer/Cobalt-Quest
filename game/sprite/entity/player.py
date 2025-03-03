import pygame

from octagon.utils import img, play_sound
from octagon.utils.img import Texture
from octagon.environment.object.entity import Entity

from game.sprite.particle.entity import Damage, Dash, Footstep


class Player(Entity):
    def __init__(self, env, pos, health=100, mana=100):
        Entity.__init__(self, env, priority=1, position=pos, health=health, velocity=50, max_health=100,
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
        self.dash_emitter = Dash(env=self.env, pos=(self.hitbox.center[0], self.hitbox.center[1]), priority=self.priority + 1)
        self.dash_emitter.emitting = False
        self.env.particles.append(self.dash_emitter)

    def update(self):
        if self.health <= 0:
            return

        for event in self.env.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.mana > 0:
                    self.dash()

        velocity_factor = 1

        if self.dashing > 0:
            velocity_factor *= 4
            self.dashing -= self.env.delta_time
            self.dash_emitter.update_emitter([self.hitbox.center[0], self.hitbox.center[1]])
        else:
            self.dash_emitter.emitting = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity_factor /= 2

        direction = pygame.Vector2()
        if key[pygame.K_s]:
            direction.y += 1
        if key[pygame.K_w]:
            direction.y -= 1
        if key[pygame.K_d]:
            direction.x += 1
        if key[pygame.K_a]:
            direction.x -= 1

        self.move(direction, velocity_factor)
        self.entity_update()
        if direction != [0, 0]:
            play_sound('step')

    def dash(self):
        if self.submana(20):
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

    def submana(self, amount):
        if self.mana - amount < 0:
            return False
        else:
            self.mana -= amount
            return True
