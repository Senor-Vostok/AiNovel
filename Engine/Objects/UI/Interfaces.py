from Engine.Objects.UI import Widgets as W
import random

screen_width = None
screen_height = None


class ChoicePrefab:
    def __init__(self, language_data, xoy, textures):
        img = textures.buttonBigButton[0]
        self.character = W.Button(textures.buttonBigButtonChoice, (xoy[0] - (img.get_rect()[2] / 2) * 1.1, xoy[1]),
                                  text="Персонаж", colors=[(10, 52, 35), (83, 38, 8)])
        self.location = W.Button(textures.buttonBigButtonChoice, (xoy[0] + (img.get_rect()[2] / 2) * 1.1, xoy[1]),
                                 text="Место", colors=[(10, 52, 35), (83, 38, 8)])
        self.surface = W.Surface(self.character, self.location)


class Settings:
    def __init__(self, language_data, xoy, textures, api):
        self.Back = W.Image(textures.BackSettings, xoy)
        self.VolumeSettingInf = W.Label(text="Звук", xoy=(
            xoy[0], xoy[1] - self.Back.image.get_rect()[3] / 2 + 50 * textures.resizer), size=20)
        self.VolumeSetting = W.Slicer(images=textures.Slicer,
                                      xoy=(xoy[0], xoy[1] - self.Back.image.get_rect()[3] / 2 + 90 * textures.resizer),
                                      cuts=100, now_sector=20)
        self.ApiInf = W.Label(text="Ваш апи ключ от gpt", xoy=(xoy[0], xoy[1] - self.Back.image.get_rect()[3] / 2 + 170 * textures.resizer), size=20)
        cen = (xoy[0], xoy[1] - self.Back.image.get_rect()[3] / 2 + 220 * textures.resizer)
        self.ApiField = W.InteractLabel(textures.Field, xoy=(cen[0] - textures.Eye[0].get_rect()[2] / 2, cen[1]), size=textures.Field[0].get_rect()[3] - textures.Field[0].get_rect()[3] // 4, center=True, text=[api])
        self.Eye = W.Switch(textures.Eye, (cen[0] + textures.Field[0].get_rect()[2] / 2, cen[1]))
        self.surface = W.Surface(self.Back, self.VolumeSettingInf, self.VolumeSetting, self.ApiInf, self.ApiField, self.Eye)


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
            (img.get_rect()[2] / 2 + 100) * self.textures.resizer,
            (img.get_rect()[3] / 2 + 100) * self.textures.resizer)
        self.NewStory = W.Button(self.textures.buttonBigButton, xoy_image, text="История",
                                 colors=[(10, 52, 35), (83, 38, 8)])
        self.LoadStory = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 1.2),
                                  text="Сохраненные", colors=[(10, 52, 35), (83, 38, 8)])
        self.Settings = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 2.3),
                                 text="Настройки", colors=[(10, 52, 35), (83, 38, 8)])
        self.Custom = W.Button(self.textures.buttonBigButton, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 3.6),
                               text="Мой спрайт", colors=[(10, 52, 35), (83, 38, 8)])
        self.Quite = W.Button(self.textures.buttonExit, (xoy_image[0], xoy_image[1] + img.get_rect()[3] * 4.8),
                              text="Выход", colors=[(0, 0, 0), (83, 38, 8)])
        self.NewStory.connect(new_story)
        self.Quite.connect(quit)
        self.surface.widgets.append(self.NewStory)
        self.surface.widgets.append(self.LoadStory)
        self.surface.widgets.append(self.Settings)
        self.surface.widgets.append(self.Custom)
        self.surface.widgets.append(self.Quite)

        img = self.textures.logo.get_rect()
        xoy_image = (50 * self.textures.resizer + img[2] / 2, xoy[1] * 2 - 50 * self.textures.resizer - img[3] / 2)
        self.Logo = W.Image(self.textures.logo, xoy_image)
        self.surface.widgets.append(self.Logo)


