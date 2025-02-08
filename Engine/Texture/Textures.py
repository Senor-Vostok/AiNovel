import pygame
from win32api import GetSystemMetrics


pygame.init()
screen = pygame.display.set_mode()


class Textures:
    def __init__(self):
        self.loaded_textures = dict()
        self.resizer = GetSystemMetrics(0) / 1920
        self.priority = ["UI", "Objects", "Background"]
        self.font = pygame.font.Font('19363.ttf', int(20 * self.resizer))
        self.characters = {f"character{i + 1}": [self.render(f"Assets/Characters/character{i + 1}.png", (812, 256))] for i in range(18)}

    def post_render(self, texture, size):
        return pygame.transform.scale(texture, size).convert_alpha()

    def render(self, address, size):
        if address in self.loaded_textures:
            return self.loaded_textures[address]
        size = size[0] * self.resizer, size[1] * self.resizer
        image = pygame.transform.scale(pygame.image.load(address), size).convert_alpha()
        self.loaded_textures[address] = image
        return image
