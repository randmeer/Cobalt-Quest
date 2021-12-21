import random
import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from utils import globs, dual_rect_anchor, debug_outlines, mask_overlay, block_to_cord, cord_to_block
from render.sprites.particle import entity

class Entity(pygame.sprite.Sprite):

    def __init__(self, particles, max_health=100, health=100, damage_overlay_on=True, immune_to_web=False,
                 hurt_cooldown=0.5, position=(0, 0), rotation=0, auto_rotation=True, hitboxsize=(16, 16),
                 hitboxanchor="midbottom", auto_movement=False, auto_movement_type='wander', floorjson=None):
        pygame.sprite.Sprite.__init__(self)
        self.floorjson = floorjson
        self.tex_down = self.tex_up = self.tex_left = self.tex_right = self.tex_idle = None
        self.offset = [0, 0]
        self.position = position
        self.hc = 0
        self.hc_max = hurt_cooldown
        self.hc_ani = 0.25
        self.immune_to_web = immune_to_web
        self.damage_overlay_on = damage_overlay_on
        self.health = health
        self.max_health = max_health
        self.speed_multiplier = 1
        self.rotation = rotation
        self.auto_rotation = auto_rotation
        self.velocity = 25
        self.hitbox = pygame.Rect((0, 0), hitboxsize)
        self.hitboxanchor = hitboxanchor
        self.auto_move = auto_movement
        self.am_type = auto_movement_type
        if self.auto_move:
            if self.am_type == "wander":
                self._am_createblockgrid()
                self.am_target = self.position
                self.am_path = []
                self.am_runs = 0
                self.am_todo = 0
                self._am_newpath()
        self.footstep_emitter = entity.Footstep(pos=(self.hitbox.midbottom[0], self.hitbox.midbottom[1]-2), priority=self.priority+1)
        particles.append(self.footstep_emitter)

    def damage_overlay(self):
        if self.damage_overlay_on:
            pass

    def entity_update(self, blocks, particles, delta_time, entitys, player):
        self.rect = self.image.get_rect()
        self.move(blocks=blocks, delta_time=delta_time)
        if self.health <= 0:
            particles.append(entity.Die1(center=self.hitbox.center, region=(self.hitbox.width/2, self.hitbox.height/2), radius=self.hitbox.height, ))
            particles.append(entity.Die2(center=self.hitbox.center, radius=self.hitbox.height/1.5))
            particles.remove(self.footstep_emitter)
            entitys.remove(self)
        if self.hc >= 0:
            self.hc -= delta_time
        if self.hc > self.hc_max - self.hc_ani:
            self.image = mask_overlay(image=self.image)

    def damage(self, damage, particles, pos=None):
        if pos is None:
            pos = self.hitbox.center
        if self.hc < 0:
            self.health -= damage
            self.hc = self.hc_max
            particles.append(entity.Damage(pos=pos))

    def check_block_collision(self, blocks):
        # return pygame.sprite.spritecollideany(self, blocks)
        for i in blocks:
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
            self.position = [self.position[0] + (self.offset[0] * self.speed_multiplier), self.position[1]]
        if direction == "y" or direction == "xy":
            self.position = [self.position[0], self.position[1] + (self.offset[1] * self.speed_multiplier)]
        pos = (round(self.position[0]), round(self.position[1]))
        self.hitbox.center = pos
        dual_rect_anchor(self.rect, self.hitbox, self.hitboxanchor)

    def _am_createblockgrid(self):
        self.am_blocks = list(self.floorjson["blocks"])
        for i in range(len(self.am_blocks)):
            for j in range(len(self.am_blocks)):
                if self.am_blocks[i][j] == 0:
                    self.am_blocks[i][j] = 1
                elif self.am_blocks[i][j] != 0:
                    self.am_blocks[i][j] = 0

    def _am_settarget(self):
        bambus = self.am_path[self.am_todo]
        bingo = [0, 0]
        bingo[0] = bambus[0]
        bingo[1] = bambus[1]
        bingo[0] -= self.floorjson["size"]
        bingo[1] -= self.floorjson["size"]
        self.am_target = block_to_cord(bingo, center=True)
        self.am_todo += 1

    def _am_newpath(self):
        stt = cord_to_block(self.position[0], self.position[1])
        strt = [0, 0]
        strt[0] = stt[0] + self.floorjson['size']
        strt[1] = stt[1] + self.floorjson['size']
        self.am_grid = Grid(matrix=self.am_blocks)
        start = self.am_grid.node(strt[0], strt[1])
        while True:
            random.seed()
            x_target_block = (random.randrange(self.floorjson["size"] * 2)) - self.floorjson["size"]
            y_target_block = (random.randrange(self.floorjson["size"] * 2)) - self.floorjson["size"]
            if self.am_blocks[y_target_block][x_target_block] != 0:
                break
        end = self.am_grid.node(x_target_block, y_target_block)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.am_path, self.am_runs = finder.find_path(start, end, self.am_grid)
        self.am_todo = 0
        self._am_settarget()
        if self.am_target != self.position:
            # the entity does not stand in the mittle of a block
            # --> start from the 2nd path coordinate to avoid doing an unnecessary movement
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

    def _automove(self, pathfinding, blocks):
        if pathfinding == "wander":
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
        if self.check_block_collision(blocks):
            self._undo_move("x")
        self._move("y")
        if self.check_block_collision(blocks):
            self._undo_move("y")

    def move(self, blocks, delta_time):
        self.speed_multiplier = delta_time
        if self.auto_move:
            self.image = self.tex_idle.get()
            self.offset = [0, 0]
            self._automove(self.am_type, blocks)
        else:
            self._move("x")
            if self.check_block_collision(blocks):
                self._undo_move("x")
            self._move("y")
            if self.check_block_collision(blocks):
                self._undo_move("y")

        dual_rect_anchor(self.hitbox, self.rect, self.hitboxanchor)
        if self.offset == [0, 0]:
            self.footstep_emitter.emitting = False
        else:
            self.footstep_emitter.update_emitter([self.hitbox.midbottom[0], self.hitbox.midbottom[1] - 2])
            self.footstep_emitter.emitting = True

    def draw(self, surface):
        image = self.image
        if globs.soft_debug:
            image = debug_outlines(self.image, self.hitbox, self.rect, anchor="midbottom")

            if self.auto_move:
                cords = self.am_path.copy()
                for i in range(len(cords)):
                    cord = list(cords[i])
                    cord[0] -= self.floorjson["size"]
                    cord[1] -= self.floorjson["size"]
                    cord = block_to_cord(cord, center=True)
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
