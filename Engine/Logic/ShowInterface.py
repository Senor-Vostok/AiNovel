from Engine.Objects.UI import Interfaces
from Engine.Objects.UI import Widgets


def showMainMenu(handler, centre):
    handler.interfaces['mainMenu'] = Interfaces.MainMenu(None, centre, handler.textures, handler.saves_story)
