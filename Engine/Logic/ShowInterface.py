from Engine.Objects.UI import Interfaces
from Engine.Objects.UI import Widgets

def show_UI(handler, centre):
    # handler.interfaces['test'] = Interfaces.Test(None, centre, handler.textures)
    Entry = Widgets.Entry
    # handler.interfaces['main_menu'] = Interfaces.MainMenu(None, centre, handler.textures,
    #                                                       entries=[Entry("story 1"),
    #                                                             Entry("story 2"),
    #                                                             Entry("story 3"),
    #                                                             Entry("Story 4"),
    #                                                             Entry("Story 5"),
    #                                                             Entry("Story 6"),
    #                                                             Entry("Story 7"),
    #                                                             Entry("Story 8"),
    #                                                             Entry("Story 9"),
    #                                                             Entry("Story 10")])

    handler.interfaces['new_story_creation_screen'] = Interfaces.NewStoryCreationScreen(None, centre, handler.textures)