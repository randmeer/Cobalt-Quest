import random
import math
import pygame

from utils import globs, get_outline_mask

class ParticleCloud(pygame.sprite.Sprite):
    def __init__(self, center, radius, velocity, ptsize=1, color=(255, 255, 255), density=1, fadeout=False, dist=0.3,
                 damagecooldown=0.5, damage=0, colorvar=50, priority=2, no_debug=False, spawnradius=0,
                 spawnregion=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.priority = priority
        self.damage = damage
        if self.damage > 0:
            self.dc = 0
            self.dc_max = damagecooldown
        self.no_debug = no_debug
        self.center = list(center)
        self.radius = radius
        self.fadeout = fadeout
        self.ptsize = ptsize
        self.color = color
        self.colorvar = colorvar
        self.vel = velocity
        self.dist = dist
        self.spawnregion = spawnregion
        if spawnradius != 0:
            self.spawnregion = (spawnradius, spawnradius)
        self.particles = []
        for i in range(density):
            self.particles.append(self.generate_particle())
        self.rect = pygame.Rect(self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2)
        self.rect.center = self.center[0], self.center[1]

    def generate_particle(self):
        # standard      [[posx, posy], [velx, vely], radius, (r, g, b)]
        pt_center = self.center.copy()
        if self.spawnregion != (0, 0):
            pt_center = [pt_center[0] + random.randint(int(-self.spawnregion[0] / 2), int(self.spawnregion[0] / 2)),
                         pt_center[1] + random.randint(int(-self.spawnregion[1] / 2), int(self.spawnregion[1] / 2))]
        pt_color = [self.color[0] + random.randint(-self.colorvar, self.colorvar),
                    self.color[1] + random.randint(-self.colorvar, self.colorvar),
                    self.color[2] + random.randint(-self.colorvar, self.colorvar)]
        for j in range(3):
            if pt_color[j] < 0:
                pt_color[j] = 0
            if pt_color[j] > 255:
                pt_color[j] = 255
        pt = [pt_center, [self.vel * random.uniform(-1, 1) * random.uniform(1 - self.dist, 1 + self.dist), self.vel * random.uniform(-1, 1) * random.uniform(1 - self.dist, 1 + self.dist)], self.ptsize, pt_color]
        return pt

    def update(self, delta_time, entitys, player, particles, blocks, projectiles, melee):
        for pt in self.particles:
            dist = self.radius - math.sqrt((self.rect.centerx - pt[0][0]) ** 2 + (self.rect.centery - pt[0][1]) ** 2)
            if dist < 0:
                self.particles.remove(pt)
            pt[0][0] += pt[1][0]
            pt[0][1] += pt[1][1]
            if self.fadeout:
                pt[2] = self.ptsize * dist / self.radius
        if len(self.particles) == 0:
            particles.remove(self)
        if self.damage > 0:
           self.update_damage(delta_time, particles, entitys, player)

    def update_damage(self, delta_time, particles, entitys, player):
        self.dc -= delta_time
        if self.dc < 0:
            for i in entitys:
                if self.rect.colliderect(i.hitbox):
                    i.damage(damage=self.damage, particles=particles)
                    self.dc = self.dc_max
            if self.rect.colliderect(player.hitbox):
                player.damage(damage=self.damage, particles=particles)

    def draw(self, surface):
        for i in self.particles:
            if self.ptsize > 1:
                pygame.draw.circle(surface, i[3], (i[0][0]+surface.get_width()/2, i[0][1]+surface.get_height()/2), i[2])
            else:
                surface.set_at((int(i[0][0]+surface.get_width()/2), int(i[0][1]+surface.get_height()/2)), i[3])

        if globs.soft_debug and not self.no_debug:
            surf = pygame.Surface((self.rect.width, self.rect.height))
            surf.fill((0, 0, 0))
            outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
            surface.blit(outlinesurf, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))

class Emitter(ParticleCloud):
    def __init__(self, center, radius, velocity, ptsize=1, color=(255, 255, 255), density=0, fadeout=False, dist=0.3, damagecooldown=0.5, damage=0, colorvar=50, priority=2, no_debug=False, spawnradius=0, spawnregion=(0, 0), pps=1):
        ParticleCloud.__init__(self, center, radius, velocity, ptsize=ptsize, color=color, density=density, fadeout=fadeout, dist=dist, damagecooldown=damagecooldown, damage=damage, colorvar=colorvar, priority=priority, no_debug=no_debug, spawnradius=spawnradius, spawnregion=spawnregion)
        self.emitting = True
        self.pps = pps
        self.emit_timer = 1 / pps
        self.dead = False

    def update(self, delta_time, entitys, player, particles, blocks, projectiles, melee):
        self.emit_timer -= delta_time
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
            particles.remove(self)

    def update_emitter(self, center):
        self.center = center
        self.rect.center = self.center[0], self.center[1]

    def kill(self):
        self.emitting = False
        self.dead = True
