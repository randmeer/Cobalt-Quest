import pygame
import os
from distutils.dir_util import copy_tree
from shutil import rmtree
from octagon.utils import img, var, get_setting, set_setting, mp_screen, play_sound, save_settings
from octagon.gui import Overlay

from game import globs
from game.overlay.alert import Alert


# TODO: re-implement all legacy functionality

class Settings(Overlay):
    def __init__(self, window, background, arguments):
        super().__init__(window, background, arguments)
        self.add_group("tab", "content", "general", "audio", "video", "other")
        self.add_button(text="GENERAL", relpos=(0.15, 0.1), anchor="center", relsize=(0.2, 0.09), id="general", groups=["tab"])
        self.add_button(text="AUDIO", relpos=(0.3875, 0.1), anchor="center", relsize=(0.2, 0.09), id="audio", groups=["tab"])
        self.add_button(text="VIDEO", relpos=(0.6135, 0.1), anchor="center", relsize=(0.2, 0.09), id="video", groups=["tab"])
        self.add_button(text="OTHER", relpos=(0.85, 0.1), anchor="center", relsize=(0.2, 0.09), id="other", groups=["tab"])
        self.add_button(text="SAVE AND RETURN", relpos=(0.6, 0.85), anchor="topleft", relsize=(0.35, 0.09), id="back")

        self.add_group_leftclick_events(self.tab)
        self.add_leftclick_events(self.back)

        # audio
        self.add_label(text=f"VOLUME: {get_setting('volume')}", relpos=(0.05, 0.2), anchor="topleft", id="audio_volume", groups=["content", "audio"])
        self.add_label(text=f"BACKGROUND MUSIC: {get_setting('background_music')}", relpos=(0.05, 0.3), anchor="topleft", id="audio_music", groups=["content", "audio"])
        self.add_label(text="RELOAD SETTINGS GUI", relpos=(0.05, 0.2), anchor="topleft", id="other_reload", groups=["content", "other"])

        # video
        self.add_label(text="SELECT PACK", relpos=(0.05, 0.2), anchor="topleft", color=var.GRAYSHADES[0], id="video_selectpack", groups=["content", "video"])
        resourcepacks = os.listdir("./resources/resourcepacks")
        for i in range(len(resourcepacks)):
            self.add_label(text=resourcepacks[i], relpos=(0.05, 0.2 + 0.05 * i + 0.02 * i + 0.1), anchor="topleft", color=var.GRAYSHADES[2], id=f"video_packlist_{i}", groups=["content", "video"])

        self.add_label(text=f"RESOLUTION: {var.res_size}", relpos=(0.5, 0.2), anchor="topleft", id="video_res", groups=["content", "video"])
        self.add_label(text=f"ASPECT RATIO: {get_setting('aspect_ratio')}", relpos=(0.5, 0.3), anchor="topleft", id="video_ar", groups=["content", "video"])
        self.add_label(text=f"PARTICLES: True", relpos=(0.5, 0.4), anchor="topleft", id="video_part", groups=["content", "video"])

        self.add_keypress_function(self.keypress)

        for i in self.get_group("content"):
            i.set_visible(False)
        for i in self.get_group("general"):
            i.set_visible(True)
        self.get_component("general").set_pressed(True)


    def keypress(self, key):
        if key == pygame.K_ESCAPE:
            self.exit()

    def tab(self, component_id):
        play_sound("click")
        for i in self.get_group("tab"):
            i.set_pressed(False)
        self.get_component(component_id).set_pressed(True)
        for i in self.get_group("content"):
            i.set_visible(False)
        for i in self.get_group(component_id):
            i.set_visible(True)

    def back(self):
        self.exit()

