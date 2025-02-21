from Engine.Objects.UI.Widgets import *


class Test:  # Специально для Богданчика пример с интерфейсом
    def __init__(self, language_data, xoy, textures):
        self.hello = Label("Hello Team 1 :))", (xoy[0], xoy[1] + 100), 80, (255, 255, 255))
        self.image = Image(textures.characters["character19"][0], (xoy[0], xoy[1] - 200))
        self.figure = Figure([xoy[0], xoy[1] - 100], (48, 35, 22, 255),
                             form=[[100, 30], [30, 100], [100, 100], [30, 30], [100, 30]], thickness=2,
                             color_bord=(252, 0, 0, 255))
        self.circle = Circle([xoy[0], xoy[1] + 200], (48, 35, 22, 255), radius=100, thickness=2,
                             color_bord=(252, 0, 0, 0))
        self.label = InteractLabel(images=[pygame.image.load('C:/Users/alber/Downloads/Board.png'),
                                          pygame.image.load('C:/Users/alber/Downloads/Board1.png')], xoy=xoy)
        self.label_norm = Label('jsddjskdjakdjkajdsdfsdfds\nfdsfsdfsdfdsfdk', xoy=xoy, pp=50)
        self.surface = Surface(self.label)

        self.dropdown = DropDown(textures.DropDown["selected"] + textures.DropDown["arrow"] + textures.DropDown["variant"], (xoy[0], xoy[1] + 200), ("1", "2", "3", "4", "5"))
        self.background = Image(textures.locations["InsideTheCircusTent"][0], xoy)
        self.surface = Surface(self.label_norm)