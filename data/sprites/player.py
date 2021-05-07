import pygame, math
from data import globals, utils


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skin = utils.getSetting('skin')
        if self.skin == '3lia03':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(pygame.image.load("data/textures/3lia03.png"), (50, 50)))
        elif self.skin == 'Rande':
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(pygame.image.load("data/textures/Rande.png"), (50, 50)))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (globals.WIDTH / 2, globals.HEIGHT / 2)
        self.velocity = 2
        self.position = (0, 0)

    def update(self, webgroup):
        collideweb = pygame.sprite.spritecollideany(self, webgroup)
        velocity = self.velocity

        if collideweb:
            velocity = self.velocity / 2

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity = self.velocity / 2

        if key[pygame.K_s] and self.rect.bottom < 500:
            self.rect.y += velocity
        if key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= velocity
        if key[pygame.K_d] and self.rect.right < 500:
            self.rect.x += velocity
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= velocity

        self.position = self.rect.center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, window):
        window.blit(self.image, self.rect)
