import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    source_dialog_path: str = "./dialog"
    dialog_path: str = "./translated_dialog"

    source_image_path: str = "./img"
    image_path: str = "./resized_img"

    save_path: str = "./save"

    width: int = 1208
    height: int = 720

    languages = ["english", "portuguese", "german"]
    language = "portuguese"

    def __post_init__(self) -> None:
        "check if pyinstaller tmp data directory is present and set the game data paths"
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            return

        # import time
        #
        # print(sys._MEIPASS)
        # time.sleep(300)

        self.source_dialog_path = os.path.join(base_path, "dialog")
        self.dialog_path = os.path.join(base_path, "translated_dialog")

        self.source_image_path = os.path.join(base_path, "img")
        self.image_path = os.path.join(base_path, "resized_img")

        self.save_path = os.path.join(base_path, "save")
        self.languages = self.get_languages()

    def get_languages(self) -> list[str]:
        return [p.name for p in Path(self.dialog_path).glob("*") if p.is_dir()]
