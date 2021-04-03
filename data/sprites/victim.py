import pygame, random
from data import globals


class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        keksi_original = pygame.image.load("data/textures/IchKeksi.png")
        self.image = pygame.transform.scale(keksi_original, (50, 50))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)

    def summon(self, direction, number):
        if not globals.on_screen[number]:
            position = random.randint(50, 450)
            if direction == 1:
                self.rect.center = (position, -50)
            if direction == 3:
                self.rect.center = (position, 550)
            if direction == 2:
                self.rect.center = (550, position)
            if direction == 4:
                self.rect.center = (-50, position)

    def update(self, direction, velocity, player, number, click, damagecooldown):
        if globals.on_screen[number]:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideplayer = self.rect.colliderect(player.rect)

            if direction == 1:
                self.rect.y += velocity
            elif direction == 2:
                self.rect.x -= velocity
            elif direction == 3:
                self.rect.y -= velocity
            elif direction == 4:
                self.rect.x += velocity

            if self.rect.centerx > 550 or self.rect.centerx < -50 or self.rect.centery > 550 or self.rect.centery < -50:
                self.kill()
                self.rect = None
                globals.on_screen[number] = False
                globals.victimhealth[number] = -1

            if collidemouse and click:
                globals.victimhealth[number] -= 1

            if collideplayer and damagecooldown >= globals.maxcooldown:
                globals.playerhealthpoints -= 1
                globals.damagecooldown = 0

            if globals.victimhealth[number] == 0:
                self.kill()
                self.rect = None
                globals.victimskilled += 1
                globals.on_screen[number] = False

            if globals.victimhealth[number] == -1:
                self.kill()
                self.rect = None
                globals.victimsmissed += 1
                globals.on_screen[number] = False

    def draw(self, window):
        window.blit(self.image, self.rect)
