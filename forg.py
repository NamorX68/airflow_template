import json
import subprocess
from pathlib import Path

SETTINGS = {}
LAUNCH = {}


def write_dict_to_json_file(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def create_folders(project_dir):
    folders = [".vscode", "dags", project_dir.name, "data", "tests"]
    for folder_name in folders:
        folder_path = project_dir / folder_name
        folder_path.mkdir(exist_ok=True)


def create_settings_file(vscode_folder):
    # Erstelle settings.json-Datei
    settings_json_path = vscode_folder / "settings.json"


    # Schreibe SETTINGS in settings.json-Datei
    write_dict_to_json_file(settings_json_path, SETTINGS)


def create_launch_file(vscode_folder):
    # Erstelle launch.json-Datei
    launch_json_path = vscode_folder / "launch.json"
    launch_json_path.touch()

    # Schreibe LAUNCH in launch.json-Datei
    write_dict_to_json_file(launch_json_path, LAUNCH)


def poetry_create_package():
    poetry_command = ["poetry", "init"]
    subprocess.run(poetry_command)


def poetry_add_dependencies():
    pass


def poetry_install_package():
    poetry_command = ["poetry", "install"]
    subprocess.run(poetry_command)


def create_project_structure():
    # Bestimme das aktuelle Verzeichnis
    current_dir = Path.cwd()
    project_name = current_dir.name

    # Initialisiere das Python-Paket mit Poetry, falls es nicht bereits existiert
    if not (current_dir / "pyproject.toml").exists():
        poetry_create_package()
    
    else:
        poetry_install_package()

    # Erstelle Unterordner für verschiedene Teile des Projekts
    create_folders(current_dir)

    # Erstelle Dateien im .vscode-Ordner
    vscode_folder = current_dir / ".vscode"
    vscode_folder.mkdir(exist_ok=True)

    # Erstelle launch.json-Datei und schreibe LAUNCH
    create_launch_file(vscode_folder)

    # Erstelle settings.json-Datei und schreibe SETTINGS
    create_settings_file(vscode_folder)

    print(f"Projektstruktur für '{current_dir.name}' wurde erstellt.")


def main():
    create_project_structure()


if __name__ == "__main__":
    main()
