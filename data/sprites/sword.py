import pygame


class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.image = pygame.transform.scale(pygame.image.load("data/textures/sword.png"), (50, 150))
        self.rect = self.image.get_rect()
        self.angle = 0

    def update(self, posX, posY):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(posX, posY)).center)
        self.angle -= 1
        print(self.angle)
        if self.angle < -30:
            self.kill()
            self.rect = None
            self.image = None
            print("killed")

    def draw(self, window):
        window.blit(self.image, self.rect)
