import pygame
from data import globals, utils


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.skin = utils.getSetting('skin')
        if self.skin == '3lia03':
            self.image = pygame.transform.scale(pygame.image.load("data/textures/3lia03.png"), (50, 50))
        elif self.skin == 'Rande':
            self.image = pygame.transform.scale(pygame.image.load("data/textures/Rande.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (globals.WIDTH / 2, globals.HEIGHT / 2)

    def update(self, w, a, s, d, velocity, webgroup):
        collideweb = pygame.sprite.spritecollideany(self, webgroup)

        if collideweb:
            velocity = velocity / 2

        if s and self.rect.bottom < 500:
            self.rect.y += velocity
        if a and self.rect.left > 0:
            self.rect.x -= velocity
        if w and self.rect.top > 0:
            self.rect.y -= velocity
        if d and self.rect.right < 500:
            self.rect.x += velocity

    def draw(self, window):
        window.blit(self.image, self.rect)
