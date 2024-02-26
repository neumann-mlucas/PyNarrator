from dataclasses import dataclass


@dataclass
class Config:
    dialog_path: str = "/home/neumann/Desktop/oppaiman/dialog"
    image_path: str = "/home/neumann/Desktop/oppaiman/img"

    width: int = 640
    height: int = 480
