import pygame


class MainCamera(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mouse_click = (0, 0, None, None)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.KEYUP:
            pass
        pressed = True in pygame.mouse.get_pressed()
        number = None
        if pressed:
            number = [_ for _ in pygame.mouse.get_pressed()].index(True) + 1
        self.mouse_click = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], pressed, number]
