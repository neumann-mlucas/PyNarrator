import json
import logging
import os
import shutil
import tomllib
from pathlib import Path
from typing import Any, Iterator

from deep_translator import GoogleTranslator


class TranslateDialogs:
    def __init__(self, target_language: str, source: str, target: str) -> None:
        self.source_language = "portuguese"
        self.target_language = target_language

        self.translator = GoogleTranslator(
            source=self.source_language, target=self.target_language
        )

        assert Path(source).exists()
        self.source_dir = Path(source)

        self.target_dir = Path(target) / self.target_language
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def translate_dialog(self, dialog: dict) -> dict:
        return dict(self.translate_key_value(k, v) for k, v in dialog.items())

    def translate_key_value(self, key: str, value: Any) -> tuple[str, Any]:
        match key, value:
            case "text", str():
                return key, self.translator.translate(value)
            case str(), dict():
                translated_dict = dict(
                    self.translate_key_value(k, v) for k, v in value.items()
                )
                return (key, translated_dict)
            case _:
                return key, value

    def load_dialogs(self) -> Iterator[dict]:
        for file in self.source_dir.rglob("*.toml"):
            logging.info(f"Trying to load file: {file}")
            try:
                with open(file, "rb") as fp:
                    dialog = tomllib.load(fp)
                yield dialog
            except (tomllib.TOMLDecodeError, FileNotFoundError, PermissionError) as exp:
                logging.error(f"Error {exp} while reading {file}")
                continue

    def save_dialog(self, dialog: dict) -> None:
        if "label" not in dialog and "text" not in dialog:
            logging.error(f"Bad dialog formatting / structure: {dialog}")
            return

        filepath = self.target_dir / f"{dialog['label']}.json"
        with open(filepath, "w") as fp:
            json.dump(dialog, fp)

    def run(self):
        logging.info(f"> Starting Translation to {self.target_language}")
        for dialog in self.load_dialogs():
            translated = self.translate_dialog(dialog)
            self.save_dialog(translated)
            logging.info(
                f"Dialog {dialog.get('label')!r} was translated to {self.target_language!r}"
            )
        logging.info(f"> Done with Translation to {self.target_language}")


def clean_dir(dir: str) -> None:
    dir = Path(dir)
    dir.mkdir(parents=True, exist_ok=True)

    for dir in (p for p in dir.glob("*") if p.is_dir()):
        shutil.rmtree(dir)


def main(args: dict[str, str] = None):
    if args is None:
        languages = "english,portuguese"
        source_dir = "dialog_dir"
    else:
        languages = args.languages
        source_dir = args.dialog_dir
    target_dir = "./translated_dialog"

    clean_dir(target_dir)
    for lang in languages.strip('"').split(","):
        TranslateDialogs(lang, source_dir, target_dir).run()


if __name__ == "__main__":
    main()
