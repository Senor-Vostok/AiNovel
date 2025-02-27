import shutil
import tkinter as tk
from tkinter import filedialog
import os

def get_new_asset_name():
    asset_number = len(os.listdir("Assets/Characters")) + 1
    return f"Characters/character{asset_number}.png"


def choose_asset(asset_type):
    root = tk.Tk()
    root.withdraw()

    file_path = tk.filedialog.askopenfilename(
        initialdir="/",
        title="Выберите файл",
        filetypes=[("PNG files", "*.png")])

    if file_path:
        if asset_type == "character":
            file_name = get_new_asset_name()
        elif asset_type == "location":
            file_name = "Locations/" + os.path.basename(file_path)
            if os.path.exists(f"Assets/Locations/{file_name}"):
                # Написать, что локация с таким названием уже есть (?)
                return
        else:
            return

        shutil.copy(file_path, f"Assets/{file_name}")
    else:
        # Написать, что файл не выбран (?)
        return

choose_asset("character")
