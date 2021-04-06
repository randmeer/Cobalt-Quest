import pygame


class Outline(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.image = pygame.transform.scale(pygame.image.load("data/textures/outline.png"), (50, 50))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)

    def draw(self, window):
        self.rect.x = round((pygame.mouse.get_pos()[0] - 25) / 50) * 50
        self.rect.y = round((pygame.mouse.get_pos()[1] - 25) / 50) * 50
        window.blit(self.image, self.rect)
