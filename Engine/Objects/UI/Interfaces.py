from Engine.Objects.UI import Widgets as W
import pygame
import random
screen_width = None
screen_height = None


class MainMenu:
    def __init__(self, language_data, xoy, textures, saves_story):
        self.textures = textures
        self.screen_width = xoy[0] * 2
        self.screen_height = xoy[1] * 2
        self.entries = [W.Entry(story["name"], story["launch"]) for story in saves_story]
        self.entries.append(W.Entry("New story", None))
        self.surface = W.Surface()
        self.base_widget_kit = []
        self.button_state_color = (0, 0, 0, 0)
        self.button_trigger_color = (196, 73, 0, 255)

        print(f"Screen Dimensions: {screen_width}×{screen_height}")

        # Константы заполнения интерфейса
        self.VERTICAL_PERCENT_FILLING = 0.5
        self.HORIZONTAL_PERCENT_FILLING = 0.5

        image = self.textures.characters[random.choice(list(self.textures.characters.keys()))][0]
        image = self.textures.post_render(image, (image.get_rect()[2] * 0.7, image.get_rect()[3] * 0.7))
        xoy_image = (image.get_rect()[2] / 2 + 10 * self.textures.resizer, self.screen_height - image.get_rect()[3] / 2 - 10 * self.textures.resizer)
        self.base_widget_kit.append(W.Image(image, xoy_image))
        self.update_displayed_entries()

    def update_displayed_entries(self):
        self.surface.widgets = self.base_widget_kit
        cell_height = self.cell_height()
        print("Cell height: ", cell_height)
        vertical_position = (self.screen_height * (1 - self.VERTICAL_PERCENT_FILLING)) / 2 + cell_height * 2
        horizontal_position = self.screen_width // 2
        for entry in self.entries:
            print(vertical_position)
            button_trigger_figure, button_state_figure = self.create_button_figures((horizontal_position, vertical_position), entry.text, self.button_trigger_color, max_height=cell_height * 2)
            entry_button = W.Button(xoy=(horizontal_position, vertical_position), images=[button_state_figure.surface, button_trigger_figure.surface], text=entry.text)
            if entry.function is not None:
                entry_button.connect(entry.function)
            self.surface.widgets.append(entry_button)
            vertical_position += cell_height * 3

    def cell_height(self) -> int:
        global screen_height
        global screen_width
        amount_of_entries = len(self.entries)
        amount_of_cells = amount_of_entries * 2 + amount_of_entries + 1
        return int((self.screen_height * self.VERTICAL_PERCENT_FILLING) // amount_of_cells)

    def create_button_figures(self, position, button_text: str, color: tuple[...], max_height) -> tuple[W.Figure, W.Figure]:
        max_height = self.cell_height() if not max_height else max_height
        max_vertical_distance = max_height // 2
        horizontal_safe_zone_size = int(self.screen_width - (0.1 * self.screen_width)) // 2
        # Создание псевдо текста и его длины
        font = pygame.font.Font("19363.ttf", max_height - max_height // 3)
        LabelText = font.render(button_text, 1, (0, 0, 0)).get_rect()[2]
        #
        max_horizontal_distance = min(LabelText, horizontal_safe_zone_size)
        vertical_distance = lambda: random.randint(int(max_vertical_distance - (0.1 * max_vertical_distance)), max_vertical_distance)
        horizontal_distance = lambda: random.randint(int(max_horizontal_distance - (0.1 * max_horizontal_distance)), max_horizontal_distance)
        bottom_left = [-horizontal_distance(), -vertical_distance()]
        top_left = [-horizontal_distance(), vertical_distance()]
        top_right = [horizontal_distance(), vertical_distance()]
        bottom_right = [horizontal_distance(), -vertical_distance()]
        return W.Figure(xoy=position,
                        color=color,
                        form=[top_left, top_right, bottom_right, bottom_left]), \
               W.Figure(xoy=position,
                        color=(0, 0, 0, 0,),
                        form=[top_left, top_right, bottom_right, bottom_left])


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
                             pp=80, color=(0, 0, 0), centric=False)

        self.genre_label = W.Label(text="Жанр",
                                   xoy=(left_column_horizontal_position, self.screen_height * 0.2),
                                   pp=80, color=(0, 0, 0), centric=False)

        actors_vertical_position = self.screen_height * 0.3
        self.actors_label = W.Label(text="Действующие лица",
                                    xoy=(left_column_horizontal_position, actors_vertical_position),
                                    pp=80, color=(0, 0, 0), centric=False)

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
                                         pp=80, color=(0, 0, 0), centric=False)

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
                                                 color=(255,255,255),
                                                 color_bord=(0, 0, 0, 255),
                                                 form=[top_left, top_right, bottom_right, bottom_left],
                                                 thickness=2)

        self.elements = [self.title, self.genre_label, self.actors_label, self.desctiption_label, self.description_field_figure] + self.add_actors_plus_symbol

        self.surface = W.Surface(*self.elements)
