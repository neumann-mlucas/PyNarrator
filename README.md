# PyNarrator

## Overview

PyNarrator is a dialogue-based game created as a coding challenge for a job interview. This repository implements a dialogue tree allowing users to navigate through different interactions. The example dialogue in the config folder demonstrates a simple client-waiter interaction in a restaurant, with all dialogues structured as TOML files. The game leverages the `pygame` library for rendering the screen and capturing user events. It supports saving the game state and changing the dialogue language. Deployment is facilitated by `PyInstaller`, which compiles the game into a standalone executable file. Configuration for the build and options are specified in the `makefile`.

## Features

- **Dialogue Tree Customization**: Utilizes static configuration files.
- **Dialogue Options**: Support navigating to previously visited nodes, forming a dialogue graph.
- **Language Support**: Includes build-time configurable translation.
- **Save Game Support**: Dialogue state is saved in a temporary folder.
- **Cross-Platform Compatibility**: Compatible with Windows, macOS, and Linux.

## TODO

- [x] **Capture User Input**: A new view/controller class is needed. Due to time constraints, this feature was not implemented.
- [x] **Image Resolution Build Option**: Implementation would follow a similar approach to the translation hook. This feature was not completed on time.
- [x] **CLI Interface for Build Options**: Currently relies on a makefile for build configurations.

## Prerequisites

- Python 3.11 or higher
- Poetry package manager
- Pygame 2.5
- PyInstaller 6.4
- deep-translator 1.11

## Installation

```bash
git clone https://github.com/neumann-mlucas/PyNarrator.git
cd PyNarrator

# setup virtual env
poetry install
poetry shell

# build game
python cli.py pynarrator/main.py --output_name PyNarrator
```

### Build Options

```bash
# support different languages
python cli.py pynarrator/main.py --languages=english,german

# support a different resolution 
python cli.py pynarrator/main.py --resolution=fullhd

# build with different source dialog
python cli.py pynarrator/main.py --dialog_dir=./dialog
```

## Usage

To launch the game, execute:

```bash
# executable file in the distribution folder
./dist/PyNarrator
```

## Notes

The project adopts an MVC architecture: 
- The model directory contains functions for parsing dialogue configurations into objects, creating a dialogue graph accessible via the `DialogFacade` object. Dialogue configurations are simple TOML files detailing a label for internal reference, display text, background image, and options. Each option specifies text and a label for another dialogue node. TOML files are translated at build time and stored as JSON files for efficient serialization.
- The view directory houses classes responsible for rendering images and text on the game screen. Each screen displays main text and clickable options as well as the background image, with each view defining the main text, option texts, and, for the game view, each option's label.
- The controller manages user events and game state interactions within the main game loop. Each controller has a game state attribute and an options callback function, which is called when an option is selected. The game state attribute is updated to switch screens within the main game loop.
- The `main.py` file's main game loop selects the appropriate controller based on the game state, calls event handling functions, and refreshes the view.
