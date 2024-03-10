import logging
import shutil
from pathlib import Path

from PIL import Image


class ResizeImages:
    def __init__(self, resolution_alias: str, source: str, target: str) -> None:
        self.resolution = self.to_resolution(resolution_alias)

        assert Path(source).exists()
        self.source_dir = Path(source)

        self.target_dir = Path(target)
        self.target_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def to_resolution(alias: str) -> tuple[int, int]:
        match alias.strip().lower():
            case "hd":
                return (1280, 720)
            case "fullhd":
                return (1920, 1080)
            case "2k":
                return (2048, 1080)
            case "qhd":
                return (2048, 1080)
            case "4k":
                return (4096, 2160)
            case _:
                return (1280, 720)

    def resize_img(self, input: Path) -> Image:
        image = Image.open(str(input))
        return image.resize(self.resolution, Image.Resampling.LANCZOS)

    def save_img(self, src_file: Path, img: Image) -> None:
        dst = self.target_dir / src_file.name
        img.save(str(dst))

    def run(self) -> None:
        logging.info(f"> Starting Image Resizing To {self.resolution}")
        for file in self.source_dir.rglob("*"):
            logging.info(f"trying to load file: {file}")
            try:
                img = self.resize_img(file)
                self.save_img(file, img)
                logging.info(f"image {file.name!r} was resized")
            except Exception as exp:
                logging.error(f"error {exp} while resizing image: {file}")
                continue
        logging.info("> Done with Resizing")


def clean_dir(dir: str) -> None:
    dir = Path(dir)
    dir.mkdir(parents=True, exist_ok=True)

    for dir in (p for p in dir.glob("*") if p.is_dir()):
        shutil.rmtree(dir)


def main(args=None):
    resolution = "hd" if args is None else args.resolution
    source_dir = "./img" if args is None else args.img_dir
    target_dir = "./resized_img"

    clean_dir(target_dir)
    ResizeImages(resolution, source_dir, target_dir).run()


if __name__ == "__main__":
    main()
