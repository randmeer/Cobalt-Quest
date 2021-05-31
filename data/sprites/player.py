import pygame
from math import pi
from math import atan2
from data import globals
from data.utils import getSetting
from data.utils import relToAbsHeight
from data.utils import absToRelHeight

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skin = getSetting('skin')
        if self.skin == '3lia03':
            self.original_original_image = pygame.Surface.convert_alpha(pygame.image.load("data/textures/3lia03.png"))
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(pygame.image.load("data/textures/3lia03.png"), (50, 50)))
        elif self.skin == 'Rande':
            self.original_original_image = pygame.Surface.convert_alpha(pygame.image.load("data/textures/Rande.png"))
            self.original_image = pygame.Surface.convert_alpha(
                pygame.transform.scale(pygame.image.load("data/textures/Rande.png"), (50, 50)))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (globals.WIDTH / 2, globals.HEIGHT / 2)
        self.velocity = 0
        self.position = (0, 0)
        self.relposx = 0.5
        self.relposy = 0.5

    def update(self, webgroup):

        collideweb = pygame.sprite.spritecollideany(self, webgroup)
        velocity = self.velocity
        w, h = pygame.display.get_surface().get_size()

        if collideweb:
            self.velocity = h * 0.001 * globals.difficulty
        else:
            self.velocity = h * 0.002 * globals.difficulty

        key = pygame.key.get_pressed()
        if key[pygame.K_LSHIFT]:
            velocity = self.velocity / 2

        if key[pygame.K_s] and self.rect.bottom < 500:
            self.relposy += absToRelHeight(self.velocity)
            self.rect.y += velocity
        if key[pygame.K_w] and self.rect.top > 0:
            self.relposy -= absToRelHeight(self.velocity)
            self.rect.y -= velocity
        if key[pygame.K_d] and self.rect.right < 500:
            self.relposx += absToRelHeight(self.velocity)
            self.rect.x += velocity
        if key[pygame.K_a] and self.rect.left > 0:
            self.relposx -= absToRelHeight(self.velocity)
            self.rect.x -= velocity



        self.position = self.rect.center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / pi) * -atan2(rel_y, rel_x) - 90
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.position)
        #self.image.fill((255, 255, 255))
        print(self.rect.x)

        self.rect.centerx = relToAbsHeight(self.relposx)
        self.rect.centery = relToAbsHeight(self.relposy)


    def draw(self, window):
        window.blit(self.image, self.rect)
