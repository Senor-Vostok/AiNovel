# from Engine.Objects.UI.Widgets import *
from Engine.Objects.UI import Widgets as W
import random
screen_width = None
screen_height = None

def set_screen_size(xoy):
    global screen_width
    global screen_height
    screen_width = xoy[0] * 2
    screen_height = xoy[1] * 2

class Test:
    def __init__(self, language_data, xoy, textures):
        self.hello = W.Label("Hello Team 1 :))", (xoy[0], xoy[1] + 100), 80, (255, 255, 255))

        self.image = W.Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))

        self.figure = W.Figure([xoy[0], xoy[1] - 100], (48, 35, 22, 255),
                             form=[[100, 30], [30, 100], [100, 100], [30, 30], [100, 30]], thickness=2,
                             color_bord=(252, 0, 0, 255))

        self.circle = W.Circle([xoy[0], xoy[1] + 200], (48, 35, 22, 255), radius=100, thickness=2,
                             color_bord=(252, 0, 0, 0))

        self.dropdown = W.DropDown(textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"], (xoy[0], xoy[1] + 200), ("1", "2", "3", "4", "5"))
        self.background = W.Image(textures.locations["InsideTheCircusTent"][0], xoy)
        self.surface = W.Surface(self.background, self.image, self.hello, self.figure, self.dropdown)


class MainMenu:
    def __init__(self, language_data, xoy, textures, entries):
        global screen_width
        global screen_height

        set_screen_size(xoy)

        #example entries
        if entries is not None:
            self.entries = entries
        else:
            self.entries = [W.Entry("story 1"),
                            W.Entry("story 2"),
                            W.Entry("story 3"),
                            W.Entry("Story 4"),
                            W.Entry("Story 5"),
                            W.Entry("Story 6"),
                            W.Entry("Story 7"),
                            W.Entry("Story 8"),
                            W.Entry("Story 9"),
                            W.Entry("Story 10")]
            # handler.entries = [W.Entry("story 1"),
            #                 W.Entry("story 2"),
            #                 W.Entry("story 3")]

        self.surface = W.Surface()
        self.base_widget_kit = []


        print(f"Screen Dimensions: {screen_width}×{screen_height}")

        # цвета будут определяться с помощью цвета фона, фоны при наведении — меняться, поэтому для каждой кнопки свой цвет обводки
        self.button_state_color = (48, 35, 22, 0)
        self.button_trigger_color = (48, 35, 22, 255)

        self.update_displayed_entries()


    def update_displayed_entries(self):
        print("amount of entries: ", len(self.entries))
        self.surface.widgets = self.base_widget_kit
        cell_height = self.cell_height()
        print("Cell height: ", cell_height)
        vertical_postiion = 0 + cell_height * 2
        horizontal_position = screen_width // 2
        for entry in self.entries:
            print(vertical_postiion)

            button_trigger_figure, button_state_figure = \
                  self.create_button_figures((horizontal_position, vertical_postiion),
                                              entry.text,
                                              self.button_trigger_color,
                                              max_height=cell_height * 2)

            entry_button = W.Button(xoy=(horizontal_position, vertical_postiion),
                                  images=[button_state_figure.surface, button_trigger_figure.surface],
                                  text=entry.text)

            if entry.function is not None:
                entry_button.connect(entry.function)

            self.surface.widgets.append(entry_button)
            vertical_postiion += cell_height * 3


    def cell_height(self) -> int:
        global screen_height
        global screen_width
        amount_of_entries = len(self.entries)
        amount_of_cells = amount_of_entries * 2 + amount_of_entries + 1
        return screen_height // amount_of_cells


    def create_button_figures(self, position, button_text: str, color: tuple[int, int, int, int], max_height) -> tuple[W.Figure, W.Figure]:

        if max_height is None:
            max_height = self.cell_height()

        max_vertical_distance = max_height // 2
        horizontal_safe_zone_size = int(screen_width - (0.1 * screen_width)) // 2
        max_horizontal_distance = min(max_height * len(button_text), horizontal_safe_zone_size)

        vertical_distance = lambda: random.randint(int(max_vertical_distance - (0.1 * max_vertical_distance)),
                                                   max_vertical_distance)
        horizontal_distance = lambda: random.randint(int(max_horizontal_distance - (0.1 * max_horizontal_distance)),
                                                     max_horizontal_distance)

        bottom_left = [-horizontal_distance(), -vertical_distance()]
        top_left = [-horizontal_distance(), vertical_distance()]
        top_right = [horizontal_distance(), vertical_distance()]
        bottom_right = [horizontal_distance(), -vertical_distance()]

        return W.Figure(xoy=position,
                      color=color,
                      form=[top_left, top_right, bottom_right, bottom_left],
                      thickness=2), \
               W.Figure(xoy=position,
                      color=(0, 0, 0, 0,),
                      form=[top_left, top_right, bottom_right, bottom_left],
                      thickness=2)

class NewStoryCreationScreen:
    def __init__(self, language_data, xoy, textures):
        global screen_height
        global screen_width
        set_screen_size(xoy)
        print(screen_width)
        print(xoy[0])
        left_column_horizontal_position = screen_width * 0.1
        print(left_column_horizontal_position)

        self.title = W.Label(text="Новая история",
                             xoy=(left_column_horizontal_position, screen_height * 0.1),
                             pp=80, color=(0, 0, 0), centric=False)

        self.genre_label = W.Label(text="Жанр",
                                   xoy=(left_column_horizontal_position, screen_height * 0.2),
                                   pp=80, color=(0, 0, 0), centric=False)

        self.actors_label = W.Label(text="Действующие лица",
                                    xoy=(left_column_horizontal_position, screen_height * 0.3),
                                    pp=80, color=(0, 0, 0), centric=False)

        self.desctiption_label = W.Label(text="Описание или вступление:",
                                         xoy=(left_column_horizontal_position, screen_height * 0.45),
                                         pp=80, color=(0, 0, 0), centric=False)


        description_field_position = (xoy[0], screen_height * 0.7)
        description_field_height = screen_height * 0.3

        top_left = (-(xoy[0] - left_column_horizontal_position),
                    description_field_height // 2)

        top_right = ((xoy[0] - left_column_horizontal_position),
                     description_field_height // 2)

        bottom_right = ((xoy[0] - left_column_horizontal_position),
                        -(description_field_height // 2))

        bottom_left = (-(xoy[0] - left_column_horizontal_position),
                       -(description_field_height // 2))


        self.description_field_figure = W.Figure(xoy=description_field_position,
                                                 color=(255,255,255),
                                                 color_bord=(0, 0, 0, 255),
                                                 form=[top_left, top_right, bottom_right, bottom_left],
                                                 thickness=2)

        self.elements = [self.title, self.genre_label, self.actors_label, self.desctiption_label, self.description_field_figure]

        self.surface = W.Surface(*self.elements)