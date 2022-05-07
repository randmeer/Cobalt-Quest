import random
import pygame

from octagon.utils import dual_rect_anchor, set_anchor_point, debug_outlines, mask_overlay, cord_to_block, var


class Entity(pygame.sprite.Sprite):
    def __init__(self, env, priority=2, max_health=100, health=100, damage_overlay_on=True, immune_to_web=False,
                 hurt_cooldown=0.5, position=(0, 0), rotation=0, velocity=25, hitboxsize=(16, 16), hitboxanchor="midbottom",
                 automove=False, automove_type='wander', automove_target=None,
                 footstep_particle: type = None, death_particles: tuple[type, type] = None, damage_particle: type = None):
        pygame.sprite.Sprite.__init__(self)
        self.env = env
        self.tex_down = self.tex_up = self.tex_left = self.tex_right = self.tex_idle = None
        self.priority = priority
        self.offset = [0, 0]
        self.position = list(position)
        self.hc = 0
        self.hc_max = hurt_cooldown
        self.hc_ani = 0.25
        self.immune_to_web = immune_to_web
        self.damage_overlay_on = damage_overlay_on
        self.health = health
        self.max_health = max_health
        self.speed_multiplier = 1
        self.rotation = rotation
        self.velocity = velocity
        self.hitbox = pygame.Rect((0, 0), hitboxsize)
        self.hitboxanchor = hitboxanchor
        set_anchor_point(self.hitbox, self.position, self.hitboxanchor)
        self.auto_move = automove
        self.am_type = automove_type
        if self.auto_move:
            self.vsize = int(len(self.env.pathfinder_blocks) / 2)
            self.hsize = int(len(self.env.pathfinder_blocks[0]) / 2)
            if self.am_type == "wander":
                self.am_path = []
                self.am_runs = 0
                self.am_todo = 0
                self.am_target = (0, 0)
                self._am_newpath(automove_target)
        self.FootstepPt = footstep_particle
        if self.FootstepPt is not None:
            self.footstep_emitter = self.FootstepPt(env=self.env, pos=(self.hitbox.midbottom[0], self.hitbox.midbottom[1] - 2), priority=self.priority + 1)
            self.env.particles.append(self.footstep_emitter)
        self.DeathPt = death_particles
        self.DamagePt = damage_particle

    def damage_overlay(self):
        if self.damage_overlay_on:
            pass

    def entity_update(self):
        self.rect = self.image.get_rect()
        self.move()
        if self.health <= 0:
            if self.DeathPt is not None:
                for DeathParticle in self.DeathPt:
                    self.env.particles.append(DeathParticle(env=self.env, center=self.hitbox.center))
            if self.FootstepPt:
                self.env.particles.remove(self.footstep_emitter)
            self.env.entities.remove(self)
        if self.hc >= 0:
            self.hc -= self.env.delta_time
        if self.hc > self.hc_max - self.hc_ani:
            self.image = mask_overlay(image=self.image)

    def damage(self, damage, pos=None):
        if pos is None:
            pos = self.hitbox.center
        if self.hc < 0:
            self.health -= damage
            self.hc = self.hc_max
            if self.DamagePt is not None:
                self.env.particles.append(self.DamagePt(self.env, pos=pos))

    def check_block_collision(self):
        # return pygame.sprite.spritecollideany(self, blocks)
        for i in self.env.blocks:
            if self.hitbox.colliderect(i.rect):
                return True

    def _undo_move(self, direction):
        if direction == "x" or direction == "xy":
            self.position = [self.position[0] - (self.offset[0] * self.speed_multiplier), self.position[1]]
        if direction == "y" or direction == "xy":
            self.position = [self.position[0], self.position[1] - (self.offset[1] * self.speed_multiplier)]
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def _move(self, direction):
        if direction == "x" or direction == "xy":
            self.position[0] += self.offset[0] * self.speed_multiplier
        if direction == "y" or direction == "xy":
            self.position[1] += self.offset[1] * self.speed_multiplier
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def _am_settarget(self):
        target = [self.am_path[self.am_todo][0] - self.hsize, self.am_path[self.am_todo][1] - self.vsize]
        self.am_target = [target[0] * 16 + self.hitbox.width / 2, target[1] * 16 + self.hitbox.height / 2]
        self.am_todo += 1

    def _am_newpath(self, target=None):

        # start node
        start_block = cord_to_block(self.position[0], self.position[1])
        start_unsigned = [0, 0]
        start_unsigned[0] = start_block[0] + self.hsize
        start_unsigned[1] = start_block[1] + self.vsize
        start = self.env.pathfinder_grid.node(start_unsigned[0], start_unsigned[1])

        # end node
        if target is None:
            # generate new target
            while True:
                random.seed()
                x_target_block = (random.randrange(self.hsize * 2))
                y_target_block = (random.randrange(self.vsize * 2))
                if self.env.pathfinder_blocks[y_target_block][x_target_block] != 0:
                    break
            end = self.env.pathfinder_grid.node(x_target_block, y_target_block)
            self.am_todo = 0
        else:
            # use given target
            self.am_todo = 1  # start on the second target, to avoid unnecessarily moving back and forth
            end = self.env.pathfinder_grid.node(target[0], target[1])

        # finder
        self.am_path, self.am_runs = self.env.pathfinder.find_path(start, end, self.env.pathfinder_grid)
        self.env.pathfinder_grid.cleanup()
        self._am_settarget()

    def _am_approachtarget(self):
        ott_x = self.am_target[0] - self.position[0]  # offset to target x
        ott_y = self.am_target[1] - self.position[1]  # offset to target y
        if ott_x > 0:
            self.offset[0] = self.velocity
        elif ott_x < 0:
            self.offset[0] = -self.velocity
        if ott_y > 0:
            self.offset[1] = self.velocity
        elif ott_y < 0:
            self.offset[1] = -self.velocity

    def _automove(self):
        if self.am_type == "wander":
            if round(self.position[0]) != self.am_target[0] or round(self.position[1]) != self.am_target[1]:
                # the entity has not reached its target yet --> keep moving in the target's direction
                self._am_approachtarget()
            else:
                # the entity has reached its target --> set target to next coordinate on path
                if self.am_todo == len(self.am_path):
                    # the reached target is the path's last coordinate --> create new path
                    self._am_newpath()
                else:
                    # set next target to approach
                    self._am_settarget()

        self._move("x")
        if self.check_block_collision():
            self._undo_move("x")
        self._move("y")
        if self.check_block_collision():
            self._undo_move("y")

    def move(self):
        self.speed_multiplier = self.env.delta_time
        if self.auto_move:
            self.image = self.tex_idle.get()
            self.offset = [0, 0]
            self._automove()
        else:
            self._move("x")
            if self.check_block_collision():
                self._undo_move("x")
            self._move("y")
            if self.check_block_collision():
                self._undo_move("y")

        dual_rect_anchor(self.hitbox, self.rect, self.hitboxanchor)
        if self.FootstepPt is not None:
            if self.offset == [0, 0]:
                self.footstep_emitter.emitting = False
            else:
                self.footstep_emitter.update_emitter([self.hitbox.midbottom[0], self.hitbox.midbottom[1] - 2])
                self.footstep_emitter.emitting = True

    def draw(self, surface):
        image = self.image
        if var.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect, anchor="midbottom")

            if self.auto_move:
                cords = self.am_path.copy()
                for i in range(len(cords)):
                    cord = list(cords[i])
                    cord[0] -= self.hsize
                    cord[1] -= self.vsize
                    cord = [cord[0] * 16 + self.hitbox.width / 2, cord[1] * 16 + self.hitbox.height / 2]
                    cord[0] += surface.get_width() / 2
                    cord[1] += surface.get_height() / 2
                    cords[i] = cord
                try:
                    pygame.draw.lines(surface, (255, 255, 0), False, cords, 1)
                    for i in cords:
                        pygame.draw.circle(surface, (255, 255, 0), (i[0], i[1]), 2)
                    pygame.draw.circle(surface, (255, 0, 0), (cords[len(cords) - 1][0], cords[len(cords) - 1][1]), 3)
                except:
                    pass

                pygame.draw.circle(surface, (255, 0, 0), (self.am_target[0] + surface.get_width() / 2, self.am_target[1] + surface.get_height() / 2), 2)

        surface.blit(image, (self.rect.x + surface.get_width() / 2, self.rect.y + surface.get_height() / 2))
