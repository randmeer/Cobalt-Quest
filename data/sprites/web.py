import pygame, random


class Web(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        keksi_original = pygame.image.load("data/textures/web.png")
        self.image = pygame.transform.scale(keksi_original, (50, 50))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)

    def summon(self, direction):
        position = random.randint(50, 450)
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
        elif direction == 2:
            self.rect.x -= velocity
        elif direction == 3:
            self.rect.y -= velocity
        elif direction == 4:
            self.rect.x += velocity

        if -100 < self.rect.x > 600:
            self.kill()
        if -100 < self.rect.y > 600:
            self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect)

    #def die(self):
    #    self.kill()
