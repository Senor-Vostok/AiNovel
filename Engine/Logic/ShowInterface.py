from Engine.Objects.UI import Interfaces


def showDialog(handler, centre):
    test_cue = {
        "Characters_names": [_ for _ in handler.story['characters_name'] if _ != handler.story['dialogues'][handler.dialog][0]],
        "Location": handler.story['location'],
        "Main_character": handler.story['dialogues'][handler.dialog][0],
        "Dialog": handler.story['dialogues'][handler.dialog][1]}
    handler.interfaces['dialog'] = Interfaces.DialogueUI(None, centre, handler.textures, test_cue)
    handler.interfaces['dialog'].ReturnToMenu.connect(lambda: showMainMenu(handler, centre))
    handler.interfaces['dialog'].ButtonNextStep.connect(lambda: handler.step(1))
    handler.interfaces['dialog'].ButtonBackStep.connect(lambda: handler.step(-1))


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


def showNewStoryCreation(handler, centre):
    handler.interfaces = dict()
    handler.interfaces['create'] = Interfaces.NewStoryCreationScreen(None, centre, handler.textures, ["Детектив", "Романтика", "Боевик"])
    handler.interfaces['create'].ReturnToMenuButton.connect(lambda: showMainMenu(handler, centre))
    a = handler.interfaces['create']
    a.proceedButton.connect(lambda: handler.startStory({"genre": a.genre_dropdown.selected_text.text[0],
                                                        "persons": ', '.join(a.actors_field.text),
                                                        "entry": ' '.join(a.description_field.text)}))


def showSettings(handler, centre):
    if len(handler.interfaces) > 1: handler.interfaces.pop([_ for _ in handler.interfaces if handler.interfaces[_] == handler.last_interface][0])
    handler.interfaces['settings'] = Interfaces.Settings(None, centre, handler.textures)
    handler.interfaces['settings'].VolumeSetting.connect(lambda: handler.change_volume(handler.interfaces['settings'].VolumeSetting))

