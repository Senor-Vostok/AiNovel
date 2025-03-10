from Engine.Objects.UI import Interfaces
from Engine.Objects.UI import Widgets


def show_UI(handler, centre):
    handler.interfaces['main_menu'] = Interfaces.MainMenu(None, centre, handler.textures, handler.saves_story)
    # handler.interfaces['new_story'] = Interfaces.NewStoryCreationScreen(None, centre, handler.textures)
