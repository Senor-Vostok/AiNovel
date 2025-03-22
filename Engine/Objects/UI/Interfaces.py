from Engine.Objects.UI import Widgets as W
import pygame
import random

screen_width = None
screen_height = None


class Test:
    def __init__(self, language_data, xoy, textures):
        self.hello = W.Label("Hello Team 1 :))", (xoy[0], xoy[1] + 100), 80, 100, (255, 255, 255))

        self.image = W.Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))

        self.figure = W.Figure([xoy[0], xoy[1] - 100], (48, 35, 22, 255),
                               form=[[100, 30], [30, 100], [100, 100], [30, 30], [100, 30]], thickness=2,
                               color_bord=(252, 0, 0, 255))

        self.circle = W.Circle([xoy[0], xoy[1] + 200], (48, 35, 22, 255), radius=100, thickness=2,
                               color_bord=(252, 0, 0, 0))
        self.dropdown = W.DropDown(
            textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"],
            (xoy[0], xoy[1] + 200), ("1", "2", "3", "4", "5"))
        self.background = W.Image(textures.locations["InsideTheCircusTent"][0], xoy)
        self.surface = W.Surface(self.background, self.image, self.hello, self.figure, self.dropdown)


class Entry:
    def __init__(self, text, func=None):
        self.text = text
        self.function = func


class MainMenu:
    def __init__(self, language_data, xoy, textures, saves_story, new_story):
        self.textures = textures
        self.screen_width = xoy[0] * 2
        self.screen_height = xoy[1] * 2
        self.entries = [W.Entry(story["name"], story["launch"]) for story in saves_story]
        self.surface = W.Surface()

        location = self.textures.locations[random.choice(list(self.textures.locations.keys()))][0]
        self.surface.widgets.append(W.Image(location, xoy))

        character = self.textures.characters[random.choice(list(self.textures.characters.keys()))][0]
        character = self.textures.post_render(character, (character.get_rect()[2] * 1.8, character.get_rect()[3] * 1.8))
        xoy_image = ((self.screen_width - character.get_rect()[2] / 2 - 10) * self.textures.resizer, (self.screen_height - character.get_rect()[3] / 2) * self.textures.resizer)
        self.surface.widgets.append(W.Image(character, xoy_image))

        # back = self.textures.back
        # self.surface.widgets.append(W.Image(back, xoy))

        img = self.textures.buttonBigButton[0]
        xoy_image = ((img.get_rect()[2] / 2 + 200) * self.textures.resizer, (img.get_rect()[3] / 2 + 100) * self.textures.resizer)
        self.NewStory = W.Button(self.textures.buttonBigButton, xoy_image, text="New Story", colors=[(10, 52, 35), (83, 38, 8)])
        self.LastStory = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 1.2), text="Continue", colors=[(10, 52, 35), (83, 38, 8)])
        self.LoadStory = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 2.4), text="Load", colors=[(10, 52, 35), (83, 38, 8)])
        self.Settings = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 3.6), text="Settings", colors=[(10, 52, 35), (83, 38, 8)])
        self.AI = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 4.8), text="Connect AI", colors=[(10, 52, 35), (83, 38, 8)])
        self.Custom = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 6), text="My sprites", colors=[(10, 52, 35), (83, 38, 8)])
        self.Quite = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 7.2), text="Quite", colors=[(10, 52, 35), (83, 38, 8)])
        self.NewStory.connect(new_story)
        self.surface.widgets.append(self.NewStory)
        self.surface.widgets.append(self.LastStory)
        self.surface.widgets.append(self.LoadStory)
        self.surface.widgets.append(self.Settings)
        self.surface.widgets.append(self.AI)
        self.surface.widgets.append(self.Custom)
        self.surface.widgets.append(self.Quite)

        img = self.textures.logo
        xoy_image = ((self.screen_width - img.get_rect()[2] / 2) * self.textures.resizer, (img.get_rect()[3] / 2) * self.textures.resizer)
        self.NewStory = W.Image(self.textures.logo, xoy_image)
        self.surface.widgets.append(self.NewStory)


