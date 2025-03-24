import random
import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame.display
from Engine.Texture.Textures import Textures
from Engine.Sound.Sounds import Sounds
from Engine.Logic.Machine import Scene
from Engine.Objects.MainCamera import MainCamera
from Engine.Logic.AI import OpenAIWrapper
from win32api import GetSystemMetrics
from Engine.Constants import *
from Engine.Visual.Render import Render
from Engine.Logic.ShowInterface import *


class EventHandler:
    def __init__(self):
        pygame.mixer.init()
        pygame.display.set_caption('Test')
        # handler.settings = dict()
        self.volumes_channels = [1] * 8
        # handler.language_data = dict()
        # handler.export_language(handler.settings['language'])
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.center = (self.size[0] // 2, self.size[1] // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.textures = Textures()
        self.screen.blit(self.textures.loading, (self.center[0] - self.textures.loading.get_rect()[2] // 2,
                                                 self.center[1] - self.textures.loading.get_rect()[3] // 2))
        pygame.display.flip()
        self.textures.init_textures()
        self.sounds = Sounds()
        pygame.mixer.Channel(0).play(random.choice(self.sounds.menu), -1)
        pygame.mixer.Channel(0).set_volume(0.2)
        self.timer, self.timer_backmusic, self.last_interface = None, None, None
        self.logic = Scene(self)
        self.open_some, self.flag = True, True
        self.interfaces = dict()
        self.effects = list()  # Хранит объекты класса Effects
        self.camera = MainCamera()
        self.render = Render(self)
        self.saves_story = []
        showMainMenu(self, self.center)
        self.ai = OpenAIWrapper("")
        if self.ai.tryCreateClient():
            print("SUCCES")
        self.story = dict()
        self.now_story = str
        self.dialog = 0

    def step(self, step=1):
        if self.dialog + step == -1:
            return
        elif self.dialog + step == len(self.story['dialogues']):
            self.story, self.now_story = self.continue_story(self.values)
            print(self.story, self.now_story)
            self.dialog = -1
        self.dialog += step
        self.interfaces["dialog"].updateDialog({
            "Characters_names": [_ for _ in self.story['characters_name'] if
                                 _ != self.story['dialogues'][self.dialog][0]],
            "Location": self.story['location'],
            "Main_character": self.story['dialogues'][self.dialog][0],
            "Dialog": self.story['dialogues'][self.dialog][1]})

    def change_volume(self, slicer, channel=0):
        self.volumes_channels[channel] = slicer.now_sector / slicer.cuts  # Проценты
        pygame.mixer.Channel(channel).set_volume(self.volumes_channels[channel])

    def createNewStory(self):
        showNewStoryCreation(self, self.center)

    def startStory(self, values):
        try:
            self.story, self.now_story = self.get_story(values)
            pygame.mixer.Channel(0).play(random.choice(self.sounds.musics), -1)
            self.interfaces.clear()
            showDialog(self, self.center)
        except Exception:
            pass

    def changeApiKey(self, api_key):
        self.ai.updateAPIKEY(api_key)

    def click_handler(self):
        command = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.KEYDOWN:
                command = i
                if i.key == pygame.K_ESCAPE:
                    if len(self.interfaces) > 1:
                        self.interfaces.pop(
                            [_ for _ in self.interfaces if self.interfaces[_] == self.last_interface][0])
            if i.type == pygame.QUIT:
                self.quit()
        return command

    def continue_story(self, values):
        locations = self.textures.locations.keys()
        s = f"""История для визуальной новеллы на русском не меняй шаблон и подписывай говорящих в диалоге, свою историю составь только из диалогов персонажей, без 
                        описания чего-либо происходящего между ними. Диалоги сделай достаточно длинными и информативными, старайся редко использовать 
                        короткие эмоциональные предложения. Не забывай, что в описании диалога, ты должен использовать 
                        кодовое имя персонажа в формате "chatacterX: dialog", без указания настоящего имени говорящего(НИГДЕ, КРОМЕ САМОГО ДИАЛОГА ИМЯ НЕ ДОЛЖНО УПОМЯНАТЬСЯ). И делай диалоги 
                        подлиннее. В ответе между строками НЕ СОТАВЛЯЙ ПУСТЫЕ МЕСТА, только текст без каких либо "украшений". В Characters_names только те персонажи которые действительно участвуют в диалогах И ТОЛЬКО ИХ КОДОВЫЕ ИМЕНА:
                        Твой ответ должен соответствовать данным паттернам r"\*\*Characters_names:\s*.*\n*\*\*Location:\s*.*\n*\*\*Main_character:\s*.*\n*\*\*Dialog:\s*.*\n*" и r"Characters_names:\s*.*\n*Location:\s*.*\n*Main_character:\s*.*\n*Dialog:\s*.*\n"
                        Жанр - {values["genre"]}
                        Characters_names: {', '.join(self.story['characters_name'])}
                        Location: {', '.join(locations)}
                        Main_character:
                        Dialog:"""
        s = f"""запомни, твой ответ должен быть ТОЧНО ТАКОЙ же: ```{self.now_story}``` тебе нужно лишь написать новые диалоги, как продолжение истории, если хочешь, можешь поменять Location из списка {', '.join(locations)}. Следуй памятке {s}"""
        original = self.ai.request_to_ai(s)
        response = [i for i in original.split("\n") if i]
        print(response)
        story = dict()
        if not (''.join((response[0].split())[1:])).split(','):
            response = response[1:-1]
        story["characters_name"] = (''.join((response[0].split())[1:])).split(',')
        story["location"] = response[1].split()[1]
        story["dialogues"] = [[i.split(": ")[0], ": ".join(i.split(": ")[1:])] for i in response[4:] if i]
        print(story)
        return story, original

    def get_story(self, values):
        self.values = values
        characters = self.textures.characters.keys()
        locations = self.textures.locations.keys()
        s = f"""Создай историю для визуальной новеллы на русском в соответствии с этим шаблоном, выбрав случайных персонажей, не давая им имен, и 
                локацию (не меняй шаблон и подписывай говорящих в диалоге), свою историю составь только из диалогов персонажей, без 
                описания чего-либо происходящего между ними. Во время диалога дай имена персонажам и держи их в уме, когда будешь 
                составлять диалоги между ними. Диалоги сделай достаточно длинными и информативными, старайся редко использовать 
                короткие эмоциональные предложения. Имена персонажей для диалога можешь выбрать из этого списка: 
                {values["persons"] if len(values["persons"]) > 0 else 'на твое усмотрение'}. Не забывай, что в описании диалога, ты должен использовать 
                кодовое имя персонажа в формате "chatacterX: dialog", без указания настоящего имени говорящего(НИГДЕ, КРОМЕ САМОГО ДИАЛОГА ИМЯ НЕ ДОЛЖНО УПОМЯНАТЬСЯ). И делай диалоги 
                подлиннее. В ответе между строками НЕ СОТАВЛЯЙ ПУСТЫЕ МЕСТА, только текст без каких либо "украшений"(```). В Characters_names только те персонажи которые действительно участвуют в диалогах И ТОЛЬКО ИХ КОДОВЫЕ ИМЕНА
                Жанр - {values["genre"]}, Предыстория или краткое начало, которые ты должен знать: {values["entry"]}:
                Characters_names: {', '.join(characters)}
                Location: {', '.join(locations)}
                Main_character:
                Dialog:"""
        original = self.ai.request_to_ai(s)
        response = [i for i in original.split("\n") if i]
        print(response)
        story = dict()
        if not (''.join((response[0].split())[1:])).split(','):
            response = response[1:-1]
        story["characters_name"] = (''.join((response[0].split())[1:])).split(',')
        story["location"] = response[1].split()[1]
        story["dialogues"] = [[i.split(": ")[0], ": ".join(i.split(": ")[1:])] for i in response[4:] if i]
        print(story)
        return story, original

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.clock.tick()
        self.render.rendering()

    def get_new_asset_name(self):
        asset_number = len(os.listdir("Assets/Characters")) + 1
        return f"Characters/character{asset_number}.png"

    def choose_asset(self, asset_type):
        root = tk.Tk()
        root.withdraw()
        file_path = tk.filedialog.askopenfilename(
            initialdir="/",
            title="Выберите файл",
            filetypes=[("PNG files", "*.png")])
        if file_path:
            if asset_type == "character":
                file_name = self.get_new_asset_name()
            elif asset_type == "location":
                file_name = "Locations/" + os.path.basename(file_path)
                if os.path.exists(f"Assets/{file_name}"):
                    messagebox.showerror("Добавление файла",
                                         f"Файл с названием {os.path.basename(file_path)} уже добавлен.")
                    return
            else:
                return

            shutil.copy(file_path, f"Assets/{file_name}")
        else:
            return

    def quit(self):
        sys.exit()
