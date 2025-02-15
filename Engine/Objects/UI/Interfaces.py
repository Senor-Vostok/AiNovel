from Engine.Objects.UI.Widgets import *
from Engine.Texture.Textures import screen
import random


class Test:  # Специально для Богданчика пример с интерфейсом
    def __init__(self, language_data, xoy, textures):
        self.hello = Label("Hello Team 1 :))", (xoy[0], xoy[1] + 100), 80, (255, 255, 255))
        self.image = Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))
        self.figure = Figure([xoy[0], xoy[1] - 100], (48, 35, 22, 255),
                             form=[[100, 30], [30, 100], [100, 100], [30, 30], [100, 30]], thickness=2,
                             color_bord=(252, 0, 0, 255))
        self.circle = Circle([xoy[0], xoy[1] + 200], (48, 35, 22, 255), radius=100, thickness=2,
                             color_bord=(252, 0, 0, 0))
        self.dropdown = DropDown(textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"], (xoy[0], xoy[1] + 200), ("1", "2", "3", "4", "5"))
        self.background = Image(textures.locations["InsideTheCircusTent"][0], xoy)
        self.surface = Surface(self.background, self.image, self.hello, self.figure, self.dropdown)

class Entry:
    def __init__(self, text: str, function = None):
        self.text = text
        self.function = function

class MainMenu:
    def __init__(self, language_data, xoy, size, textures):
        self.entries = [Entry("story 1")]
        self.surface = Surface()
        self.base_widget_kit = []
        self.screen_height = size[0]
        self.screen_width = size[1]
        self.button_state_color = (48, 35, 22, 0)
        self.button_trigger_color = (48, 35, 22, 255)
        self.horizontal_screen_center = xoy[0]
        self.update_displayed_entries()


    def update_displayed_entries(self):
        self.surface.widgets = self.base_widget_kit
        cell_height = self.cell_height()
        vertical_postiion = self.screen_height - cell_height * 2
        horizontal_position = self.screen_width // 2
        for entry in self.entries:
            entry_button = Button(xoy=(horizontal_position, vertical_postiion),
                                    images=[self.create_button_figure((horizontal_position, vertical_postiion), entry.text, self.button_state_color).surface,
                                            self.create_button_figure((horizontal_position, vertical_postiion), entry.text, self.button_trigger_color).surface],
                                    text=entry.text)
            if entry.function is not None:
                entry_button.connect(entry.function)
            self.surface.widgets.append(entry_button)
            print(self.surface.widgets[-1])
            
            vertical_postiion += cell_height * 2

    def cell_height(self) -> int:
        amount_of_entries = len(self.entries)
        amount_of_cells = amount_of_entries * 2 + amount_of_entries + 1
        return self.screen_height // amount_of_cells

    def create_button_figure(self, position, button_text:str, color:tuple[int, int, int, int], max_height = None) -> Figure:
        if max_height is None:
            max_height = self.cell_height()
        max_vertical_distance = max_height  // 2
        max_horizontal_distance = max_height * len(button_text)

        vertical_distance = lambda: random.randint(int(max_vertical_distance - 0.1 * max_vertical_distance), max_vertical_distance)

        horizontal_distance = lambda: random.randint(int(max_horizontal_distance - 0.1 * max_horizontal_distance), max_horizontal_distance)

        bottom_left = [-vertical_distance(), -horizontal_distance()]

        top_left = [vertical_distance(), -horizontal_distance()]

        top_right = [horizontal_distance(), vertical_distance()]

        bottom_right = [horizontal_distance(), -vertical_distance()]

        return Figure(xoy=position,
                      color=color,
                      form=[bottom_left, top_left, top_right, bottom_right],
                      thickness=2)