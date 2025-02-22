from Engine.Objects.UI import Interfaces


def show_UI(handler, centre):
    handler.interfaces['main_menu'] = Interfaces.MainMenu(None, centre, handler.textures, handler.saves_story)
