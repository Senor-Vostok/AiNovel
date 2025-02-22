import math

import pygame
from datetime import datetime
import Engine.Constants
from Engine.Constants import DEFAULT_COLOR
from Engine.Sound.Sounds import Sounds
from win32api import GetSystemMetrics

sounds = Sounds()


class Button(pygame.sprite.Sprite):
    def __init__(self, images, xoy, active=True, text=None, colors=(Engine.Constants.TEXT_ENABLE, Engine.Constants.TEXT_DISABLE)):
        pygame.sprite.Sprite.__init__(self)
        self.xoy = xoy
        self.colors = colors
        self.main_color = self.colors[0]
        self.state = images[0]
        self.trigger = images[1]
        self.image = self.state
        self.text = text
        self.func = None
        self.args = None
        self.active = active
        self.rect = self.image.get_rect(center=xoy)
        self.font = pygame.font.Font("19363.ttf", self.rect[3] - self.rect[3] // 3)
        self.one_press = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        text = self.font.render(self.text, 1, self.main_color)
        center = text.get_rect(center=self.xoy)
        screen.blit(text, (center.x, center.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if not self.active:
            return
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1):
            self.image = self.trigger
            self.main_color = self.colors[0]
            if mouse_click[2] and mouse_click[3] == 1 and self.func:
                if self.one_press:
                    self.one_press = False
                    # pygame.mixer.Channel(1).play(sounds.click)
                    self.func(*self.args)
            else:
                self.one_press = True
        else:
            self.image = self.state
            self.main_color = self.colors[1]


class Switch(pygame.sprite.Sprite):
    def __init__(self, images, xoy, active=False):
        pygame.sprite.Sprite.__init__(self)
        self.active = active
        self.enable = images[0]
        self.disable = images[1]
        self.one_press = False
        self.func, self.args = None, None
        if self.active:
            self.image = self.enable
        else:
            self.image = self.disable
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            if self.one_press:
                return
            # pygame.mixer.Channel(1).play(sounds.click)
            self.one_press = True
            self.active = not self.active
            self.image = self.enable if self.active else self.disable
        else:
            self.one_press = False


class Slicer(pygame.sprite.Sprite):
    def __init__(self, images, xoy, cuts=1, now_sector=1):
        pygame.sprite.Sprite.__init__(self)
        self.back_image = images[0]
        self.point_image = images[1]
        self.cuts = cuts
        self.func, self.args = None, None
        self.now_sector = now_sector
        self.rect = self.back_image.get_rect(center=xoy)

    def draw(self, screen):
        delta_x = ((self.rect[2] - self.point_image.get_rect()[2]) / self.cuts) * self.now_sector
        screen.blit(self.back_image, self.rect)
        screen.blit(self.point_image,
                    (self.rect.x + delta_x, self.rect.y - (self.point_image.get_rect()[3] // 2 - self.rect[3] // 2)))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            if self.now_sector != (mouse_click[0] - self.rect[0]) // (self.rect[2] / self.cuts) + 1:
                if self.func:
                    self.func(*self.args)
                self.now_sector = int((mouse_click[0] - self.rect[0]) // (self.rect[2] / self.cuts) + 1)


class InteractLabel(pygame.sprite.Sprite):
    def __init__(self, images, xoy, active=True, center=False):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.state = images[0]
        self.flex = images[1]
        self.image = self.state
        self.text = ''
        self.func = None
        self.args = None
        self.active = active
        self.rect = self.image.get_rect(center=xoy)
        self.font = pygame.font.Font("19363.ttf", self.rect[3] - self.rect[3] // 3)
        self.timer = datetime.now()
        self.visible = True
        self.can_write = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        image = self.font.render(self.text, False, DEFAULT_COLOR if self.can_write else Engine.Constants.TEXT_DISABLE)
        i = 1
        while image.get_rect()[2] < self.rect[2] - 50 and i <= len(self.text):
            image = self.font.render(self.text[-i:], False,
                                     DEFAULT_COLOR if self.can_write else Engine.Constants.TEXT_DISABLE)
            i += 1
        if not self.center:
            screen.blit(image, (self.rect[0] + 10, self.rect[1] + 6))
        else:
            screen.blit(image, (self.rect[0] + self.rect[2] // 2 - image.get_rect()[2] // 2, self.rect[1] + 6))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if not self.active:
            return
        elif (datetime.now() - self.timer).seconds > 0.15 and not ''.join(self.text.split('/')):
            self.text = self.text + '/' if self.visible else self.text[:-1]
            self.timer = datetime.now()
            self.visible = not self.visible
        elif not self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            self.can_write = False
            self.image = self.state
        elif self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            self.can_write = True
            self.image = self.flex
        elif self.can_write:
            self.go_write(command)

    def go_write(self, command):
        if command:
            self.text = ''.join(self.text.split('/'))
            if (command.key == pygame.K_v) and (command.mod & pygame.KMOD_CTRL):
                self.text = self.text + ("".join(str(pygame.scrap.get(pygame.SCRAP_TEXT))[2:].split(r"\x00")))
            elif command.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif int(command.key) == Engine.Constants.KEY_ENTER:
                if self.func:
                    self.func(*self.args)
            elif len(str(command.unicode)) > 0 and command.type == pygame.KEYDOWN:
                self.text = self.text + command.unicode


class Surface:
    def __init__(self, *args):
        self.widgets = list()
        for i in args:
            self.widgets.append(i)

    def add(self, widget):
        self.widgets.append(widget)

    def delete(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)

    def update(self, mouse_click, screen, command=None):
        for i in self.widgets:
            i.update(mouse_click, command)
            i.draw(screen)


class Label(pygame.sprite.Sprite):
    def __init__(self, text, xoy, pp, color=DEFAULT_COLOR, centric=True):
        pygame.sprite.Sprite.__init__(self)
        text = str(text)
        self.color = color
        self.text = text
        self.size = pp
        self.font = pygame.font.Font("19363.ttf", pp)
        self.label = list()
        for text in self.text.split('\n'):
            self.label.append(self.font.render(text, 1, color))
        self.rect = self.label[0].get_rect(center=xoy)
        if not centric:
            self.rect.x, self.rect.y = xoy

    def new_text(self, text):
        text = str(text)
        self.label.clear()
        for text in text.split('\n'):
            self.label.append(self.font.render(text, 1, self.color))

    def draw(self, screen):
        for i in range(len(self.label)):
            screen.blit(self.label[i], (self.rect.x, self.rect.y + self.size * 1.5 * i))

    def update(self, mouse_click, command):
        pass


class Image(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, mouse_click, command):
        pass


class DropDown(pygame.sprite.Sprite):
    def __init__(self, images, xoy, texts):
        pygame.sprite.Sprite.__init__(self)
        self.center = images[3].get_rect(center=xoy)
        self.center.x += images[3].get_rect()[2] / 2
        self.is_open = False
        self.selected_text = InteractLabel([images[0], images[0]], (self.center.x - images[1].get_rect()[2] / 2, self.center.y), False)
        self.selected_text.text = texts[0]
        self.arrow_button = Button(images[1:3], (self.center.x + images[0].get_rect()[2] / 2, self.center.y))
        self.variants = list()
        for i, text in enumerate(texts):
            self.variants.append(Button(images[3:], (self.center[0], self.center[1] + (i + 1) * images[3].get_rect()[3]), text=text))
            self.variants[-1].connect(self.select_variant, text)
        self.arrow_button.connect(self.open_close)

    def select_variant(self, text):
        self.selected_text.text = text

    def open_close(self):
        self.is_open = not self.is_open

    def draw(self, screen):
        self.selected_text.draw(screen)
        self.arrow_button.draw(screen)
        if not self.is_open:
            return
        for obj in self.variants:
            obj.draw(screen)

    def update(self, mouse_click, command):
        self.selected_text.update(mouse_click, command)
        self.arrow_button.update(mouse_click, command)
        if not self.is_open:
            return
        for obj in self.variants:
            obj.update(mouse_click, command)


class Figure(pygame.sprite.Sprite):
    def __init__(self, xoy, color, color_bord=(0, 0, 0, 0), form=[...], thickness=1):
        pygame.sprite.Sprite.__init__(self)
        self.local_form = form
        self.local_center = []
        self.xoy = xoy
        self.color = color
        self.color_bord = color_bord
        self.thickness = thickness
        self.surface = None
        self.create_surface()

    def create_surface(self):
        delta_x, delta_y = (max([_[0] for _ in self.local_form]) - min([_[0] for _ in self.local_form]),
                            max([_[1] for _ in self.local_form]) - min([_[1] for _ in self.local_form]))
        self.local_center = ((delta_x + self.thickness * 2) / 2, (delta_y + self.thickness * 2) / 2)
        self.surface = pygame.Surface((delta_x + self.thickness * 2, delta_y + self.thickness * 2), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.fill_surface()

    def fill_surface(self):
        zero_x, zero_y = min([_[0] for _ in self.local_form]), min([_[1] for _ in self.local_form])
        form = [(i[0] - zero_x + self.thickness, i[1] - zero_y + self.thickness) for i in self.local_form]
        pygame.draw.polygon(self.surface, self.color, form)
        pygame.draw.polygon(self.surface, self.color_bord, form, self.thickness) if self.color_bord != (0, 0, 0, 0) else None

    def draw(self, screen):
        screen.blit(self.surface, (self.xoy[0] - self.local_center[0], self.xoy[1] - self.local_center[1]))

    def update(self, mouse_click, command):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, xoy, color, color_bord=(0, 0, 0, 0), radius=1, thickness=0):
        pygame.sprite.Sprite.__init__(self)
        self.xoy = xoy
        self.color = color
        self.color_bord = color_bord
        self.radius = radius
        self.thickness = thickness
        self.surface = None
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.Surface((2 * (self.radius + self.thickness), 2 * (self.radius + self.thickness)),
                                      pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.fill_surface()

    def fill_surface(self):
        center = (self.radius + self.thickness, self.radius + self.thickness)
        pygame.draw.circle(self.surface, self.color, center, self.radius)
        pygame.draw.circle(self.surface, self.color_bord, center, self.radius, self.thickness)

    def draw(self, screen):
        screen.blit(self.surface, (self.xoy[0] - self.radius - self.thickness, self.xoy[1] - self.radius - self.thickness))

    def update(self, mouse_click, command):
        pass

class Entry:
    def __init__(self, text: str, function=None):
        self.text = text
        self.function = function
