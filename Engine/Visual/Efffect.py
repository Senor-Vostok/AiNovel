import pygame
import datetime
from Engine.Constants import DEFAULT_COLOR, SPEED_ANIMATION_TEXT


class Effect(pygame.sprite.Sprite):
    def __init__(self, xoy, animation, recursive=False, speed=0.3):
        pygame.sprite.Sprite.__init__(self)
        self.timer = datetime.datetime.now()
        self.time_delta = speed * 1000
        self.recursive = recursive
        self.image = animation[0]
        self.effect = animation
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move):
        stadia = (datetime.datetime.now() - self.timer).microseconds // self.time_delta
        if stadia >= len(self.effect) and self.recursive:
            stadia = 0
            self.timer = datetime.datetime.now()
        elif stadia >= len(self.effect):
            return False
        self.image = self.effect[stadia]
        self.rect.move_ip(move)
        return True


class Information(pygame.sprite.Sprite):
    def __init__(self, xoy, text, resizer=1, back_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.xoy = xoy
        self.font = pygame.font.SysFont('progresspixel-bold', int(30 * resizer))
        self.resizer = resizer
        self.speed_animation = SPEED_ANIMATION_TEXT
        self.image = self.font.render(text, 1, DEFAULT_COLOR)
        self.back_image = pygame.transform.scale(back_image, (self.image.get_rect()[2] * 1.1, back_image.get_rect()[3])).convert_alpha()
        self.timer = datetime.datetime.now()
        self.rect = self.back_image.get_rect()
        self.rect.x = xoy[0] + self.back_image.get_rect()[0]
        self.rect.y = xoy[1]
        self.flag = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move):
        if self.xoy[0] - self.rect.x < self.rect[2] and not self.flag:
            self.rect.x -= self.speed_animation
        elif self.xoy[0] - self.rect.x >= self.rect[2] and not self.flag:
            self.flag = True
            self.timer = datetime.datetime.now()
        elif (datetime.datetime.now() - self.timer).seconds > 1 and self.flag:
            self.rect.x += self.speed_animation
            if self.rect.x >= self.xoy[0]:
                return False
        return True
