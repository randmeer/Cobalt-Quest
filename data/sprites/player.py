import pygame

WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 500


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((100, 100))
        elia_original = pygame.image.load("data/textures/3lia03.png")
        self.image = pygame.transform.scale(elia_original, (50, 50))
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self, w, a, s, d, velocity):
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
