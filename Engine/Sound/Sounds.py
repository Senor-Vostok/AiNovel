import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)


class Sounds:
    def __init__(self):
        self.loaded_sound = dict()
        # self.click = self.__load_sound(f'data/sounds/click.mp3') example

    def __load_sound(self, file):
        if file not in self.loaded_sound:
            self.loaded_sound[file] = pygame.mixer.Sound(file)
        return self.loaded_sound[file]
