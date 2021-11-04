import math
import random
import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, rotation, maxdistance, velocity, distribution, colorvariation, spawnregion):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.size = size
        self.spawnregion = spawnregion
        self.originalcolor = color
        self.colorvariation = colorvariation
        self.maxdistance = maxdistance
        self.distribution = distribution
        self.original_velocity = velocity
        self.rotation = rotation
        self.generate_randoms()
        self.original_image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.original_image.fill(self.color)
        self.image = self.original_image
        self.rect = self.original_image.get_rect()
        self.update(1/60, [])
        self.borderdistance = 0

    def generate_randoms(self):
        self.pos = [self.pos[0] + random.randint(-self.spawnregion[0], self.spawnregion[0]), self.pos[1] + random.randint(-self.spawnregion[1], self.spawnregion[1])]
        self.color = [self.originalcolor[0] + random.randint(-self.colorvariation, self.colorvariation),
                      self.originalcolor[1] + random.randint(-self.colorvariation, self.colorvariation),
                      self.originalcolor[2] + random.randint(-self.colorvariation, self.colorvariation)]
        for i in range(3):
            if self.color[i] < 0:
                self.color[i] = 0
            if self.color[i] > 255:
                self.color[i] = 255
        self.rotangle = random.randint(0, 90)
        self.radians = random.uniform(0, 2 * math.pi)
        self.velocity = random.uniform(1 - (self.distribution), 1 + (self.distribution)) * self.original_velocity
        self.dx = math.cos(self.radians)
        self.dy = math.sin(self.radians)
        self.dxtotal, self.dytotal = 0, 0

    def update(self, delta_time, particles):
        if self.rotation:
            self.image = pygame.transform.rotate(self.original_image, self.rotangle)
            if self.rotangle > 90:
                self.rotangle = 0
            else:
                self.rotangle += 1
        self.rect.center = self.pos[0] + self.dxtotal, self.pos[1] + self.dytotal
        self.dxtotal += self.dx * self.velocity * delta_time
        self.dytotal += self.dy * self.velocity * delta_time
        self.borderdistance = self.maxdistance - math.sqrt((self.rect.centerx - self.pos[0])**2 + (self.rect.centery - self.pos[1])**2)
        if self.borderdistance < 0:
            particles.remove(self)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x+surface.get_width()/2, self.rect.y+surface.get_height()/2))
