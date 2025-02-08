from Engine.Launch.Handler import EventHandler
import pygame

if __name__ == "__main__":
    pygame.init()
    handler = EventHandler()
    while True:
        handler.update()
