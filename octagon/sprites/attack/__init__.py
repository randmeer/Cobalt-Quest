import pygame

from octagon.utils import angle_deg, conv_deg_rad, sin, cos, get_outline_mask, var


class Attack(pygame.sprite.Sprite):
    def __init__(self, mousepos, playerpos, image, offset=0):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 2
        self.collided = False
        self.mp = mousepos
        self.pp = playerpos
        self.offset = offset
        self.damage = 10
        self.swing_deg = angle_deg(self.pp, self.mp)
        self.swing_rad = conv_deg_rad(self.swing_deg)
        dx = sin(self.swing_rad)
        dy = cos(self.swing_rad)
        self.swing_target = (self.pp[0] + dx * 20, self.pp[1] - dy * 20)
        self.swing_image = image
        self.image = pygame.transform.rotate(self.swing_image.get(), -self.swing_deg+self.offset)
        self.rect = self.image.get_rect()
        self.rect.center = self.swing_target

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time, blocks, entitys, particles, player, projectiles, melee):
        if self.swing_image.get() == False:
            melee.remove(self)
            return
        else:
            self.image = pygame.transform.rotate(self.swing_image.get(), -self.swing_deg+self.offset)
        if self.collided: return

        self.mask = pygame.mask.from_surface(self.image)

        for i in projectiles:
            if pygame.sprite.collide_mask(self, i):
                i.collide(particles=particles, projectiles=projectiles, despawn_seconds=0)
                return
        for i in entitys:
            if pygame.sprite.collide_mask(self, i):
                i.damage(damage=self.damage, particles=particles, pos=(self.rect[0] + pygame.sprite.collide_mask(self, i)[0], self.rect[1] + pygame.sprite.collide_mask(self, i)[1],))
                self.collided = True
                return
        # TODO: get the collision between the swing mask and the entity rect, not the entity mask

    def draw(self, surface):
        image = self.image
        if var.soft_debug:
            image = self.image.copy()
            clone = image.copy()
            clone.fill((0, 0, 0))
            mask1 = get_outline_mask(clone, 1, (255, 255, 255))
            mask2 = get_outline_mask(image, 1, (255, 0, 0))
            image.blit(mask1, (0, 0))
            image.blit(mask2, (0, 0))
        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))

