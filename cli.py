import argparse

import PyInstaller.__main__

from hooks import hook_resizer, hook_translate


def build_with_pyinstaller(args):
    PyInstaller.__main__.run(
        [
            args.source_file,
            f"--name={args.output_name}",
            "--paths=.",
            f"--add-data={args.dialog_dir}:dialog",
            f"--add-data={args.img_dir}:img",
            "--add-data=save:save",
            "--add-data=translated_dialog:translated_dialog",
            "--onefile",
            "--windowed",
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Build a Python project with PyInstaller.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source_file",
        type=str,
        help="Path to the Python source file.",
    )
    parser.add_argument(
        "--output_name",
        type=str,
        # required=True,
        default="PyNarrator",
        help="Name for the output executable.",
    )

    parser.add_argument(
        "--dialog_dir",
        type=str,
        # required=True,
        default="./dialog",
        help="Path to the directory with the dialog files",
    )
    parser.add_argument(
        "--img_dir",
        type=str,
        # required=True,
        default="./img",
        help="Path to the directory with the image files",
    )

    parser.add_argument(
        "--languages",
        type=str,
        # required=True,
        default="english,portuguese,spanish",
        help="Langues that the game will support",
    )
    parser.add_argument(
        "--resolution",
        type=str,
        # required=True,
        default="fullhd",
        help="In game image resolution",
    )

    args = parser.parse_args()

    # Run Translation Hook
    hook_translate.main(args)

    # Run Resize Hook
    hook_resizer.main(args)

    # run PyInstaller
    build_with_pyinstaller(args)


if __name__ == "__main__":
    main()
