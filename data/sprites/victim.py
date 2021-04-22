import pygame, random
from data import globals, utils


class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.image = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.floatx = 0
        self.floaty = 0
        self.direction = random.randint(1, 4)
        self.onscreen = True
        self.velocity = globals.difficulty
        self.health = globals.victimhealthpointsmax
        self.breakcooldown = 0

    def summon(self):
        if self.onscreen:
            position = random.randint(50, 450)

            if self.direction == 1:
                self.rect.center = (position, -50)
                self.floatx = position - 25
                self.floaty = -50 - 25
            if self.direction == 3:
                self.rect.center = (position, 550)
                self.floatx = position - 25
                self.floaty = 550 - 25
            if self.direction == 2:
                self.rect.center = (550, position)
                self.floatx = 550 - 25
                self.floaty = position - 25
            if self.direction == 4:
                self.rect.center = (-50, position)
                self.floatx = -50 - 25
                self.floaty = position - 25

    def update(self, player, click, damagecooldown, webgroup):
        if self.onscreen:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideweb = pygame.sprite.spritecollideany(self, webgroup)
            collideplayer = self.rect.colliderect(player.rect)

            if collideweb:
                if self.breakcooldown > globals.victimbreakcooldownmax:
                    collideweb.kill()
                    self.breakcooldown = 0
                self.breakcooldown += 1
                self.velocity = 0.3

            if self.direction == 1:
                self.floaty += self.velocity
                self.rect.y = self.floaty
            elif self.direction == 2:
                self.floatx -= self.velocity
                self.rect.x = self.floatx
            elif self.direction == 3:
                self.floaty -= self.velocity
                self.rect.y = self.floaty
            elif self.direction == 4:
                self.floatx += self.velocity
                self.rect.x = self.floatx

            if self.rect.centerx > 550 or self.rect.centerx < -50 or self.rect.centery > 550 or self.rect.centery < -50:
                self.kill()
                self.rect = None
                self.onscreen = False
                self.health = -1
                globals.victimsmissed += 1

            # THIS IS THE FINAL CODE
            # if collidemouse and click:
            #    globals.victimhealth[number] -= 1
            #    globals.damagesum += 1
            #    utils.playHit()
            # UNCOMMENT AFTER

            # TEMPORARY CODE TO KILL VICTIMS FASTER
            if collidemouse:
                self.health -= 1
                globals.damagesum += 1
                utils.playHit()
            # REMOVE AFTER

            if collideplayer and damagecooldown >= globals.maxcooldown:
                globals.playerhealthpoints -= 1
                globals.damagecooldown = 0
                utils.playHurt()

            if self.health == 0:
                self.kill()
                self.rect = None
                globals.victimskilled += 1
                self.onscreen = False

    def draw(self, window):
        window.blit(self.image, self.rect)
