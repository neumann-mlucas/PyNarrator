.PHONY: clean build run

SPEC_FILE=./PyNarrator.spec

APP_NAME=PyNarrator

PYINSTALLER_CMD=poetry run pyinstaller

DIST_DIR=./dist
BUILD_DIR=./build

export PYNARRATOR_DIALOG_PATH=./dialog
export PYNARRATOR_TRANS_DIALOG_PATH=./translated_dialog
export PYNARRATOR_GAME_LANGUAGES="english,portuguese,spanish"

build:
	# install packages
	poetry install
	# run pre build hook to translated the dialogs
	poetry run python hooks/hook-translate.py
	# build the executable file
	$(PYINSTALLER_CMD) $(SPEC_FILE)

clean:
	rm -rf $(DIST_DIR)
	rm -rf $(BUILD_DIR)

run:
	./$(DIST_DIR)/$(APP_NAME)
