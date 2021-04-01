import pygame


WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 500


class Victim(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        keksi_original = pygame.image.load("data/textures/IchKeksi.png")
        self.image = pygame.transform.scale(keksi_original, (50, 50))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)

    def summon(self, direction, position):
        if direction == 1:
            self.rect.center = (position, -50)
        if direction == 3:
            self.rect.center = (position, 550)
        if direction == 2:
            self.rect.center = (550, position)
        if direction == 4:
            self.rect.center = (-50, position)

    def update(self, direction, velocity):
        if direction == 1:
            self.rect.y += velocity
        if direction == 2:
            self.rect.x -= velocity
        if direction == 3:
            self.rect.y -= velocity
        if direction == 4:
            self.rect.x += velocity