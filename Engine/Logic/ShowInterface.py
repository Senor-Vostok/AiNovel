from Engine.Objects.UI.Interfaces import *


def show_test(self, centre):
    test = Test(None, centre, self.textures)
    self.interfaces['test'] = test
