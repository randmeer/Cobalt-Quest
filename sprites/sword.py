import pygame

from utils import relToAbsDual, relToAbs

sword_texture = pygame.image.load("textures/dagger.png")

class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.default_image = pygame.transform.scale(sword_texture, relToAbsDual(0.1, 0.1))
        self.image = self.default_image
        self.rect = self.default_image.get_rect()
        self.rect.center = (-100, -100)
        self.animation = 0
        self.visibility = False
        self.absangle = 0

    def update(self, playersprite, delta_time):
        if self.visibility and self.animation > 0:
            self.absangle = abs(playersprite.rotation - 270) - 180
            self.image = pygame.transform.rotate(self.default_image, playersprite.rotation)
            # self.absangle = abs(playersprite.angle - 90)
            # self.image = pygame.transform.rotate(self.default_image, playersprite.angle)
            self.rect = self.image.get_rect(center=playersprite.rect.center)

            # move the sword in the correct x and y directions
            if 0 <= self.absangle <= 90:
                self.rect.centerx -= self.animation * relToAbs((90 - self.absangle) / 500)
                self.rect.centery -= self.animation * relToAbs((self.absangle - 0) / 500)
            elif 90 <= self.absangle <= 180:
                self.rect.centerx += self.animation * relToAbs((self.absangle - 90) / 500)
                self.rect.centery -= self.animation * relToAbs((180 - self.absangle) / 500)
            elif 180 <= self.absangle <= 270:
                self.rect.centerx += self.animation * relToAbs((270 - self.absangle) / 500)
                self.rect.centery += self.animation * relToAbs((self.absangle - 180) / 500)
            elif 270 <= self.absangle <= 360:
                self.rect.centerx -= self.animation * relToAbs((self.absangle - 270) / 500)
                self.rect.centery += self.animation * relToAbs((360 - self.absangle) / 500)

            self.animation -= 5 * delta_time

        if self.animation <= 0:
            self.visibility = False

    def resize(self):
        self.default_image = pygame.transform.scale(sword_texture, relToAbsDual(0.1, 0.1))
        self.rect = self.default_image.get_rect()

    def draw(self, window):
        if self.visibility:
            window.blit(self.image, self.rect)
