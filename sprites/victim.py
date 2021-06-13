import math
import pygame
import random
import globals
import utils
from utils import absToRel
from utils import relToAbs
from utils import relToAbsDual

ichkeksi_image = pygame.image.load("textures/ichkeksi.png")
damage_image = pygame.image.load("textures/damage.png")


class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.testsurface = pygame.Surface((50, 50))
        self.original_image = ichkeksi_image
        self.damage = damage_image
        self.image = pygame.transform.scale(ichkeksi_image, (relToAbsDual(0.1, 0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.direction = random.randint(1, 4)
        self.onscreen = True
        self.velocity = globals.difficulty
        self.health = globals.victimhealthpointsmax
        self.breakcooldown = 0
        self.relposx = 0
        self.relposy = 0
        self.tookdamage = False
        self.damage_animation_cooldown = 10

    def summon(self):
        if self.onscreen:
            position = random.randint(relToAbs(0.1), relToAbs(0.9))

            if self.direction == 1:
                self.rect.center = (position, relToAbs(0.1) * -1)
                self.relposx = absToRel(position - relToAbs(0.05))
                self.relposy = absToRel(relToAbs(0.1) * -1 - relToAbs(0.05))

            elif self.direction == 3:
                self.rect.center = (position, relToAbs(1.1))
                self.relposx = absToRel(position - relToAbs(0.05))
                self.relposy = absToRel(relToAbs(1.1) - relToAbs(0.05))

            elif self.direction == 2:
                self.rect.center = (relToAbs(1.1), position)
                self.relposx = absToRel(relToAbs(1.1) - relToAbs(0.05))
                self.relposy = absToRel(position - relToAbs(0.05))

            elif self.direction == 4:
                self.rect.center = (relToAbs(0.1) * -1, position)
                self.relposx = absToRel(relToAbs(0.1) * -1 - relToAbs(0.05))
                self.relposy = absToRel(position - relToAbs(0.05))

    def update(self, player, click, webgroup, delta_time):
        if self.onscreen:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideweb = pygame.sprite.spritecollideany(self, webgroup)
            collideplayer = self.rect.colliderect(player.rect)
            collidereach = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)

            if collideweb:
                if self.breakcooldown > globals.victimbreakcooldownmax:
                    collideweb.kill()
                    self.breakcooldown = 0
                self.breakcooldown += 1
                self.velocity = 0.05 * delta_time
            else:
                self.velocity = 0.1 * delta_time

            if self.direction == 1:
                self.relposy += self.velocity

            elif self.direction == 2:
                self.relposx -= self.velocity

            elif self.direction == 3:
                self.relposy -= self.velocity

            elif self.direction == 4:
                self.relposx += self.velocity

            self.rect.x = relToAbs(self.relposx)
            self.rect.y = relToAbs(self.relposy)

            print(self.rect.x, self.rect.y)

            if self.rect.centerx > relToAbs(1.1) or self.rect.centerx < relToAbs(
                    0.1) * -1 or self.rect.centery > relToAbs(1.1) or self.rect.centery < relToAbs(
                0.1) * -1:
                self.kill()
                self.rect = None
                self.onscreen = False
                self.health = -1
                globals.victimsmissed += 1

            self.damage_animation_cooldown -= 1
            if self.damage_animation_cooldown < 1:
                self.image = pygame.transform.scale(ichkeksi_image, (relToAbsDual(0.1, 0.1)))
            if click and collidemouse and collidereach <= relToAbs(player.reach):
                self.damage_animation_cooldown = 5
                surface = pygame.transform.scale(ichkeksi_image, (relToAbsDual(0.1, 0.1)))
                surface.blit(pygame.transform.scale(damage_image, (relToAbsDual(0.1, 0.1))), (0, 0))
                self.image = surface
                self.health -= 1
                globals.damagesum += 1
                utils.playSound('hit')
            # UNCOMMENT AFTER

            # TEMPORARY CODE TO KILL VICTIMS FASTER
            # if collidemouse:
            #    self.health -= 1
            #    globals.damagesum += 1
            #    utils.playSound('hit')
            # REMOVE AFTER
            # smarty pants

            if collideplayer and globals.damagecooldown >= globals.maxcooldown:
                globals.playerhealthpoints -= 1
                globals.damagecooldown = 0
                globals.player_hurt = True
                globals.damage_animation_cooldown = 10
                utils.playSound('hurt')

            if self.health == 0:
                self.kill()
                self.rect = None
                globals.victimskilled += 1
                self.onscreen = False

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (relToAbsDual(0.1, 0.1)))
        self.rect = self.image.get_rect()

    def draw(self, window):
        print("hello lol")
        window.blit(self.image, self.rect)
        if self.tookdamage:
            window.blit(self.damage, self.rect)
