import tomllib

from copy import deepcopy
from dataclasses import field, dataclass
from pathlib import Path
from typing import Iterator, Any, Generator

from config import Config
from logger import get_logger

logger = get_logger()


@dataclass
class DialogNode:
    "represent an in game dialog"

    label: str
    text: str
    image: str

    options: list["DialogOption"] = field(default_factory=list)

    def __str__(self) -> str:
        opts = "\n\t".join(map(str, self.options))
        return f"[DIALOG {self.label!r}]:\n{self.text}\n\t{opts}"


@dataclass
class DialogOption:
    "represent an option of a given dialog"

    label: str
    text: str

    def __str__(self) -> str:
        return f"<OPTION : {self.label!r}>: {self.text}"


class LoadDialogs:
    "function pipeline to read tomls files and parse then into a dialog graph"

    @staticmethod
    def load_tomls(dir: str) -> Iterator[dict]:
        "givem a directory, reads all toml files and yield each one of then"
        dir_path = Path(dir)
        assert dir_path.exists(), f"Dialog directory {dir!r} doesn't exist"

        for file in dir_path.rglob("*.toml"):
            # read toml file
            try:
                with open(file, "rb") as fp:
                    dialog = tomllib.load(fp)
                yield dialog
            except (tomllib.TOMLDecodeError, FileNotFoundError, PermissionError) as exp:
                logger.error(f"Error {exp} while reading {file}")
                continue

    @staticmethod
    def parse_option(opt: dict) -> DialogOption:
        "parse a toml item into a DialogOption"
        return DialogOption(label=opt.pop("label"), text=opt.pop("text"))

    @classmethod
    def parse_dialog(cls, dialog: dict[str, Any]) -> DialogNode | None:
        "tries to parse a toml object into DialogNode, returns None in case of error"
        try:
            node = DialogNode(
                label=dialog.pop("label"),
                text=dialog.pop("text"),
                image=dialog.pop("image"),
            )
            node.options = [cls.parse_option(opt) for label, opt in dialog.items()]
            return node
        except (ValueError, KeyError) as exp:
            logger.error(f"Error {exp} when parsing {dialog}")
            return None

    @staticmethod
    def validate_dialogs(dialogs: dict[str, DialogNode]) -> None:
        "checks if all dialog options point to an existing dialog node"
        missing_labels = [
            option.label
            for dialog in dialogs.values()
            for option in dialog.options
            if option.label not in dialogs.keys()
        ]
        if missing_labels:
            raise Exception(f"Missing Dialog Nodes : {missing_labels}")

    @classmethod
    def run(cls, config: Config) -> dict[str, DialogNode]:
        "load dialogs from the config"
        # load dialog files
        tomls = cls.load_tomls(config.dialog_path)
        # try to parse toml files into a dialog graph
        dialog_map = {
            dialog.label: dialog for dialog in map(cls.parse_dialog, tomls) if dialog
        }
        # validated dialogs
        cls.validate_dialogs(dialog_map)

        # TODO: function here to translate text
        return dialog_map


def walk_dialog(dialogs: dict[str, DialogNode], start: str = "root") -> Generator:
    "genrator that walks the dialog graph, given a next node to visit if yield the node and the walinkg history"
    current, breadcrumbs = start, []
    while True:
        node = dialogs[current]
        breadcrumbs.append(current)

        if current == "end":
            yield (node, breadcrumbs)
            break
        current = yield (node, breadcrumbs)
        assert current in (
            opt.label for opt in node.options
        ), "Select option in not avalible for this node"


class DialogFacade:
    "encapsulates the dialog graph behavior"

    def __init__(self, config, start="root"):
        self._dialogs = LoadDialogs.run(config)
        self._walker = walk_dialog(self._dialogs, start)
        self._current, self._history = next(self._walker)

    def next(self, option: str) -> DialogNode:
        "choose an option and go to the next dialog node"
        self._current, self._history = self._walker.send(option)
        return deepcopy(self._current)

    @property
    def current(self) -> DialogNode:
        "get current node"
        return deepcopy(self._current)

    @property
    def history(self) -> tuple[str]:
        "get history of nodes visited"
        return tuple(self._history)

    @property
    def current_text(self) -> str:
        return self._current.text

    @property
    def current_img(self) -> str:
        return self._current.image

    @property
    def current_options(self) -> list[DialogOption]:
        return deepcopy(self._current.options)

    def reset(self) -> None:
        "reset the dialog to the starting position"
        self._walker = walk_dialog(self._dialogs)
        self._current, self._history = next(self._walker)

    def load(self, history: list[str]) -> None:
        pass
