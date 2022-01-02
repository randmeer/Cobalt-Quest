import math
import pygame

from utils import play_sound, globs, conv_rad_deg, debug_outlines, angle_deg, conv_deg_rad
from render.sprites.particle import explosion

def get_deltas(radians):
    dx = math.sin(radians)
    dy = -math.cos(radians)
    return dx, dy

class Projectile(pygame.sprite.Sprite):
    def __init__(self, particles, image, pos, radians=None, homing=False, homing_target=None, hitbox=(3, 3), rotating=False,
                 rotation_increment=0, velocity=3, exploding=False, damage=10, sender="player"):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 2
        self.collided = False
        self.damage = damage
        self.homing = homing
        self.homing_target = homing_target
        self.exploding = exploding
        self.exploded = False
        self.pc_target = None
        self.pc_target_offset = [0, 0]
        self.rotating = rotating
        self.rot_increment = rotation_increment
        self.sender = sender
        self.rot_angle = 0
        self.despawn_seconds = 4
        self.pos, self.radians, self.velocity = pos, radians, velocity
        self.original_image = image
        self.image = self.original_image
        if not self.rotating:
            self.image = pygame.transform.rotate(self.original_image, -conv_rad_deg(self.radians)+45)
        self.rect = self.image.get_rect()
        self.dx, self.dy = get_deltas(self.radians)
        self.dxtotal, self.dytotal = 0, 0
        self.hitbox = pygame.Rect(pos, hitbox)
        if self.exploding:
            self.spark_emitter = explosion.SparkEmitter(pos=(self.rect.centerx, self.rect.centery))
            particles.append(self.spark_emitter)

    def projectile_update(self, delta_time, blocks, entitys, player, particles, projectiles, melee):
        if self.collided:
            self.post_collision_update(delta_time=delta_time, projectiles=projectiles)
            return

        for i in blocks:
            if self.hitbox.colliderect(i.rect):
                self.collide(particles=particles, projectiles=projectiles, sound="blockplace", despawn_seconds=4)
                return
        for i in projectiles:
            if i != self and i.sender != self.sender:
                if not i.collided:
                    if self.hitbox.colliderect(i.rect):
                        self.collide(particles=particles, projectiles=projectiles, sound="hit", despawn_seconds=0)
                        i.collide(particles=particles, projectiles=projectiles, despawn_seconds=0)
                        return

        if self.sender == "player":
            for i in entitys:
                if self.hitbox.colliderect(i.hitbox):
                    self.collide(hit=True, target=i, particles=particles, projectiles=projectiles, sound="hit", despawn_seconds=2)
                    i.damage(damage=self.damage, particles=particles, pos=self.hitbox.center)
                    return
        elif self.sender == "entity":
            if self.hitbox.colliderect(player.hitbox):
                self.collide(particles=particles, projectiles=projectiles, sound="hit", despawn_seconds=2)
                player.damage(damage=self.damage, particles=particles, pos=self.hitbox.center)
                return

        if self.rotating:
            self.image = pygame.transform.rotate(self.original_image, self.rot_angle)
            self.rot_angle += 4
            if self.rot_angle > 360:
                self.rot_angle = 0
            self.rect = self.image.get_rect()

        if self.homing:
            dx, dy = get_deltas(conv_deg_rad(angle_deg(self.hitbox.center, self.homing_target.hitbox.center)))
        else:
            dx, dy = self.dx, self.dy

        self.dxtotal += dx * self.velocity * 50 * delta_time
        self.dytotal += dy * self.velocity * 50 * delta_time
        self.rect.center = (self.pos[0] + self.dxtotal, self.pos[1] + self.dytotal)
        self.hitbox.center = self.rect.center

    def collide(self, particles, projectiles, hit=False, target=None, sound=None, despawn_seconds=4):
        if self.exploding:
            play_sound('explosion')
            self.explode(particles=particles)
            projectiles.remove(self)
            self.spark_emitter.kill()
        else:
            self.despawn_seconds = despawn_seconds
            if sound is not None:
                play_sound(sound)
            self.collided = True
            if hit:
                self.pc_target_offset = [self.hitbox.centerx - target.hitbox.centerx, self.hitbox.centery - target.hitbox.centery]
                self.pc_target = target

    def post_collision_update(self, delta_time, projectiles):
        self.despawn_seconds -= delta_time
        if self.despawn_seconds < 0:
            projectiles.remove(self)
        if self.pc_target:
            self.rect.centerx = self.pc_target.hitbox.centerx + self.pc_target_offset[0]
            self.rect.centery = self.pc_target.hitbox.centery + self.pc_target_offset[1]

    def explode(self, particles):
        particles.append(explosion.Smoke(self.rect.center))
        particles.append(explosion.Fire(self.rect.center))
        particles.append(explosion.Sparks(self.rect.center))

    def draw(self, surface):
        image = self.image
        if globs.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect)
        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
