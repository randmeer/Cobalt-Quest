import pygame

WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 500


class Victim(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((100, 100))
        keksi_original = pygame.image.load("data/textures/IchKeksi.png")
        self.image = pygame.transform.scale(keksi_original, (50, 50))
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self, direction, velocity):
        if direction == 1:
            self.rect.y += velocity
        if direction == 2:
            self.rect.x -= velocity
        if direction == 3:
            self.rect.y -= velocity
        if direction == 4:
            self.rect.x += velocity

        if self.rect.left > WIDTH:
            self.rect.right = 0