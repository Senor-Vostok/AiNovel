import math

import pygame
from datetime import datetime
import Engine.Constants
from Engine.Constants import DEFAULT_COLOR, BACKGROUND_COLOR
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
        self.text = ['']
        self.current_text = 0
        self.func = None
        self.args = None
        self.active = active
        self.rect = self.image.get_rect(center=xoy)
        self.font = pygame.font.Font("19363.ttf", int(self.rect[3] * 0.3))
        self.timer = datetime.now()
        self.visible = True
        self.can_write = False
        self.surface = None
        self.text_image = None
        self.y = 0
        self.scroll_offset = 0
        self.scrollbar_width = 10
        self.scrollbar_rect = pygame.Rect(self.rect.width - self.scrollbar_width, 0, self.scrollbar_width,
                                          self.rect.height)
        self.scrollbar_handle_height = 50
        self.scrollbar_dragging = False
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.fill_surface()

    def fill_surface(self):
        pygame.draw.rect(self.surface, (0, 0, 0, 0), self.rect)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))
        y_offset = -self.scroll_offset
        for idx, line in enumerate(self.text):
            text_surface = self.font.render(line, False, (0, 0, 0))
            if text_surface.get_width() > self.rect.width * 0.9:
                words = line.split('|')
                new_line = ''
                for word in words:
                    test_line = new_line + word
                    if self.font.size(test_line)[0] < self.rect.width * 0.9:
                        new_line = test_line
                    else:
                        self.surface.blit(self.font.render(new_line, False, (0, 0, 0)), (5, y_offset))
                        new_line = word
                self.surface.blit(self.font.render(new_line, False, (0, 0, 0)), (5, y_offset))
                y_offset += self.font.get_height()
            else:
                self.surface.blit(text_surface, (5, y_offset))
                y_offset += self.font.get_height()
        total_text_height = self.font.get_height() * len(self.text)
        scrollbar_handle_y = (self.scroll_offset / total_text_height) * self.rect.height
        scrollbar_handle_height = (self.rect.height / total_text_height) * self.rect.height
        pygame.draw.rect(self.surface, (200, 200, 200), self.scrollbar_rect)
        pygame.draw.rect(self.surface, (100, 100, 100),
                         (self.scrollbar_rect.x, scrollbar_handle_y,
                            self.scrollbar_width, scrollbar_handle_height))
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.surface, (self.rect.x, self.rect.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if not self.active:
            return
        elif (datetime.now() - self.timer).seconds > 0.15 and not ''.join(self.text[self.current_text].split('/')):
            self.text[self.current_text] = self.text[self.current_text] + '/'\
                if self.visible else self.text[self.current_text][:-1]
            self.timer = datetime.now()
            self.visible = not self.visible
        elif (not self.rect.colliderect(pygame.Rect(mouse_click[0], mouse_click[1], 1, 1))
              and mouse_click[2] and mouse_click[3] == 1):
            self.can_write = False
            self.image = self.state
        elif (self.rect.colliderect(pygame.Rect(mouse_click[0], mouse_click[1], 1, 1))
              and mouse_click[2] and mouse_click[3] == 1):
            self.can_write = True
            self.image = self.flex
        elif self.can_write:
            self.go_write(command)
        if self.scrollbar_rect.collidepoint(mouse_click[0] - self.rect.x, mouse_click[1] - self.rect.y):
            if mouse_click[2]:
                self.scrollbar_dragging = True
        elif not mouse_click[2]:
            self.scrollbar_dragging = False
        if self.scrollbar_dragging:
            total_text_height = sum(self.font.size(line)[1] for line in self.text)
            scrollbar_handle_y = mouse_click[1] - self.rect.y
            self.scroll_offset = (scrollbar_handle_y / self.rect.height) * total_text_height
            self.scroll_offset = max(0, min(self.scroll_offset, total_text_height - self.rect.height))

    def go_write(self, command):
        if command:
            self.text[self.current_text] = ''.join(self.text[self.current_text].split('/'))
            if (command.key == pygame.K_v) and (command.mod & pygame.KMOD_CTRL):
                self.text[self.current_text] = (self.text[self.current_text] +
                                                ("".join(str(pygame.scrap.get(pygame.SCRAP_TEXT))[2:].split(r"\x00"))))
            elif command.key == pygame.K_BACKSPACE:
                if self.text[self.current_text]:
                    self.text[self.current_text] = self.text[self.current_text][:-1]
                elif self.current_text > 0:
                    self.text.pop(self.current_text)
                    self.current_text -= 1
            elif command.key == pygame.K_RETURN:
                if self.func:
                    self.func(*self.args)
            elif len(str(command.unicode)) > 0 and command.type == pygame.KEYDOWN:
                self.text[self.current_text] = self.text[self.current_text] + command.unicode
                if self.font.size(self.text[self.current_text])[0] > self.rect.width * 0.9:
                    self.current_text += 1
                    self.text.append('')


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


class Label(pygame.sprite.Sprite): # если хотите переносить на другую строчку нужно в тексте указывать \n сам класс не определяет момент переноса
    def __init__(self, text, xoy, pp, color=DEFAULT_COLOR, centric=True):
        pygame.sprite.Sprite.__init__(self)
        text = str(text)
        self.color = color
        self.text = text
        self.size = pp
        self.font = pygame.font.Font("19363.ttf", pp)
        self.label = []
        self.current_label = 0
        for text in self.text.split('\n'):
            self.label.append(self.font.render(text, 1, color))
        self.rect = self.label[0].get_rect(center=xoy)
        if not centric:
            self.rect.x, self.rect.y = xoy
        self.scroll_offset = 0
        self.scrollbar_width = 10
        self.scrollbar_rect = pygame.Rect(self.rect.width - self.scrollbar_width + 10, 0, self.scrollbar_width,
                                          self.rect.height)
        self.scrollbar_handle_height = 50
        self.scrollbar_dragging = False
        self.surface = None
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.Surface((self.rect.width + 10, self.rect.height))
        self.surface.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, self.rect)

    def new_text(self, text):
        text = str(text)
        self.label.clear()
        for text in text.split('\n'):
            self.label.append(self.font.render(text, 1, self.color))

    def draw(self, screen):
        self.surface.fill(BACKGROUND_COLOR)
        y_offset = -self.scroll_offset

        for idx, line in enumerate(self.label):
            self.surface.blit(line, (0, y_offset))
            y_offset += self.size * 1.5
        total_text_height = len(self.label) * self.size * 1.5
        if total_text_height > self.rect.height:
            scrollbar_handle_y = (self.scroll_offset / total_text_height) * self.rect.height
            scrollbar_handle_height = (self.rect.height / total_text_height) * self.rect.height
            pygame.draw.rect(self.surface, (200, 200, 200), self.scrollbar_rect)
            pygame.draw.rect(self.surface, (100, 100, 100),
                             (self.scrollbar_rect.x, scrollbar_handle_y,
                              self.scrollbar_width, scrollbar_handle_height))

        screen.blit(self.surface, (self.rect.x, self.rect.y))

    def update(self, mouse_click, command=None):
        if mouse_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.scrollbar_rect.collidepoint(mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y):
                if mouse_click[0]:
                    self.scrollbar_dragging = True

        if not pygame.mouse.get_pressed()[0]:
            self.scrollbar_dragging = False

        if self.scrollbar_dragging:
            mouse_pos = pygame.mouse.get_pos()
            total_text_height = len(self.label) * self.size * 1.5
            scrollbar_handle_y = mouse_pos[1] - self.rect.y
            self.scroll_offset = (scrollbar_handle_y / self.rect.height) * total_text_height
            self.scroll_offset = max(0, min(self.scroll_offset, total_text_height - self.rect.height))


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
