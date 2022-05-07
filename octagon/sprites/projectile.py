import pygame

from octagon.utils import debug_outlines, var, play_sound
from octagon.utils.static import angle_deg, conv_deg_rad, conv_rad_deg, get_deltas


class Projectile(pygame.sprite.Sprite):
    def __init__(self, env, image, pos, radians, homing=False, homing_target=None, hitbox=(3, 3), rotating=False,
                 rotation_increment=0, velocity=3, exploding=False, explosion_particles:list[type]=None, damage=10, sender="player"):
        pygame.sprite.Sprite.__init__(self)
        self.env = env
        self.env.projectiles.append(self)
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
        self.velocity = velocity
        self.pos = pos
        self.radians = radians
        self.hitbox = pygame.Rect(self.pos, hitbox)

        self.original_image = image
        self.image = self.original_image
        if not self.rotating:
            self.image = pygame.transform.rotate(self.original_image, -conv_rad_deg(self.radians)+45)
        self.rect = self.image.get_rect()
        self.dx, self.dy = get_deltas(self.radians)
        self.dxtotal, self.dytotal = 0, 0
        if self.exploding:
            self.ExplosionPts = explosion_particles
            self.spark_emitter = self.ExplosionPts[3](env=self.env, pos=pos)
            env.particles.append(self.spark_emitter)

    def projectile_update(self):
        if self.exploding:
            self.spark_emitter.update_emitter([self.rect.centerx, self.rect.centery])
        if self.collided:
            self.post_collision_update()
            return

        for i in self.env.blocks:
            if self.hitbox.colliderect(i.rect):
                self.collide(sound="blockplace", despawn_seconds=4)
                return
        for i in self.env.projectiles:
            if i != self and i.sender != self.sender:
                if not i.collided:
                    if self.hitbox.colliderect(i.rect):
                        self.collide(sound="hit", despawn_seconds=0)
                        i.collide(particles=self.env.particles, projectiles=self.env.projectiles, despawn_seconds=0)
                        return

        if self.sender == "player":
            for i in self.env.entities:
                if self.hitbox.colliderect(i.hitbox):
                    self.collide(hit=True, target=i, sound="hit", despawn_seconds=2)
                    i.damage(damage=self.damage, pos=self.hitbox.center)
                    return
        elif self.sender == "entity":
            if self.hitbox.colliderect(self.env.player.hitbox):
                self.collide(sound="hit", despawn_seconds=2)
                self.env.player.damage(damage=self.damage, particles=self.env.particles, pos=self.hitbox.center)
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

        self.dxtotal += dx * self.velocity * 50 * self.env.delta_time
        self.dytotal += dy * self.velocity * 50 * self.env.delta_time
        self.rect.center = (self.pos[0] + self.dxtotal, self.pos[1] + self.dytotal)
        self.hitbox.center = self.rect.center

    def collide(self, hit=False, target=None, sound=None, despawn_seconds=4):
        if self.exploding:
            play_sound('explosion')
            self.explode()
            self.env.projectiles.remove(self)
            self.spark_emitter.kill()
        else:
            self.despawn_seconds = despawn_seconds
            if sound is not None:
                play_sound(sound)
            self.collided = True
            if hit:
                self.pc_target_offset = [self.hitbox.centerx - target.hitbox.centerx, self.hitbox.centery - target.hitbox.centery]
                self.pc_target = target

    def post_collision_update(self):
        self.despawn_seconds -= self.env.delta_time
        if self.despawn_seconds < 0:
            self.env.projectiles.remove(self)
        if self.pc_target:
            self.rect.centerx = self.pc_target.hitbox.centerx + self.pc_target_offset[0]
            self.rect.centery = self.pc_target.hitbox.centery + self.pc_target_offset[1]

    def explode(self):
        self.env.particles.append(self.ExplosionPts[0](self.env, self.rect.center))
        self.env.particles.append(self.ExplosionPts[1](self.env, self.rect.center))
        self.env.particles.append(self.ExplosionPts[2](self.env, self.rect.center))

    def draw(self, surface):
        image = self.image
        if var.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect)
        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
