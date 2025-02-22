from Engine.Objects.UI.Widgets import *
import random


class Test:
    def __init__(self, language_data, xoy, textures):
        self.hello = Label("Hello Team 1 :))", (xoy[0], xoy[1] + 100), 80, (255, 255, 255))
        self.image = Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))
        self.figure = Figure([xoy[0], xoy[1] - 100], (48, 35, 22, 255),
                             form=[[100, 30], [30, 100], [100, 100], [30, 30], [100, 30]])
        self.circle = Circle([xoy[0], xoy[1] + 200], (48, 35, 22, 255), radius=100, thickness=2, color_bord=(252, 0, 0, 0))
        self.dropdown = DropDown(textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"], (xoy[0], xoy[1] + 200), ("1", "2", "3", "4", "5"))
        self.background = Image(textures.locations["InsideTheCircusTent"][0], xoy)
        self.surface = Surface(self.background, self.image, self.hello, self.figure, self.dropdown)


class Entry:
    def __init__(self, text: str, function=None):
        self.text = text
        self.function = function


class MainMenu:
    def __init__(self, language_data, xoy, textures, saves_story):
        self.entries = [Entry(story["name"], story["launch"]) for story in saves_story]
        self.textures = textures
        self.entries.append(Entry("Новая история"))
        self.surface = Surface()
        self.base_widget_kit = []
        self.screen_height = xoy[1] * 2
        self.screen_width = xoy[0] * 2
        self.button_state_color = (0, 0, 0, 0)
        self.button_trigger_color = (196, 73, 0, 255)

        # Константы заполнения интерфейса
        self.VERTICAL_PERCENT_FILLING = 0.5
        self.HORIZONTAL_PERCENT_FILLING = 0.5

        image = self.textures.characters[random.choice(list(self.textures.characters.keys()))][0]
        self.textures.post_render(image, (image.get_rect()[2] * 0.7, image.get_rect()[3] * 0.7))
        xoy_image = (image.get_rect()[2] / 2 + 10 * self.textures.resizer, self.screen_height - image.get_rect()[3] / 2 -  + 10 * self.textures.resizer)
        self.base_widget_kit.append(Image(image, xoy_image))
        self.update_displayed_entries()

    def update_displayed_entries(self):
        self.surface.widgets = self.base_widget_kit
        cell_height = self.cell_height()
        vertical_position = (self.screen_height * (1 - self.VERTICAL_PERCENT_FILLING)) / 2  + cell_height * 2
        horizontal_position = self.screen_width // 2
        for entry in self.entries:
            button_trigger_figure, button_state_figure = self.create_button_figures((horizontal_position, vertical_position), entry.text, self.button_trigger_color, max_height=cell_height * 2)
            entry_button = Button(xoy=(horizontal_position, vertical_position), images=[button_state_figure.surface, button_trigger_figure.surface], text=entry.text)
            entry_button.connect(entry.function)
            self.surface.widgets.append(entry_button)
            vertical_position += cell_height * 3

    def cell_height(self) -> int:
        amount_of_entries = len(self.entries)
        amount_of_cells = amount_of_entries * 2 + amount_of_entries + 1
        return int((self.screen_height * self.VERTICAL_PERCENT_FILLING) // amount_of_cells)

    def create_button_figures(self, position, button_text: str, color: tuple[...], max_height: int) -> tuple[Figure, Figure]:
        max_height = self.cell_height() if not max_height else max_height
        max_vertical_distance = max_height // 2
        horizontal_safe_zone_size = int(self.screen_width - (0.1 * self.screen_width)) // 2
        # Создание псевдо текста и его длины
        font = pygame.font.Font("19363.ttf", max_height - max_height // 3)
        LabelText = font.render(button_text, 1, (0, 0, 0)).get_rect()[2]
        #
        max_horizontal_distance = min(LabelText, horizontal_safe_zone_size)
        vertical_distance = lambda: random.randint(int(max_vertical_distance - (0.1 * max_vertical_distance)),
                                                   max_vertical_distance)
        horizontal_distance = lambda: random.randint(int(max_horizontal_distance - (0.1 * max_horizontal_distance)),
                                                     max_horizontal_distance)
        bottom_left = [-horizontal_distance(), -vertical_distance()]
        top_left = [-horizontal_distance(), vertical_distance()]
        top_right = [horizontal_distance(), vertical_distance()]
        bottom_right = [horizontal_distance(), -vertical_distance()]
        return Figure(xoy=position,
                      color=color,
                      form=[top_left, top_right, bottom_right, bottom_left]), \
               Figure(xoy=position,
                      color=(0, 0, 0, 0),
                      form=[top_left, top_right, bottom_right, bottom_left])
