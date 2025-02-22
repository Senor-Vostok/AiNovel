import copy
import sys
import pygame.display
from Engine.Texture.Textures import Textures
from Engine.Sound.Sounds import Sounds
from Engine.Logic.Machine import Scene
from Engine.Objects.MainCamera import MainCamera
from Engine.Visual.Efffect import Effect, Information
from win32api import GetSystemMetrics
from Engine.Constants import *
from Engine.Visual.Render import Render
from Engine.Logic.ShowInterface import *


class EventHandler:
    def __init__(self):
        pygame.mixer.init()
        pygame.display.set_caption('Test')
        # self.settings = dict()
        # self.volumes_channels = [1] * 8
        # self.language_data = dict()
        # self.export_language(self.settings['language'])
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (self.size[0] // 2, self.size[1] // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.textures = Textures()
        # self.screen.blit(self.textures.loading, (self.centre[0] - self.textures.loading.get_rect()[2] // 2, self.centre[1] - self.textures.loading.get_rect()[3] // 2))
        # pygame.display.flip()
        self.sounds = Sounds()
        # pygame.mouse.set_visible(False)
        # pygame.mixer.Channel(0).play(self.sounds.menu, -1)
        self.timer, self.timer_backmusic, self.last_interface = None, None, None
        self.logic = Scene(self)
        self.open_some, self.flag = True, True
        self.interfaces = dict()
        self.effects = list()  # Хранит объекты класса Effects
        self.camera = MainCamera()
        self.render = Render(self)
        self.saves_story = [{"name": "История бобра Максима", "launch": None},
                            {"name": "История бобра Максима", "launch": None},
                            {"name": "История бобра Максима", "launch": None},
                            {"name": "История бобра Максима", "launch": None},
                            {"name": "История бобра Максима", "launch": None}]
        show_UI(self, self.centre)
        # self.__xoy_information = [self.centre[0] * 2, self.centre[1] * 2 - self.textures.land['barrier'][0].get_rect()[2]]

    # def change_volume(self, slicer, channel):
    #     self.volumes_channels[channel] = slicer.now_sector / slicer.cuts  # Проценты
    #     pygame.mixer.Channel(channel).set_volume(self.volumes_channels[channel])

    def click_handler(self):
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.KEYDOWN:
                c = i
                if i.key == pygame.K_ESCAPE:
                    if len(self.interfaces) > 1:
                        self.interfaces.pop([_ for _ in self.interfaces if self.interfaces[_] == self.last_interface][0])
                        continue
                    # show_pause(self, self.centre) if 'pause' not in self.interfaces and not self.open_some else None
                if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
                if 'buildmenu' in self.interfaces: self.interfaces.pop('buildmenu')
                if 'choicegame' in self.interfaces: self.interfaces.pop('choicegame')
            if i.type == pygame.QUIT:
                self.quit()
        return c

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.clock.tick()
        self.render.rendering()

    #def quit(self):
    #     sys.exit()
