import pygame
import os
from win32api import GetSystemMetrics

pygame.init()
screen = pygame.display.set_mode()


class Textures:
    def __init__(self):  # 1920 1080
        self.loaded_textures = dict()
        self.resizer = GetSystemMetrics(0) / 1920
        self.priority = ["UI", "Objects", "Background"]
        self.font = pygame.font.Font('19363.ttf', int(20 * self.resizer))
        self.loading = self.render("Assets/Loading/logo.png", (1280, 720))
        self.back = self.render("Assets/UI/Menu/something.png", (1920, 1080))
        self.buttonBigButtonChoice = [self.render("Assets/UI/Menu/ButtonChoiceGame.png", (356 * 1.5, 68 * 1.5)),
                                      self.render("Assets/UI/Menu/ButtonChoiceGameT.png", (356 * 1.5, 68 * 1.5))]
        self.buttonBigButton = [self.render("Assets/UI/Menu/ButtonNewGame.png", (356 * 1.5, 68 * 1.5)),
                                self.render("Assets/UI/Menu/ButtonNewGameT.png", (356 * 1.5, 68 * 1.5))]
        self.buttonExit = [self.render("Assets/UI/Menu/ButtonExit.png", (356 * 1.5, 68 * 1.5)),
                                self.render("Assets/UI/Menu/ButtonExitT.png", (356 * 1.5, 68 * 1.5))]
        self.buttonStep = [self.render("Assets/UI/Dialog/back.png", (17 * 6, 9 * 6)),
                           self.render("Assets/UI/Dialog/backT.png", (17 * 6, 9 * 6))]
        self.EBack = [self.render("Assets/UI/Dialog/eback.png", (17 * 6, 9 * 6)),
                      self.render("Assets/UI/Dialog/ebackT.png", (17 * 6, 9 * 6))]
        self.Slicer = [self.render("Assets/UI/Menu/slicerback.png", (134 * 6, 2 * 6)),
                       self.render("Assets/UI/Menu/slicerbutton.png", (8 * 6, 8 * 6))]
        self.dialogLabel = self.render("Assets/UI/Dialog/DialogLabel.png", (205 * 6, 75 * 6))
        self.BackSettings = self.render("Assets/UI/Menu/Back.png", (156 * 6, 99 * 6))
        self.logo = self.render("Assets/UI/Menu/logo.png", (153 * 6, 52 * 6))

    def init_textures(self):
        self.characters = {name[:-4]: [self.render(f"Assets/Characters/{name}", (512, 512))] for name in
                           os.listdir("Assets/Characters")}
        self.locations = {name[:-4]: [self.render(f"Assets/Locations/{name}", (1920, 1080))] for name in
                          os.listdir("Assets/Locations")}
        self.DropDown = {"selected": [self.render("Assets/UI/DropDown/selected.png", (342, 48))],
                         "arrow": [self.render("Assets/UI/DropDown/arrow.png", (48, 48)),
                                   self.render("Assets/UI/DropDown/arrowt.png", (48, 48))],
                         "variant": [self.render("Assets/UI/DropDown/variant.png", (390, 48)),
                                     self.render("Assets/UI/DropDown/variantt.png", (390, 48))]}

    def post_render(self, texture, size):
        return pygame.transform.scale(texture, size).convert_alpha()

    def render(self, address, size):
        if address in self.loaded_textures:
            return self.loaded_textures[address]
        size = size[0] * self.resizer, size[1] * self.resizer
        image = pygame.transform.scale(pygame.image.load(address), size).convert_alpha()
        self.loaded_textures[address] = image
        return image
