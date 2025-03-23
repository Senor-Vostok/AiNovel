from Engine.Objects.UI import Widgets as W
import random

screen_width = None
screen_height = None


class ChoicePrefab:
    def __init__(self, language_data, xoy, textures):
        img = textures.buttonBigButton[0]
        self.character = W.Button(textures.buttonBigButtonChoice, (xoy[0] - (img.get_rect()[2] / 2) * 1.1, xoy[1]),
                                  text="Character", colors=[(10, 52, 35), (83, 38, 8)])
        self.location = W.Button(textures.buttonBigButtonChoice, (xoy[0] + (img.get_rect()[2] / 2) * 1.1, xoy[1]),
                                 text="Location", colors=[(10, 52, 35), (83, 38, 8)])
        self.surface = W.Surface(self.character, self.location)


class Settings:
    def __init__(self, language_data, xoy, textures):
        self.Back = W.Image(textures.BackSettings, xoy)
        self.VolumeSettingInf = W.Label(text="Volume", xoy=(
        xoy[0], xoy[1] - self.Back.image.get_rect()[3] / 2 + 50 * textures.resizer), size=20)
        self.VolumeSetting = W.Slicer(images=textures.Slicer,
                                      xoy=(xoy[0], xoy[1] - self.Back.image.get_rect()[3] / 2 + 90 * textures.resizer),
                                      cuts=100, now_sector=20)
        self.surface = W.Surface(self.Back, self.VolumeSettingInf, self.VolumeSetting)


class Entry:
    def __init__(self, text, func=None):
        self.text = text
        self.function = func


class MainMenu:
    def __init__(self, language_data, xoy, textures, saves_story, new_story, quit):
        self.textures = textures
        self.screen_width = xoy[0] * 2
        self.screen_height = xoy[1] * 2
        self.entries = [W.Entry(story["name"], story["launch"]) for story in saves_story]
        self.surface = W.Surface()

        location = self.textures.locations[random.choice(list(self.textures.locations.keys()))][0]
        self.surface.widgets.append(W.Image(location, xoy))

        character = self.textures.characters[random.choice(list(self.textures.characters.keys()))][0]
        character = self.textures.post_render(character, (character.get_rect()[2] * 1.8, character.get_rect()[3] * 1.8))
        xoy_image = ((self.screen_width - character.get_rect()[2] / 2 - 10) * self.textures.resizer,
                     (self.screen_height - character.get_rect()[3] / 2) * self.textures.resizer)
        self.surface.widgets.append(W.Image(character, xoy_image))

        img = self.textures.buttonBigButton[0]
        xoy_image = (
        (img.get_rect()[2] / 2 + 50) * self.textures.resizer, (img.get_rect()[3] / 2 + 100) * self.textures.resizer)
        self.NewStory = W.Button(self.textures.buttonBigButton, xoy_image, text="New Story",
                                 colors=[(10, 52, 35), (83, 38, 8)])
        self.LastStory = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 1.2),
                                  text="Continue", colors=[(10, 52, 35), (83, 38, 8)])
        self.LoadStory = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 2.4),
                                  text="Load", colors=[(10, 52, 35), (83, 38, 8)])
        self.Settings = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 3.6),
                                 text="Settings", colors=[(10, 52, 35), (83, 38, 8)])
        self.AI = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 4.8),
                           text="Connect AI", colors=[(10, 52, 35), (83, 38, 8)])
        self.Custom = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 6),
                               text="My sprites", colors=[(10, 52, 35), (83, 38, 8)])
        self.Quite = W.Button(self.textures.buttonExit, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 7.2),
                              text="Quite", colors=[(0, 0, 0), (83, 38, 8)])
        self.NewStory.connect(new_story)
        self.Quite.connect(quit)
        self.surface.widgets.append(self.NewStory)
        self.surface.widgets.append(self.LastStory)
        self.surface.widgets.append(self.LoadStory)
        self.surface.widgets.append(self.Settings)
        self.surface.widgets.append(self.AI)
        self.surface.widgets.append(self.Custom)
        self.surface.widgets.append(self.Quite)

        img = self.textures.logo
        xoy_image = ((self.screen_width - img.get_rect()[2] / 2) * self.textures.resizer,
                     (img.get_rect()[3] / 2) * self.textures.resizer)
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
    class Character:
        def __init__(self, name, position, dialogue=None, scale=1, texture=None):
            self.dialogue = dialogue
            self.name = name
            self.scale = scale
            if dialogue is not None:
                self.textures = dialogue.textures
            if texture is not None:
                self.texture = texture
            else:
                self.texture = self.textures.characters[self.name][0]

            self.scale_texture()
            self.size = self.texture.get_rect()[3]

            self.position = position

        def set_position_for_left_bottom_corner(self, position):
            size = self.texture.get_rect()[2]
            self.position = (position[0] + (size // 2), position[1] - (size // 2))
            return self

        def set_position_for_right_bottom_corner(self, position):
            size = self.texture.get_rect()[2]
            print(size)
            self.position = (position[0] - (size // 2), position[1] - (size // 2))
            return self

        def widget(self):
            return W.Image(self.texture, self.position)

        def scale_texture(self):
            self.texture = self.textures.post_render(self.texture, (self.texture.get_rect()[2] * self.scale, self.texture.get_rect()[3] * self.scale))

    def __init__(self, language_data, xoy, textures, dialogue_data, story_name=None):
        self.elements = []
        self.character_names = dialogue_data.get("Characters_names")
        self.location = dialogue_data.get("Location")
        self.main_character = dialogue_data.get("Main_character")
        self.dialog = dialogue_data.get("Dialog")
        self.textures = textures
        self.background = W.Image(textures.locations[self.location][0], xoy)
        self.elements.append(self.background)
        self.elements.append(
            DialogueUI.Character(self.main_character, xoy, self, scale=1.3)
            .set_position_for_left_bottom_corner((0, xoy[1] * 2))
            .widget()
        )
        img = textures.dialogLabel.get_rect()
        self.elements.append(W.InteractLabel(text=[self.dialog], xoy=(xoy[0] * 2 - img[2] // 2 - 20 * textures.resizer, xoy[1] * 2 - img[3] // 2 - 20 * textures.resizer), images=[textures.dialogLabel, textures.dialogLabel], active=False, size=30))
        character_position = (xoy[0] * 2 - xoy[0] * 2 * 0.01, xoy[1] * 2 - img[3] // 2 - 20 * textures.resizer - img[3] // 2)
        for character in self.character_names:
            character_obj = DialogueUI.Character(name=character, position=character_position, dialogue=self, scale=0.25).set_position_for_right_bottom_corner(character_position)
            self.elements.append(character_obj.widget())
            character_position = character_position[0] - character_obj.size, character_position[1]
        img = textures.buttonStep[0].get_rect()
        self.ButtonNextStep = W.Button(textures.buttonStep, (xoy[0] * 2 - 10 * textures.resizer - img[2] / 2, 10 * textures.resizer + img[3] / 2))
        self.ButtonBackStep = W.Button(textures.buttonStep, (10 * textures.resizer + img[2] / 2, 10 * textures.resizer + img[3] / 2))
        self.ReturnToMenu = W.Button(textures.EBack, (10 * textures.resizer + img[2] / 2, 10 * textures.resizer + img[3] * 1.6))
        self.surface = W.Surface(*self.elements, self.ButtonNextStep, self.ButtonBackStep, self.ReturnToMenu)
