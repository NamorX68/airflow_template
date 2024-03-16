import json
import subprocess
from pathlib import Path

DEPENDENCIES = ["pandas@^2.2.0", "pydantic@^2.6.1"]
DEPENDENCIES_DEV = ["apache-airflow==2.8.2", "virtualenv@^20.25.1"]


def write_dict_to_json_file(file_path, data):
    file_path.touch(exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def write_text_to_file(file_path, data):
    file_path.touch(exist_ok=True)
    with open(file_path, "w") as file:
        file.writelines(data)


def create_folders(project_dir):
    folders = [".vscode", "dags", project_dir.name, "data", "tests"]
    for folder_name in folders:
        folder_path = project_dir / folder_name
        folder_path.mkdir(exist_ok=True)


def create_settings_file(vscode_folder, dag_path):
    settings = {
        "[python]": {
            "editor.formatOnSave": True,
            "editor.defaultFormatter": "charliermarsh.ruff",
        },
        "ruff.importStrategy": "useBundled",
        "python.analysis.extraPaths": [".", "dags"],
        "python.testing.pytestArgs": ["tests"],
        "python.testing.unittestEnabled": False,
        "python.testing.pytestEnabled": True,
        "terminal.integrated.env.linux": {"AIRFLOW__CORE__DAGS_FOLDER": dag_path},
    }
    # Erstelle settings.json-Datei
    settings_json_path = vscode_folder / "settings.json"
    write_dict_to_json_file(settings_json_path, settings)


def create_launch_file(vscode_folder, project_name):
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Module",
                "type": "python",
                "request": "launch",
                "module": project_name + ".${fileBasenameNoExtension}",
                "console": "integratedTerminal",
                "justMyCode": False,
            }
        ],
    }

    # Erstelle launch.json-Datei
    launch_json_path = vscode_folder / "launch.json"
    write_dict_to_json_file(launch_json_path, launch)


def poetry_create_package(project_name: str):
    poetry_command = ["poetry", "init", "--name", project_name]
    subprocess.run(poetry_command)


def poetry_add_dependencies(dependencies):
    for modul in dependencies:
        poetry_command = ["poetry", "add", modul]
        subprocess.run(poetry_command)


def poetry_install_package():
    poetry_command = ["poetry", "install"]
    subprocess.run(poetry_command)


def create_project_structure():
    # Bestimme das aktuelle Verzeichnis
    current_dir = Path.cwd()
    project_name = current_dir.name

    # Erstelle Unterordner für verschiedene Teile des Projekts
    create_folders(current_dir)
    
    (current_dir / project_name / '__init__.py').touch(exist_ok=True)

    # Initialisiere das Python-Paket mit Poetry, falls es nicht bereits existiert
    if not (current_dir / "pyproject.toml").exists():
        poetry_create_package(project_name)
        # poetry_add_dependencies(DEPENDENCIES)
        # poetry_add_dependencies(DEPENDENCIES_DEV)
    else:
        poetry_install_package()


    # Erstelle Dateien im .vscode-Ordner
    vscode_folder = current_dir / ".vscode"
    vscode_folder.mkdir(exist_ok=True)

    # Erstelle launch.json-Datei und schreibe LAUNCH
    create_launch_file(vscode_folder, project_name=project_name)

    # Erstelle settings.json-Datei und schreibe SETTINGS
    create_settings_file(vscode_folder, dag_path=str((current_dir / "dags").resolve()))
    
    txt = """
    import os
    import sys
    from airflow.models import Variable

    def is_prod():
        if stage := Variable.get("STAGE"):
            return stage.lower() == "prod"
        return False


    def is_qual():
        if stage := Variable.get("STAGE"):
            return stage.lower() == "qual"
        return False


    def get_python_path(name: str):
        if not is_prod() and not is_qual():
            for p in sys.path:
                if p.endswith("dags"):
                    return os.path.dirname(p)
        return f"/opt/airflow/dags/{name}.zip"
    """
    util_file_path = current_dir / "dags" / "util.py"
    write_text_to_file(file_path=util_file_path, data=txt)

    print(f"Projektstruktur für '{current_dir.name}' wurde erstellt.")


def main():
    create_project_structure()


if __name__ == "__main__":
    main()
