import pygame
import os

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)


class Sounds:
    def __init__(self):
        self.loaded_sound = dict()
        self.musics = [self.__load_sound(f"Assets/music/{file}") for file in os.listdir("Assets/music")]
        self.menu = [self.__load_sound(f"Assets/menuMusic/{file}") for file in os.listdir("Assets/menuMusic")]

    def __load_sound(self, file):
        try:
            if file not in self.loaded_sound:
                self.loaded_sound[file] = pygame.mixer.Sound(file)
            return self.loaded_sound[file]
        except Exception:
            return None
