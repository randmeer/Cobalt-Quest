import random
import math
import pygame

from octagon.utils import get_outline_mask, img, var
from octagon.utils.static import angle_deg, conv_deg_rad, tuple_add, tuple_factor, list_add, get_deltas


class ParticleCloud(pygame.sprite.Sprite):
    def __init__(self, env, center, radius, velocity, preset=None, ptsize=1, color=(255, 255, 255), density=1,
                 fadeout=False, dist=0.3, damage=None, damage_cooldown=0.5, damage_amount=0, colorvar=50, priority=2,
                 no_debug=False, spawnradius=0, spawnregion=(0, 0), target=None, on_target_reach = None):
        """
        :param center: (x, y)
        :param radius: pixels
        :param velocity: custom unit
        :param preset: on of the presets from particles.json
        :param ptsize: particle-radius in pixels
        :param color: (r, g, b)
        :param density: number of particles in the cloud
        :param fadeout: boolean
        :param dist: float, velocity distribution (0 --> exactly the given velocity, 1 --> random velocity from 0% to 200% of given velocity)
        :param damage: None for no damage, "single" for single hit, "poison" for continuous damage
        :param damage_cooldown: seconds, only used for "poison"-damage
        :param damage_amount: lost health points on hit
        :param colorvar: int, color variation (0 --> exactly the given color, 20 --> random offset by [-20, 20] from given color)
        :param priority: render priority (0 --> important)
        :param no_debug: cloud hitbox doesnt show up in debug mode
        :param spawnradius: pixels
        :param spawnregion: (pixels width, pixels height), is centered around center
        :param target: Entity object particles will follow
        :param on_target_reach: lambda function executed for every particle when target is reached
        """
        pygame.sprite.Sprite.__init__(self)

        # parameters
        self.env = env
        self.priority = priority
        self.preset = preset
        self.no_debug = no_debug
        self.center = list(center)
        self.fadeout = fadeout
        self.ptsize = ptsize
        self.target = target
        self.vel = velocity
        self.dist = dist

        # damage
        self.damage = damage
        self.dmg_amount = damage_amount
        if self.damage is not None:
            self.dc = 0
            self.dc_max = damage_cooldown

        # colors
        if self.preset:
            self.color = img.particles[self.preset][0]
            self.colorvar = img.particles[self.preset][1]
        else:
            self.color = color
            self.colorvar = colorvar

        # spawn radius/region
        if spawnradius > 0:
            self.spawnregion = (spawnradius, spawnradius)
        else:
            self.spawnregion = spawnregion

        # rect
        if self.target is None:
            self.radius = radius
            self.rect = pygame.Rect(self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2)
        else:
            self.target_velocity = 0.1
            self.on_target_reach = on_target_reach
            self.rect = pygame.Rect(self.center, (2, 2))
        self.rect.center = self.center[0], self.center[1]

        # particles
        self.particles = []
        for i in range(density):
            self.particles.append(self.generate_particle())

    def generate_particle(self):
        # particle specification: [[posx, posy], [velx, vely], radius, (r, g, b)]

        # location
        pt_center = self.center.copy()
        if self.spawnregion != (0, 0):
            pt_center = [pt_center[0] + random.randint(int(-self.spawnregion[0] / 2), int(self.spawnregion[0] / 2)),
                         pt_center[1] + random.randint(int(-self.spawnregion[1] / 2), int(self.spawnregion[1] / 2))]

        # velocity
        pt_velocity = [self.vel * random.uniform(-1, 1) * random.uniform(1 - self.dist, 1 + self.dist),
                       self.vel * random.uniform(-1, 1) * random.uniform(1 - self.dist, 1 + self.dist)]

        # color
        pt_color = [self.color[0] + random.randint(-self.colorvar, self.colorvar),
                    self.color[1] + random.randint(-self.colorvar, self.colorvar),
                    self.color[2] + random.randint(-self.colorvar, self.colorvar)]
        for j in range(3):
            if pt_color[j] < 0:
                pt_color[j] = 0
            if pt_color[j] > 255:
                pt_color[j] = 255

        return [pt_center, pt_velocity, self.ptsize, pt_color]

    def update(self):
        for pt in self.particles:
            # move
            pt[0][0] += pt[1][0]
            pt[0][1] += pt[1][1]

            # distance to cloud border / target
            if self.target is None:
                dist = self.radius - math.sqrt((self.rect.centerx - pt[0][0]) ** 2 + (self.rect.centery - pt[0][1]) ** 2)
            else:
                dist = math.sqrt((pt[0][0] - self.target.position[0]) ** 2 + (pt[0][1] - self.target.position[1]) ** 2)

            # distance below 1 -> kill pt
            if dist < 1:
                self.particles.remove(pt)
                if self.target is not None:
                    self.on_target_reach()

            # if fadeout, calculate size according to distance
            if self.fadeout:
                pt[2] = self.ptsize * dist / self.radius

            if self.target is not None:
                # move towards target
                list_add(pt[0], tuple_factor(get_deltas(conv_deg_rad(angle_deg(pt[0], self.target.position))), self.target_velocity))

                # reduce outward velocity
                pt[1][0] /= 1.01
                pt[1][1] /= 1.01

                # increase target velocity
                self.target_velocity += self.env.delta_time * 0.01

                # update cloud rectangle
                # TODO: updated cloud rectangle to fit particles inside

        # no particles left -> kill cloud
        if len(self.particles) == 0:
            self.env.particles.remove(self)

        # deal damage
        if self.damage is not None:
           self.update_damage()

    def update_damage(self):
        self.dc -= self.env.delta_time

        if self.dc < 0:
            for i in self.env.entities:
                if self.rect.colliderect(i.hitbox):
                    i.damage(damage=self.dmg_amount)
            if self.rect.colliderect(self.env.player.hitbox):
                self.env.player.damage(damage=self.dmg_amount)
            self.dc = self.dc_max
            if self.damage == "single":
                self.damage = None

    def draw(self, surface):
        for i in self.particles:
            if self.ptsize > 1:
                pygame.draw.circle(surface, i[3], (i[0][0]+surface.get_width()/2, i[0][1]+surface.get_height()/2), i[2])
            else:
                surface.set_at((int(i[0][0]+surface.get_width()/2), int(i[0][1]+surface.get_height()/2)), i[3])

        if var.soft_debug and not self.no_debug:
            surf = pygame.Surface((self.rect.width, self.rect.height))
            surf.fill((0, 0, 0))
            outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
            surface.blit(outlinesurf, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))


