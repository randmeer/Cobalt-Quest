import math

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
        #self.offsetangle = 0
        self.absangle = 0

    def update(self, playersprite, delta_time):
        if self.visibility and self.animation > 0:

            # this cursed code below modifies the angle for our purposes
            # basically: angle is -90 when facing neg/neg and 90 when facing pos/pos
            #self.offsetangle = abs(playersprite.angle - 45)
            #if self.offsetangle > 180:
            #    self.offsetangle = 180 - self.offsetangle + 180
            #self.offsetangle -= 90
            # alright figured how to do it without it but keeping this here for now because it was a hella lot of work

            self.absangle = abs(playersprite.angle - 90)

            self.image = pygame.transform.rotate(self.default_image, playersprite.angle)
            #self.rect = self.image.get_rect(center=(playersprite.rect.centerx+int(self.offset * 100), playersprite.rect.centery+int(self.offset * 100)))
            #self.rect = self.image.get_rect(center=(playersprite.rect.centerx+(math.cos(playersprite.angle)*self.offset), playersprite.rect.centery+(math.sin(playersprite.angle)*self.offset)))
            self.rect = self.image.get_rect(center=playersprite.rect.center)

            # move the sword in the correct x and y directions
            if 0 <= self.absangle <= 90:
                self.rect.centerx -= self.animation * (90 - self.absangle)
                self.rect.centery -= self.animation * (self.absangle - 0)
            elif 90 <= self.absangle <= 180:
                self.rect.centerx += self.animation * (self.absangle - 90)
                self.rect.centery -= self.animation * (180 - self.absangle)
            elif 180 <= self.absangle <= 270:
                self.rect.centerx += self.animation * (270 - self.absangle)
                self.rect.centery += self.animation * (self.absangle - 180)
            elif 270 <= self.absangle <= 360:
                self.rect.centerx -= self.animation * (self.absangle - 270)
                self.rect.centery += self.animation * (360 - self.absangle)

            self.animation -= 5 * delta_time

        if self.animation <= 0:
            self.visibility = False

    def draw(self, window):
        if self.visibility:
            window.blit(self.image, self.rect)
