from Engine.Objects.UI.Widgets import *


class Test:  # Специально для Богданчика пример с интерфейсом
    def __init__(self, language_data, xoy, textures):
        self.hello = Label("Hello Team 1 :))", (xoy[0], xoy[1] + 100), 80, (48, 35, 22))
        self.image = Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 100))
        self.background = Image(textures.locations["NightStripteaseClub"][0], xoy)
        self.surface = Surface(self.background, self.image, self.hello)
