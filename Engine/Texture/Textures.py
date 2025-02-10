import pygame
import os
from win32api import GetSystemMetrics


pygame.init()
screen = pygame.display.set_mode()


class Textures:
    def __init__(self):
        self.loaded_textures = dict()
        self.resizer = GetSystemMetrics(0) / 1920
        self.priority = ["UI", "Objects", "Background"]
        self.font = pygame.font.Font('19363.ttf', int(20 * self.resizer))
        self.characters = {name[:-4]: [self.render(f"Assets/Characters/{name}", (512, 512))] for name in os.listdir("Assets/Characters")}
        self.locations = {name[:-4]: [self.render(f"Assets/Locations/{name}", (1920, 1080))] for name in os.listdir("Assets/Locations")}
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
