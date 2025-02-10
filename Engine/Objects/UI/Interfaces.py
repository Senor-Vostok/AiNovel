from Engine.Objects.UI.Widgets import *


class Test:  # Специально для Богданчика пример с интерфейсом
    def __init__(self, language_data, xoy, textures):
        xoy = (xoy[0], xoy[1] + 100)
        self.hello = Label("Hello Team 1 :))", xoy, 80, (48, 35, 22))
        self.image = Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))
        self.figure = Figure([xoy[0], xoy[1] - 100], (48, 35, 22, 255),
                             form=[[100, 30], [30, 100], [100, 100], [30, 30], [100, 30]], thickness=2,
                             color_bord=(252, 0, 0, 255))
        self.circle = Circle([xoy[0], xoy[1] + 200], (48, 35, 22, 255), radius=100, thickness=2,
                             color_bord=(252, 0, 0, 0))
        self.dropdown = DropDown(textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"], xoy, ("1", "2", "3", "4", "5"))
        self.surface = Surface(self.image, self.hello, self.figure, self.dropdown)
