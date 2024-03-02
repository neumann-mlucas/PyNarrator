import tomllib

from config import Config
from deep_translator import GoogleTranslator
import json
from typing import Any
from logger import get_logger
from typing import Iterator

from pathlib import Path

dir_path = Path("/home/neumann/Desktop/oppaiman/dialog")
logger = get_logger()


class TranslateDialogs:
    def __init__(self, config: Config, target_language: str = "en") -> None:
        self.source_language = "pt"
        self.target_language = target_language

        self.translator = GoogleTranslator(
            source=self.source_language, trarget=self.target_language
        )

        assert Path(config.source_dialog_path).exists()
        self.source_dir = Path(config.source_dialog_path)

        self.target_dir = Path(config.dialog_path) / self.target_language
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def translate_dialog(self, dialog: dict) -> dict:
        return dict(self.translate_key_value(k, v) for k, v in dialog.items())

    def translate_key_value(self, key: str, value: Any) -> dict:
        match key, value:
            case "text", str():
                return key, self.translator.translate(value)
            case str(), dict():
                translated_dict = dict(
                    self.translate_key_value(k, v) for k, v in value.items()
                )
                return (key, translated_dict)
            case _, _:
                return key, value

    def load_dialogs(self) -> Iterator[dict]:
        for file in self.source_dir.rglob("*.toml"):
            logger.info(f"Trying to load file: {file}")
            try:
                with open(file, "rb") as fp:
                    dialog = tomllib.load(fp)
                yield dialog
            except (tomllib.TOMLDecodeError, FileNotFoundError, PermissionError) as exp:
                logger.error(f"Error {exp} while reading {file}")
                continue

    def save_dialog(self, dialog: dict) -> None:
        if "label" not in dialog and "text" not in dialog:
            logger.error(f"Bad dialog formatting / structure: {dialog}")
            return

        filepath = self.target_dir / f"{dialog['label']}.json"
        with open(filepath, "w") as fp:
            json.dump(dialog, fp)

    def run(self):
        logger.info(f"> Starting Translation to {self.target_language}")
        for dialog in self.load_dialogs():
            translated = self.translate_dialog(dialog)
            self.save_dialog(translated)
            logger.info(
                f"Dialog {dialog.get('label')!r} was translated to {self.target_language!r}"
            )
        logger.info(f"> Done with Translation to {self.target_language}")


def main():
    config = Config()
    for lang in config.languages:
        print(lang)
        TranslateDialogs(config, lang).run()


main()
