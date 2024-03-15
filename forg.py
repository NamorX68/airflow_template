import json
from pathlib import Path
from poetry.factory import Factory

SETTINGS = {}
LAUNCH = {}

def write_dict_to_json_file(file_path, data):
    """
    Schreibt ein Dictionary als JSON in eine Datei.

    Args:
        file_path (str): Der Pfad inklusive Dateinamen, wo das JSON gespeichert werden soll.
        data (dict): Das Dictionary, das als JSON gespeichert werden soll.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def create_folders(project_dir):
    folders = ['.vscode', 'dags', project_dir.name, 'data', 'tests']
    for folder_name in folders:
        folder_path = project_dir / folder_name
        folder_path.mkdir(exist_ok=True)

def create_settings_file(vscode_folder):
    # Erstelle settings.json-Datei
    settings_json_path = vscode_folder / 'settings.json'
    settings_json_path.touch()

    # Schreibe SETTINGS in settings.json-Datei
    write_dict_to_json_file(settings_json_path, SETTINGS)

def create_launch_file(vscode_folder):
    # Erstelle launch.json-Datei
    launch_json_path = vscode_folder / 'launch.json'
    launch_json_path.touch()

    # Schreibe LAUNCH in launch.json-Datei
    write_dict_to_json_file(launch_json_path, LAUNCH)

def create_poetry_package(project_name):
    factory = Factory()
    poetry = factory.create_poetry(Path.cwd() / project_name)
    poetry.create(project_name)

def create_project_structure(project_name):
    # Erstelle den Hauptordner für das Projekt
    project_dir = Path.cwd() / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    # Erstelle Unterordner für verschiedene Teile des Projekts
    create_folders(project_dir)

    # Erstelle Dateien im .vscode-Ordner
    vscode_folder = project_dir / '.vscode'
    vscode_folder.mkdir(exist_ok=True)

    # Erstelle launch.json-Datei und schreibe LAUNCH
    create_launch_file(vscode_folder)

    # Erstelle settings.json-Datei und schreibe SETTINGS
    create_settings_file(vscode_folder)

    # Erstelle Python-Paket mit Poetry
    create_poetry_package(project_name)

    print(f"Projektstruktur für '{project_name}' wurde erstellt.")

def main():
    project_name = input("Bitte geben Sie den Namen des Projekts ein: ")
    create_project_structure(project_name)

if __name__ == "__main__":
    main()
