from Engine.Objects.UI import Interfaces


def showDialog(handler, centre):
    # handler.interfaces['main_menu'] = Interfaces.MainMenu(None, centre, handler.textures, handler.saves_story)
    # handler.interfaces['new_story'] = Interfaces.NewStoryCreationScreen(None, centre, handler.textures)
    test_cue = {
        "Characters_names": ["character1", "character2", "character3", "character4", "character5"],
        "Location": "AutumnCity",
        "Main_character": "character10",
        "Dialog": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
    }
    handler.interfaces['dialog'] = Interfaces.DialogueUI(None, centre, handler.textures, test_cue)
    handler.interfaces['dialog'].ReturnToMenu.connect(lambda: showMainMenu(handler, centre))


def showMainMenu(handler, centre):
    handler.interfaces = dict()
    handler.interfaces['mainMenu'] = Interfaces.MainMenu(None, centre, handler.textures, handler.saves_story, handler.createNewStory, handler.quit)
    handler.interfaces['mainMenu'].Custom.connect(lambda: showChoicePrefab(handler, centre))
    handler.interfaces['mainMenu'].Settings.connect(lambda: showSettings(handler, centre))


def showChoicePrefab(handler, centre):
    if len(handler.interfaces) > 1: handler.interfaces.pop([_ for _ in handler.interfaces if handler.interfaces[_] == handler.last_interface][0])
    handler.interfaces['choicePrefab'] = Interfaces.ChoicePrefab(None, centre, handler.textures)
    handler.interfaces['choicePrefab'].character.connect(lambda: handler.choose_asset("character"))
    handler.interfaces['choicePrefab'].location.connect(lambda: handler.choose_asset("location"))


def showSettings(handler, centre):
    if len(handler.interfaces) > 1: handler.interfaces.pop([_ for _ in handler.interfaces if handler.interfaces[_] == handler.last_interface][0])
    handler.interfaces['settings'] = Interfaces.Settings(None, centre, handler.textures)
    handler.interfaces['settings'].VolumeSetting.connect(lambda: handler.change_volume(handler.interfaces['settings'].VolumeSetting))

