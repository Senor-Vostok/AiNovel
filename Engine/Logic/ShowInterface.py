from Engine.Objects.UI import Interfaces
from Engine.Objects.UI import Widgets


def show_UI(handler, centre):
    # handler.interfaces['main_menu'] = Interfaces.MainMenu(None, centre, handler.textures, handler.saves_story)
    # handler.interfaces['new_story'] = Interfaces.NewStoryCreationScreen(None, centre, handler.textures)
    test_cue = {
        "Characters_names": ["character1", "character2", "character3", "character4", "character5"],
        "Location": "AutumnCity",
        "Main_character": "character10",
        "Dialog": "bblah blah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blahblah blah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blahblah blah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blahblah blah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blahblah blah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blahlah blah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah blahblah blah"
    }
    handler.interfaces['dialogue_ui'] = Interfaces.DialogueUI(None, centre, handler.textures, test_cue)