'''
def show_settings(window, background):
    """
    background should be the current view of the window, not scaled,
    in order for the settings gui to look like it lays on top of the window
    """
    s = True
    while s:
        s = _show_settings(window=window, background=background)


def _show_settings(window, background):
    """
    local function of show_settings
    to re-run this function, call 'return True'
    to exit this function, call 'return False'
    """

    # dear future self, have fun trying to understand this
    play_sound('click')

    labels = []

    # audio tab labels
    labels.append(label.Label(tags=["audio", "volume"], text=f"VOLUME: {get_setting('volume')}", relpos=(0.05, 0.2), anchor="topleft"))
    labels.append(label.Label(tags=["audio", "music"], text=f"BACKGROUND MUSIC: {get_setting('background_music')}", relpos=(0.05, 0.3), anchor="topleft"))

    # video tab labels
    resourcepacks = os.listdir("./resources/resourcepacks")
    for i in range(len(resourcepacks)):
        labels.append(label.Label(tags=["video", "packlist"], text=resourcepacks[i], relpos=(0.05, 0.2+0.05*i+0.02*i+0.1), anchor="topleft", color=var.GRAYSHADES[2]))

    # for i in range(len(var.res))
    labels.append(label.Label(tags=["video", ""], text="SELECT PACK", relpos=(0.05, 0.2), anchor="topleft", color=var.GRAYSHADES[0]))
    labels.append(label.Label(tags=["video", "res"], text="RESOLUTION:", relpos=(0.5, 0.2), anchor="topleft"))
    labels.append(label.Label(tags=["video", "part"], text="PARTICLES:", relpos=(0.5, 0.4), anchor="topleft"))
    labels.append(label.Label(tags=["video", "ratio"], text="ASPECT RATIO:", relpos=(0.5, 0.3), anchor="topleft"))

    # other tab labels
    labels.append(label.Label(tags=["other"], text="RELOAD SETTINGS GUI", relpos=(0.05, 0.2), anchor="topleft"))

    settings_gui = GUI(background=background, overlay=200, labels=labels, buttons=[
        button.Button(tags=["general", ""], anchor="center", relsize=(0.2, 0.1), text="GENERAL", relpos=(0.15, 0.1)),
        button.Button(tags=["audio", ""], anchor="center", relsize=(0.2, 0.1), text="AUDIO", relpos=(0.3875, 0.1)),
        button.Button(tags=["video", ""], anchor="center", relsize=(0.2, 0.1), text="VIDEO", relpos=(0.6135, 0.1)),
        button.Button(tags=["other", ""], anchor="center", relsize=(0.2, 0.1), text="OTHER", relpos=(0.85, 0.1)),
        button.Button(tags=["", ""], anchor="topleft", relsize=(0.35, 0.09), text="SAVE AND RETURN", relpos=(0.6, 0.85))])

    for i in settings_gui.labelgroup:
        if i.tags[0] == "video" and i.tags[1] == "packlist":
            i.render_outline()

    for i in settings_gui.labelgroup:
        if i.tags[0] == "video" and i.text == get_setting("resourcepack"):
            i.set_outline(outline=True)

    settings_gui.buttongroup[0].set_pressed(press=True)
    current_tab = "general"

    def set_current_tab():
        for i in settings_gui.labelgroup:
            i.set_visible(visible=True)
            if i.tags[0] != current_tab:
                i.set_visible(visible=False)
    set_current_tab()

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    if settings_gui.buttongroup[4].rect.collidepoint(mp):
                        run = False

                    # button click events
                    for i in range(4):
                        if settings_gui.buttongroup[i].rect.collidepoint(mp):
                            for j in range(4):
                                settings_gui.buttongroup[j].set_pressed(press=False)
                            settings_gui.buttongroup[i].set_pressed(press=True)
                            current_tab = settings_gui.buttongroup[i].tags[0]
                            set_current_tab()
                            play_sound('click')

                    # label click events
                    for i in settings_gui.labelgroup:
                        if i.rect.collidepoint(mp) and i.visible:

                            # clicked label is video.pack
                            if i.tags[0] == "video":
                                if i.tags[1] == "packlist":
                                    for j in settings_gui.labelgroup:
                                        if j.tags[0] == "video" and j.tags[1] == "packlist":
                                            j.set_outline(outline=False)
                                    i.set_outline(outline=True)
                                    set_setting('resourcepack', i.text)
                                    img.load()
                                    play_sound('click')

                            if i.tags[0] == "audio":

                                # clicked label is audio.volume
                                if i.tags[1] == "volume":
                                    set_setting('volume', get_setting('volume') + 1)
                                    if get_setting('volume') > 10:
                                        set_setting('volume', 0)
                                    i.text = f"VOLUME: {get_setting('volume')}"
                                    i.render()
                                    play_sound('click')

                                # clicked label is audio.music
                                if i.tags[1] == "music":
                                    set_setting('background_music', not get_setting('background_music'))
                                    i.text = f"BACKGROUND MUSIC: {get_setting('background_music')}"
                                    i.render()
                                    play_sound('click')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        if globs.quitgame:
            run = False
        if run:
            settings_gui.draw(window=window)

    save_settings()
    play_sound('click')
    return False

'''