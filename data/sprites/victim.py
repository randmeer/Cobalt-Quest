import pygame, random
from data import globals, utils
from data.utils import relToAbs
from data.utils import relToAbsHeight
from data.utils import absToRel
from data.utils import absToRelHeight


class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.original_image = pygame.image.load("data/textures/IchKeksi.png")
        self.image = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (relToAbs(0.1, 0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        # self.floatx = 0
        # self.floaty = 0
        self.direction = random.randint(1, 4)
        self.onscreen = True
        self.velocity = globals.difficulty
        self.health = globals.victimhealthpointsmax
        self.breakcooldown = 0
        self.relposx = 0
        self.relposy = 0

    def summon(self):
        if self.onscreen:
            position = random.randint(relToAbsHeight(0.1), relToAbsHeight(0.9))

            if self.direction == 1:
                self.rect.center = (position, relToAbsHeight(0.1) * -1)
                self.relposx = absToRelHeight(position - relToAbsHeight(0.05))
                self.relposy = absToRelHeight(relToAbsHeight(0.1) * -1 - relToAbsHeight(0.05))

            elif self.direction == 3:
                self.rect.center = (position, relToAbsHeight(1.1))
                self.relposx = absToRelHeight(position - relToAbsHeight(0.05))
                self.relposy = absToRelHeight(relToAbsHeight(1.1) - relToAbsHeight(0.05))

            elif self.direction == 2:
                self.rect.center = (relToAbsHeight(1.1), position)
                self.relposx = absToRelHeight(relToAbsHeight(1.1) - relToAbsHeight(0.05))
                self.relposy = absToRelHeight(position - relToAbsHeight(0.05))

            elif self.direction == 4:
                self.rect.center = (relToAbsHeight(0.1) * -1, position)
                self.relposx = absToRelHeight(relToAbsHeight(0.1) * -1 - relToAbsHeight(0.05))
                self.relposy = absToRelHeight(position - relToAbsHeight(0.05))

    def update(self, player, click, webgroup):
        if self.onscreen:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideweb = pygame.sprite.spritecollideany(self, webgroup)
            collideplayer = self.rect.colliderect(player.rect)
            w, h = pygame.display.get_surface().get_size()

            if collideweb:
                if self.breakcooldown > globals.victimbreakcooldownmax:
                    collideweb.kill()
                    self.breakcooldown = 0
                self.breakcooldown += 1
                self.velocity = h * 0.001 * globals.difficulty
            else:
                self.velocity = h * 0.002 * globals.difficulty

            if self.direction == 1:
                self.relposy += absToRelHeight(self.velocity)
                self.rect.y = relToAbsHeight(self.relposy)

            elif self.direction == 2:
                self.relposx -= absToRelHeight(self.velocity)
                self.rect.x = relToAbsHeight(self.relposx)

            elif self.direction == 3:
                self.relposy -= absToRelHeight(self.velocity)
                self.rect.y = relToAbsHeight(self.relposy)

            elif self.direction == 4:
                self.relposx += absToRelHeight(self.velocity)
                self.rect.x = relToAbsHeight(self.relposx)

            if self.rect.centerx > relToAbsHeight(1.1) or self.rect.centerx < relToAbsHeight(
                    0.1) * -1 or self.rect.centery > relToAbsHeight(1.1) or self.rect.centery < relToAbsHeight(
                0.1) * -1:
                self.kill()
                self.rect = None
                self.onscreen = False
                self.health = -1
                globals.victimsmissed += 1

            # THIS IS THE FINAL CODE
            if collidemouse and click:
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

            if collideplayer and globals.damagecooldown >= globals.maxcooldown:
                globals.playerhealthpoints -= 1
                globals.damagecooldown = 0
                utils.playSound('hurt')

            if self.health == 0:
                self.kill()
                self.rect = None
                globals.victimskilled += 1
                self.onscreen = False

            print(round(self.relposx, 3))
            #print(round(self.relposy, 3))

    def draw(self, window):
        window.blit(self.image, self.rect)
