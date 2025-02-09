from Engine.Objects.UI.Widgets import *


class Test:  # Специально для Богданчика пример с интерфейсом
    def __init__(self, language_data, xoy, textures):
        xoy = (xoy[0], xoy[1] + 100)
        self.hello = Label("Hello Team 1 :))", xoy, 80, (48, 35, 22))
        self.image = Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))
        self.surface = Surface(self.image, self.hello)
