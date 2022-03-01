import time
import pygame

from octagon.utils import mp_scene, get_setting, angle_deg, conv_deg_rad, cout, play_sound, var, img
from octagon.environment import Environment

from game import globs
from game.sprites.attack import dagger
from game.gui.overlay import pause_screen, show_inventory, end_screen
from game.sprites.projectile import arrow, shuriken, fireball
from game.sprites.entity.player import Player
from game.sprites.entity.apprentice import Apprentice


class Floor(Environment):

    def __init__(self, window):
        globs.set_global_defaults()
        Environment.__init__(self, window,
                             f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json",
                             f"./data/savegames/{get_setting('current_savegame')}/inventory.json",
                             Player,
                             [Apprentice],
                             [arrow.Arrow, shuriken.Shuriken, fireball.Fireball])

    def update(self):
        """
        updates the game surface and handles user input
        """

        # update objects
        self.click = False
        mp = mp_scene(scene=self.scene)
        self.scene.update(player=self.player, delta_time=self.delta_time, blocks=self.blocks, entitys=self.entities, particles=self.particles, projectiles=self.projectiles, melee=self.melee)
        self.hud.update(player=self.player)

        if self.player.health <= 0:
            self.invjson["health"] = 100
            self.invjson["deaths"] += 1
            self.invjson.save()
            end_screen(window=self.window, background=self.surface.copy(), end="defeat")
            self.end_loop()

        # handle events
        key = pygame.key.get_pressed()
        self.events = list(pygame.event.get())
        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                globs.quitgame = True
            # buttonevents
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and self.cooldown <= 0:
                    if self.hud.hotbar[self.hud.slot][1] == "dagger":
                        play_sound('swing')
                        self.melee.append(dagger.Stab(playerpos=self.player.hitbox.center, mousepos=mp))
                        self.cooldown += 0.25
                    if self.hud.hotbar[self.hud.slot][2] > 0:
                        if self.hud.hotbar[self.hud.slot][1] == "shuriken":
                            play_sound('swing')
                            self.projectiles.append(shuriken.Shuriken(exploding=True, particles=self.particles, pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
                            self.cooldown += 0.25
                        elif self.hud.hotbar[self.hud.slot][1] == "bow":
                            play_sound('swing')
                            self.projectiles.append(arrow.Arrow(particles=self.particles, pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
                            self.cooldown += 1
                        self.hud.hotbar[self.hud.slot][2] -= 1
                elif event.button == pygame.BUTTON_RIGHT and self.cooldown <= 0:
                    if self.hud.hotbar[self.hud.slot][1] == "dagger":
                        play_sound('swing')
                        self.melee.append(dagger.Swing(playerpos=self.player.hitbox.center, mousepos=mp))
                        self.cooldown += 0.5
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.hud.set_selectangle(self.hud.slot - 1)
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.hud.set_selectangle(self.hud.slot + 1)
            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(window=self.window, background=self.surface)
                    self.prev_time = time.time()
                elif event.key == pygame.K_e:
                    self.surface.blit(img.misc["background"]["game"], (0, 0))
                    self.scene.draw(self.surface)
                    self.hud.save_hotbar()
                    show_inventory(window=self.window, background=self.surface)
                    self.hud.load_hotbar()
                    self.hud.update(player=self.player)
                    self.prev_time = time.time()
                elif event.key == pygame.K_SPACE and self.player.mana > 0:
                    self.player.dash()
                elif event.key == pygame.K_b:
                    if key[pygame.K_F3]:
                        var.soft_debug = not var.soft_debug
                        cout("soft_debug = " + str(var.soft_debug))
                elif event.key == pygame.K_h:
                    if key[pygame.K_F3]:
                        var.hard_debug = not var.hard_debug
                        cout("hard_debug = " + str(var.hard_debug))
                elif event.key == pygame.K_g:
                    if key[pygame.K_F3]:
                        var.render_all = not var.render_all
                        cout("render_all = " + str(var.render_all))
                elif event.key == pygame.K_f:
                    if key[pygame.K_F3]:
                        var.fps_meter = not var.fps_meter
                        cout("fps_meter = " + str(var.fps_meter))
                elif event.key == pygame.K_e:
                    pass
                elif event.key == pygame.K_1:
                    self.hud.set_selectangle(0)
                elif event.key == pygame.K_2:
                    self.hud.set_selectangle(1)
                elif event.key == pygame.K_3:
                    self.hud.set_selectangle(2)
                elif event.key == pygame.K_4:
                    self.hud.set_selectangle(3)
                elif event.key == pygame.K_5:
                    self.hud.set_selectangle(4)
                elif event.key == pygame.K_6:
                    self.hud.set_selectangle(5)
                elif event.key == pygame.K_x:
                    self.save()

        # end loop if exittomenu order is detected
        if globs.exittomenu:
            self.end_loop()
            globs.menu = True
