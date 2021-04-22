import pygame, random
from data import globals, utils
from data.sprites import web


class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.image = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.floatx = 0
        self.floaty = 0

    def summon(self, direction, number):
        if not globals.on_screen[number]:
            position = random.randint(50, 450)
            if direction == 1:
                self.rect.center = (position, -50)
                self.floatx = position - 25
                self.floaty = -50 - 25
            if direction == 3:
                self.rect.center = (position, 550)
                self.floatx = position - 25
                self.floaty = 550 - 25
            if direction == 2:
                self.rect.center = (550, position)
                self.floatx = 550 - 25
                self.floaty = position - 25
            if direction == 4:
                self.rect.center = (-50, position)
                self.floatx = -50 - 25
                self.floaty = position - 25

    def update(self, direction, velocity, player, number, click, damagecooldown, webgroup):
        if globals.on_screen[number]:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideweb = pygame.sprite.spritecollideany(self, webgroup)
            collideplayer = self.rect.colliderect(player.rect)

            if collideweb:
                if globals.victimbreakcooldowns[number] > globals.victimbreakcooldownmax:
                    collideweb.kill()
                    globals.victimbreakcooldowns[number] = 0
                globals.victimbreakcooldowns[number] += 1
                velocity = 0.3

            if direction == 1:
                self.floaty += velocity
                self.rect.y = self.floaty
            elif direction == 2:
                self.floatx -= velocity
                self.rect.x = self.floatx
            elif direction == 3:
                self.floaty -= velocity
                self.rect.y = self.floaty
            elif direction == 4:
                self.floatx += velocity
                self.rect.x = self.floatx

            if self.rect.centerx > 550 or self.rect.centerx < -50 or self.rect.centery > 550 or self.rect.centery < -50:
                self.kill()
                self.rect = None
                globals.on_screen[number] = False
                globals.victimhealth[number] = -1

            # THIS IS THE FINAL CODE
            # if collidemouse and click:
            #    globals.victimhealth[number] -= 1
            #    globals.damagesum += 1
            #    utils.playHit()
            # UNCOMMENT AFTER

            # TEMPORARY CODE TO KILL VICTIMS FASTER
            if collidemouse:
                globals.victimhealth[number] -= 1
                globals.damagesum += 1
                utils.playHit()
            # REMOVE AFTER

            if collideplayer and damagecooldown >= globals.maxcooldown:
                globals.playerhealthpoints -= 1
                globals.damagecooldown = 0
                utils.playHurt()

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