class Emitter(ParticleCloud):
    def __init__(self, env, center, radius, velocity, preset=None, ptsize=1, color=(255, 255, 255), density=0, fadeout=False, dist=0.3, damage=None, damage_amount=5, damage_cooldown=0.5, colorvar=50, priority=2, no_debug=False, spawnradius=0, spawnregion=(0, 0), pps=1):
        ParticleCloud.__init__(self, env, center, radius, velocity, preset=preset, ptsize=ptsize, color=color, density=density, fadeout=fadeout, dist=dist,  damage=damage, damage_amount=damage_amount, damage_cooldown=damage_cooldown, colorvar=colorvar, priority=priority, no_debug=no_debug, spawnradius=spawnradius, spawnregion=spawnregion)
        self.emitting = True
        self.pps = pps
        self.emit_timer = 1 / pps
        self.dead = False

    def update(self):
        self.emit_timer -= self.env.delta_time
        if self.emitting and self.emit_timer < 0:
            self.emit_timer = 1 / self.pps
            pt = self.generate_particle()
            pt.append(self.center.copy())
            self.particles.append(pt)
            # [[posx, posy], [velx, vely], radius, (r, g, b), [cenx, ceny]]
        for pt in self.particles:
            dist = self.radius - math.sqrt((pt[4][0] - pt[0][0]) ** 2 + (pt[4][1] - pt[0][1]) ** 2)
            if dist < 0:
                self.particles.remove(pt)
            pt[0][0] += pt[1][0]
            pt[0][1] += pt[1][1]
            if self.fadeout:
                pt[2] = self.ptsize * dist / self.radius
        if self.dead and len(self.particles) == 0:
            self.env.particles.remove(self)

    def update_emitter(self, center):
        self.center = center
        self.rect.center = self.center[0], self.center[1]

    def kill(self):
        self.emitting = False
        self.dead = True