class NewStoryCreationScreen:
    def __init__(self, language_data, xoy, textures):
        self.screen_width = xoy[0] * 2
        self.screen_height = xoy[1] * 2
        print(screen_width)
        print(xoy[0])
        left_column_horizontal_position = self.screen_width * 0.1
        right_column_horizontal_position = self.screen_width - self.screen_width * 0.4
        print(left_column_horizontal_position)

        self.title = W.Label(text="Новая история",
                             xoy=(left_column_horizontal_position, self.screen_height * 0.1),
                             pp=80, board_size=100, color=(0, 0, 0), centric=False)

        self.genre_label = W.Label(text="Жанр",
                                   xoy=(left_column_horizontal_position, self.screen_height * 0.2),
                                   pp=80, board_size=100, color=(0, 0, 0), centric=False)

        actors_vertical_position = self.screen_height * 0.3
        self.actors_label = W.Label(text="Действующие лица",
                                    xoy=(left_column_horizontal_position, actors_vertical_position),
                                    pp=80, board_size=100, color=(0, 0, 0), centric=False)

        add_actors_plus_symbol_line_half_length = 20
        add_actors_plus_symbol_line_half_width = 2
        add_actors_plus_symbol_position = (right_column_horizontal_position, actors_vertical_position)

        bottom_left_plus_point = [-add_actors_plus_symbol_line_half_width, -add_actors_plus_symbol_line_half_length]
        bottom_right_plus_point = [add_actors_plus_symbol_line_half_width, -add_actors_plus_symbol_line_half_length]
        top_left_plus_point = [-add_actors_plus_symbol_line_half_width, add_actors_plus_symbol_line_half_length]
        top_right_plus_point = [add_actors_plus_symbol_line_half_width, add_actors_plus_symbol_line_half_length]
        print(bottom_left_plus_point, top_left_plus_point, top_right_plus_point, bottom_right_plus_point)

        left_bottom_plus_point = [-add_actors_plus_symbol_line_half_length, -add_actors_plus_symbol_line_half_width]
        left_top_plus_point = [-add_actors_plus_symbol_line_half_length, add_actors_plus_symbol_line_half_width]
        right_top_plus_point = [add_actors_plus_symbol_line_half_length, add_actors_plus_symbol_line_half_width]
        right_bottom_plus_point = [add_actors_plus_symbol_line_half_length, -add_actors_plus_symbol_line_half_width]

        add_actors_plus_symbol_vertical = W.Figure(xoy=add_actors_plus_symbol_position,
                                                   color=(0, 0, 0),
                                                   form=[bottom_left_plus_point, top_left_plus_point,
                                                         top_right_plus_point, bottom_right_plus_point],
                                                   thickness=1)

        add_actors_plus_symbol_horizontal = W.Figure(xoy=add_actors_plus_symbol_position,
                                                     color=(0, 0, 0),
                                                     form=[left_bottom_plus_point, left_top_plus_point,
                                                           right_top_plus_point, right_bottom_plus_point],
                                                     thickness=1)

        self.add_actors_plus_symbol = [add_actors_plus_symbol_vertical, add_actors_plus_symbol_horizontal]

        self.desctiption_label = W.Label(text="Описание или вступление:",
                                         xoy=(left_column_horizontal_position, self.screen_height * 0.45),
                                         pp=80, board_size=100, color=(0, 0, 0), centric=False)

        description_field_position = (xoy[0], self.screen_height * 0.7)
        description_field_height = self.screen_height * 0.3

        top_left = (-(xoy[0] - left_column_horizontal_position),
                    description_field_height // 2)

        top_right = ((xoy[0] - left_column_horizontal_position),
                     description_field_height // 2)

        bottom_right = ((xoy[0] - left_column_horizontal_position),
                        -(description_field_height // 2))

        bottom_left = (-(xoy[0] - left_column_horizontal_position),
                       -(description_field_height // 2))

        self.description_field_figure = W.Figure(xoy=description_field_position,
                                                 color=(255, 255, 255),
                                                 color_bord=(0, 0, 0, 255),
                                                 form=[top_left, top_right, bottom_right, bottom_left],
                                                 thickness=2)

        self.elements = [self.title, self.genre_label, self.actors_label, self.desctiption_label,
                         self.description_field_figure] + self.add_actors_plus_symbol

        self.surface = W.Surface(*self.elements)


class DialogueUI:
    def __init__(self, language_data, xoy, textures, cue):
        self.character_names = cue.get("Characters_names")
        self.location = cue.get("Location")
        self.main_character = cue.get("Main_character")
        self.dialog = cue.get("Dialog")
        self.textures = textures

        main_character_image = self.textures.characters[self.main_character][0]
        print(self.main_character)

        left_margin = xoy[0] * 2 * 0.05
        right_margin = xoy[0] * 2 * 0.95
        half_main_character_size = main_character_image.get_rect()[2] // 2
        main_character_vertical_position = xoy[1] - half_main_character_size
        half_other_characters_size = None

        other_characters_images = dict()
        for character_name in self.character_names:
            other_char_image = self.textures.characters[character_name][0]
            scale = 0.5
            other_char_image = self.textures.post_render(other_char_image,
                                                         (other_char_image.get_rect()[2] * scale,
                                                          other_char_image.get_rect()[3] * scale))
            other_characters_images[character_name] = other_char_image

            if half_other_characters_size is None:
                half_other_characters_size = other_char_image.get_rect()[3] // 2

        self.background = W.Image(textures.locations[self.location][0], xoy)

        self.text_box = W.Figure([xoy[0], xoy[1] + xoy[1] // 2], (255, 255, 255, 255),
                                 form=[[xoy[0], xoy[1] // 4], [xoy[0], -xoy[1] // 4], [-xoy[0], -xoy[1] // 4],
                                       [-xoy[0], xoy[1] // 4]])

        self.text = W.Label(self.dialog, (left_margin, xoy[1]), 50, xoy[0] * 2 * 0.9, lines=7, centric=False)

        self.main_character_image_widget = W.Image(main_character_image, (
        left_margin + half_main_character_size, main_character_vertical_position))

        self.elements = [self.background, self.text_box, self.text, self.main_character_image_widget]

        other_character_horizontal_position = right_margin - half_other_characters_size
        other_character_vertical_position = xoy[1] - half_other_characters_size

        print(right_margin)
        for char_image in other_characters_images.values():
            self.elements.append(
                W.Image(char_image, (other_character_horizontal_position, other_character_vertical_position)))
            other_character_horizontal_position -= half_other_characters_size * 2

        self.surface = W.Surface(*self.elements)

# how to get image: image = self.textures.characters[random.choice(list(self.textures.characters.keys()))][0]
