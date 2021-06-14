import pygame
from utils import relToAbsDual
from utils import relToAbs

sword_texture = pygame.image.load("textures/sword.png")

class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.default_image = pygame.transform.scale(sword_texture, relToAbsDual(0.12, 0.18))
        self.image = self.default_image
        self.rect = self.default_image.get_rect()
        self.rect.center = (-100, -100)
        self.animation = 0
        self.visibility = False
        self.velocity = 0.0

    def update(self, playersprite, delta_time):
        self.velocity = 0.2 * delta_time
        if self.visibility and self.animation > 0:
            self.image = pygame.transform.rotate(self.default_image, playersprite.angle)
            self.rect = self.image.get_rect(center=playersprite.rect.center)
            self.animation -= 1
        if self.animation == 0:
            self.visibility = False

    def draw(self, window):
        window.blit(self.image, self.rect)

    def reset(self):
        self.visibility = False
        self.frame = 0