class NewStoryCreationScreen:
    def __init__(self, language_data, xoy, textures, genres):
        self.screen_width = xoy[0] * 2
        self.screen_height = xoy[1] * 2
        self.genre_options = genres
        left_column_horizontal_position = self.screen_width * 0.05
        right_column_horizontal_position = self.screen_width * 0.4
        self.title = W.Label(text="Новая история",
                             xoy=(left_column_horizontal_position, self.screen_height * 0.1),
                             size=80, color=(0, 0, 0), centric=False)
        self.genre_label = W.Label(text="Жанр",
                                   xoy=(left_column_horizontal_position, self.screen_height * 0.2),
                                   size=50, color=(0, 0, 0), centric=False)
        self.genre_dropdown = W.DropDown(
            images=textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"],
            texts=self.genre_options, xoy=(right_column_horizontal_position, self.screen_height * 0.2 + 60))
        actors_vertical_position = self.screen_height * 0.3
        self.actors_label = W.Label(text="Действующие лица",
                                    xoy=(left_column_horizontal_position, actors_vertical_position),
                                    size=50, color=(0, 0, 0), centric=False)
        self.actors_field = W.InteractLabel(text=[''],
                                            xoy=(left_column_horizontal_position + 610, xoy[1] - 100),
                                            images=[textures.post_render(textures.dialogLabel, (205 * 6, 20 * 6))] * 2,
                                            active=True,
                                            size=50)
        self.description_label = W.Label(text="Описание или вступление:",
                                         xoy=(left_column_horizontal_position, self.screen_height * 0.47),
                                         size=50, color=(0, 0, 0), centric=False)
        self.description_field = W.InteractLabel(text=[''],
                                                 xoy=(left_column_horizontal_position + 610, xoy[1] + xoy[1] // 2),
                                                 images=[textures.dialogLabel, textures.dialogLabel],
                                                 active=True,
                                                 size=50)
        img = textures.buttonStep[0].get_rect()
        self.proceedButton = W.Button(textures.buttonStepNext, (xoy[0] * 2 - 10 * textures.resizer - img[2] / 2,
                                                            xoy[1] * 2 - 10 * textures.resizer - img[3] / 2))
        self.ReturnToMenuButton = W.Button(textures.EBack,
                                           (10 * textures.resizer + img[2] / 2, 5 * textures.resizer + img[3]))
        self.elements = [self.title, self.genre_label, self.actors_label, self.description_label,
                         self.description_field, self.actors_field, self.genre_dropdown, self.proceedButton,
                         self.ReturnToMenuButton]
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
            self.texture = self.textures.post_render(self.texture, (
                self.texture.get_rect()[2] * self.scale, self.texture.get_rect()[3] * self.scale))

    def __init__(self, language_data, xoy, textures, dialogue_data, story_name=None):
        self.elements = []
        self.xoy = xoy
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
        self.elements.append(W.InteractLabel(text=[self.dialog], xoy=(
            xoy[0] * 2 - img[2] // 2 - 20 * textures.resizer, xoy[1] * 2 - img[3] // 2 - 20 * textures.resizer),
                                             images=[textures.dialogLabel, textures.dialogLabel], active=False,
                                             size=30))
        character_position = (
            xoy[0] * 2 - xoy[0] * 2 * 0.01, xoy[1] * 2 - img[3] // 2 - 20 * textures.resizer - img[3] // 2)
        for character in self.character_names:
            character_obj = DialogueUI.Character(name=character, position=character_position, dialogue=self,
                                                 scale=0.25).set_position_for_right_bottom_corner(character_position)
            self.elements.append(character_obj.widget())
            character_position = character_position[0] - character_obj.size, character_position[1]
        img = textures.buttonStep[0].get_rect()
        self.ButtonNextStep = W.Button(textures.buttonStepNext, (
            xoy[0] * 2 - 10 * textures.resizer - img[2] / 2, 10 * textures.resizer + img[3] / 2))
        self.ButtonBackStep = W.Button(textures.buttonStep,
                                       (10 * textures.resizer + img[2] / 2, 10 * textures.resizer + img[3] / 2))
        self.ReturnToMenu = W.Button(textures.EBack,
                                     (10 * textures.resizer + img[2] / 2, 10 * textures.resizer + img[3] * 1.6))
        self.surface = W.Surface(*self.elements, self.ButtonNextStep, self.ButtonBackStep, self.ReturnToMenu)

    def updateDialog(self, dialogue_data):
        self.character_names = dialogue_data.get("Characters_names")
        self.location = dialogue_data.get("Location")
        self.main_character = dialogue_data.get("Main_character")
        self.dialog = dialogue_data.get("Dialog")
        self.surface.widgets[0].image = self.textures.locations[self.location][0]
        self.surface.widgets[2].text = self.surface.widgets[2].wrap_text([self.dialog])
        self.surface.widgets[1].image = self.textures.post_render(self.textures.characters[self.main_character][0], (
            self.elements[1].image.get_rect()[2], self.elements[1].image.get_rect()[3]))
        for i, character in enumerate(self.surface.widgets[3:-3]):
            character.image = self.textures.post_render(self.textures.characters[self.character_names[i]][0],
                                                        (character.image.get_rect()[2], character.image.get_rect()[3]))
