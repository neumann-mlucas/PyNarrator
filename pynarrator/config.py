from dataclasses import dataclass


@dataclass
class Config:
    source_dialog_path: str = "/home/neumann/Desktop/oppaiman/dialog"
    dialog_path: str = "/home/neumann/Desktop/oppaiman/DIALOG"

    image_path: str = "/home/neumann/Desktop/oppaiman/img"
    save_path: str = "/home/neumann/Desktop/oppaiman/save"

    width: int = 640
    height: int = 480

    languages = ("en", "pt", "ge")
    language = "pt"
