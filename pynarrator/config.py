from dataclasses import dataclass


@dataclass
class Config:
    dialog_path: str = "/home/neumann/Desktop/oppaiman/dialog"
    image_path: str = "/home/neumann/Desktop/oppaiman/img"
    save_path: str = "/home/neumann/Desktop/oppaiman/save"

    width: int = 640
    height: int = 480
