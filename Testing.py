import inspect
import random
import time
from typing import Any
from Engine.Launch.Handler import EventHandler
from Engine.Texture.Textures import Textures
from Engine.Objects.UI.Interfaces import *
from Engine.Logic.Machine import *
from Engine.Sound.Sounds import Sounds
from Engine.Objects.MainCamera import MainCamera
from Engine.Visual.Render import Render
from Engine.Visual.Efffect import *
from Engine.Objects.UI.Widgets import *

handler = EventHandler()
testImage = pygame.transform.scale(pygame.image.load("Assets/UI/DropDown/arrow.png"), (10, 10)).convert_alpha()


class TestWidget(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def draw(self, screen):
        pass

    def update(self, mouse_click, command):
        pass


def generate_random_arg(param: inspect.Parameter) -> Any:
    if param.annotation in (int, float) or param.name == "pp" or param.name == "cuts" or param.name == "now_sector" or param.name == "thickness" or param.name == "radius" or param.name == "speed" or param.name == "resizer":
        return random.uniform(1, 100) if param.annotation is float else random.randint(1, 100)
    elif param.annotation is str or param.name == "text" or param.name == "file":
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0987654321[] \/', k=random.randint(5, 10)))
    elif param.annotation is bool or param.name == "active" or param.name == "centric" or param.name == "recursive":
        return random.choice([True, False])
    elif param.annotation is list or param.name == "center":
        return [random.randint(-100, 100) for _ in range(5)]
    elif param.annotation is dict:
        return {str(i): i for i in range(5)}
    else:
        if param.name == "texture" or param.name == "image" or param.name == "back_image":
            return testImage
        elif param.name == "size" or param.name == "xoy" or param.name == "move":
            return 100, 100
        elif param.name == "address":
            return "Assets/Characters/character1.png"
        elif param.name == "images" or param.name == "animation":
            return [testImage] * 100
        elif param.name == "screen":
            return handler.screen
        elif param.name == "texts":
            return [''.join(random.choices('abcdefghijklmnopqrstuvwxyz0987654321[] \/', k=5))] * 5
        elif param.name == "mouse_click":
            return handler.camera.mouse_click
        elif param.name == "command":
            return handler.click_handler()
        elif param.name == "colors":
            return (0, 0, 0) * 20
        elif param.name == "form":
            return [(0, 0), (1, 0), (1, 10), (-1000, 23), (0, 0)]
        elif param.name == "color" or param.name == "color_bord":
            return 0, 0, 0, 0
        elif param.name == "group" or param.name == "groups":
            return
        elif param.name == "func":
            return lambda x: x * 2
        elif param.name == "args" or param.name == "widget":
            return TestWidget()
        elif param.name == "event":
            return "it`s work"
        elif param.name == "textures":
            return handler.textures
        elif param.name == "handler":
            return handler
        print(f"Can`t test value:\t {param.name}")
        return None


def test_class_methods(obj: Any):
    print(f"\n\tTesting class {obj.__class__.__name__}")
    methods = [m for m in inspect.getmembers(obj, predicate=inspect.ismethod) if
               m[1].__module__ == obj.__class__.__module__]
    results = []
    total_methods = len(methods)
    for name, method in methods:
        sig = inspect.signature(method)
        args = [generate_random_arg(param) for param in sig.parameters.values()]
        start_time = time.time()
        try:
            result_value = method(*args)
            elapsed_time = time.time() - start_time
            if elapsed_time > 5:
                result = f"\033[31m{name}: TOO SLOW\033[0m"
            elif elapsed_time >= 1:
                result = f"\033[33m{name}: SLOW\033[0m"
            else:
                result = f"\033[32m{name}: OK\033[0m"
            print(f"{result} | Result: {result_value}")
            results.append((name, result, result_value))
        except Exception as e:
            print(f"\033[31m{name}: FAILED, REASON: {e}\033[0m Input data: {args}")
            results.append((name, f"{name}: FAILED, REASON: {e}", None))
    success_count = sum(1 for _, r, _ in results if "OK" in r or "SLOW" in r)
    success_rate = (success_count / total_methods * 100) if total_methods > 0 else 0
    print(
        f"\033[30mSuccessful methods percentage: \033[{31 if success_rate <= 50 else 33 if success_rate <= 80 else 32}m{success_rate:.2f}%\033[0m")


pygame.display.iconify()
test_class_methods(handler)
test_class_methods(Textures())
print("Testing Widgets")
test_class_methods(DropDown([testImage] * 5, (0, 0), ["1", "2", '3']))
test_class_methods(Button([testImage] * 5, (0, 0)))
test_class_methods(Label("text", (0, 0), 10))
test_class_methods(Image(testImage, (0, 0)))
test_class_methods(InteractLabel([testImage] * 5, (0, 0)))
test_class_methods(Slicer([testImage] * 5, (0, 0)))
test_class_methods(Surface())
test_class_methods(Figure((0, 0), (0, 0, 0, 255), form=[(0, 0), (1, 0), (1, 10), (-1000, 23), (0, 0)]))
test_class_methods(Circle((0, 0), (0, 0, 0)))
test_class_methods(Switch([testImage] * 5, (0, 0)))
print("Testing Sounds")
test_class_methods(Sounds())
print("Testing Objects")
test_class_methods(MainCamera())
print("Testing Interfaces")
test_class_methods(Test(None, (0, 0), handler.textures))
print("Testing logics")
test_class_methods(Scene(handler))
print("Testing Visual")
test_class_methods(Render(handler))
test_class_methods(Effect((0, 0), [testImage] * 5))
test_class_methods(Information((0, 0), "test", 2, testImage))
