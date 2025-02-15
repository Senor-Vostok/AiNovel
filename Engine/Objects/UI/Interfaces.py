from Engine.Objects.UI.Widgets import *
import random


class Test:
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
    def __init__(self, text: str, function=None):
        self.text = text
        self.function = function


class MainMenu:
    def __init__(self, language_data, xoy, textures):
        self.entries = [Entry("story 1"), Entry("story 2")]
        self.surface = Surface()
        self.base_widget_kit = []
        self.screen_height = xoy[1] * 2
        self.screen_width = xoy[0] * 2
        self.button_state_color = (48, 35, 22, 0)
        self.button_trigger_color = (48, 35, 22, 255)
        self.update_displayed_entries()

    def update_displayed_entries(self):
        self.surface.widgets = self.base_widget_kit
        cell_height = self.cell_height()
        vertical_postiion = self.screen_height // 2 - cell_height
        horizontal_position = self.screen_width // 2
        for entry in self.entries:
            # button_trigger_figure = self.create_button_figures((horizontal_position, vertical_postiion), entry.text, self.button_trigger_color, cell_height)
            button_trigger_figure, button_state_figure = self.create_button_figures((horizontal_position, vertical_postiion), entry.text, self.button_trigger_color, cell_height)
            print(button_state_figure.color)
            entry_button = Button(xoy=(horizontal_position, vertical_postiion), images=[button_state_figure.surface, button_trigger_figure.surface], text=entry.text)
            if entry.function is not None:
                entry_button.connect(entry.function)
            self.surface.widgets.append(entry_button)
            print(self.surface.widgets[-1])
            vertical_postiion += cell_height * 2

    def cell_height(self) -> int:
        amount_of_entries = len(self.entries)
        amount_of_cells = amount_of_entries * 2 + amount_of_entries + 1
        print(self.screen_height)
        return self.screen_height // amount_of_cells

    def create_button_figures(self, position, button_text: str, color: tuple[int, int, int, int], max_height: int) -> tuple[Figure, Figure]:
        if max_height is None:
            max_height = self.cell_height()
        print(max_height)
        max_vertical_distance = max_height // 2
        horizontal_figure_limit = int(self.screen_width - (0.1 * self.screen_width)) // 2
        max_horizontal_distance = min(max_height * len(button_text), horizontal_figure_limit)
        vertical_distance = lambda: random.randint(int(max_vertical_distance - (0.1 * max_vertical_distance)),
                                                   max_vertical_distance)
        horizontal_distance = lambda: random.randint(int(max_horizontal_distance - (0.1 * max_horizontal_distance)),
                                                     max_horizontal_distance)
        bottom_left = [-horizontal_distance(), -vertical_distance()]
        top_left = [-horizontal_distance(), vertical_distance()]
        top_right = [horizontal_distance(), vertical_distance()]
        bottom_right = [horizontal_distance(), -vertical_distance()]
        print(bottom_left, top_left, top_right, bottom_right)
        print("potition", position)
        return Figure(xoy=position,
                      color=color,
                      form=[top_left, top_right, bottom_right, bottom_left],
                      thickness=2), \
            Figure(xoy=position,
                   color=(0, 0, 0, 0,),
                   form=[top_left, top_right, bottom_right, bottom_left],
                   thickness=2)
