import pygame


class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.default_image = pygame.transform.scale(pygame.image.load("data/textures/sword.png"), (75, 225))
        self.image = self.default_image

        self.frame1 = pygame.transform.rotate(self.default_image, 22.5)
        self.frame2 = pygame.transform.rotate(self.default_image, 45)
        self.frame3 = pygame.transform.rotate(self.default_image, 67.5)
        self.frame4 = pygame.transform.rotate(self.default_image, 90)
        self.frame5 = pygame.transform.rotate(self.default_image, 112.5)
        self.frame6 = pygame.transform.rotate(self.default_image, 135)
        self.frame7 = pygame.transform.rotate(self.default_image, 157.5)
        self.frame8 = pygame.transform.rotate(self.default_image, 180)
        self.frame9 = pygame.transform.rotate(self.default_image, 202.5)
        self.frame10 = pygame.transform.rotate(self.default_image, 225)
        self.frame11 = pygame.transform.rotate(self.default_image, 247.5)
        self.frame12 = pygame.transform.rotate(self.default_image, 270)
        self.frame13 = pygame.transform.rotate(self.default_image, 292.5)
        self.frame14 = pygame.transform.rotate(self.default_image, 315)
        self.frame15 = pygame.transform.rotate(self.default_image, 337.5)
        self.frame0 = self.default_image

        self.frames = [
            self.frame0,
            self.frame1,
            self.frame2,
            self.frame3,
            self.frame4,
            self.frame5,
            self.frame6,
            self.frame7,
            self.frame8,
            self.frame9,
            self.frame10,
            self.frame11,
            self.frame12,
            self.frame13,
            self.frame14,
            self.frame15,
            self.frame0
        ]

        self.rect = self.default_image.get_rect()
        self.frame = 0
        self.visibility = False

    def update(self, posX, posY):
        if not self.visibility:
            return
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.frame += 1
        if self.frame == 17:
            self.reset()
            print("RESET")
        print(self.frame)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def reset(self):
        self.visibility = False
        self.frame = 0
