from Engine.Objects.UI import Interfaces


def show_UI(self, centre):
    # self.interfaces['test'] = Interfaces.Test(None, centre, size, self.textures)
    self.interfaces['main_menu'] = Interfaces.MainMenu(None, centre, self.textures)
