import json
import subprocess
from pathlib import Path

DEPENDENCIES = ['pandas@^2.2.0', 'pydantic@^2.6.1']
DEPENDENCIES_DEV = ['apache-airflow==2.8.2', 'virtualenv@^20.25.1']


def write_dict_to_json_file(file_path, data):
    file_path.touch(exist_ok=True)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def write_text_to_file(file_path, data):
    file_path.touch(exist_ok=True)
    with open(file_path, 'w') as file:
        file.writelines(data)


def create_folders(project_dir):
    folders = ['.vscode', 'dags', project_dir.name, 'data', 'tests']
    for folder_name in folders:
        folder_path = project_dir / folder_name
        folder_path.mkdir(exist_ok=True)


def create_settings_file(vscode_folder, dag_path):
    settings = {
        '[python]': {
            'editor.formatOnSave': True,
            'editor.defaultFormatter': 'charliermarsh.ruff',
        },
        'ruff.importStrategy': 'useBundled',
        'python.analysis.extraPaths': ['.', 'dags'],
        'python.testing.pytestArgs': ['tests'],
        'python.testing.unittestEnabled': False,
        'python.testing.pytestEnabled': True,
        'terminal.integrated.env.linux': {'AIRFLOW__CORE__DAGS_FOLDER': dag_path},
    }
    # Erstelle settings.json-Datei
    settings_json_path = vscode_folder / 'settings.json'
    write_dict_to_json_file(settings_json_path, settings)


def create_launch_file(vscode_folder, project_name):
    launch = {
        'version': '0.2.0',
        'configurations': [
            {
                'name': 'Python: Module',
                'type': 'python',
                'request': 'launch',
                'module': project_name + '.${fileBasenameNoExtension}',
                'console': 'integratedTerminal',
                'justMyCode': False,
            }
        ],
    }

    # Erstelle launch.json-Datei
    launch_json_path = vscode_folder / 'launch.json'
    write_dict_to_json_file(launch_json_path, launch)


def create_util_file(file_path):
    txt = """
    import os
    import sys
    from airflow.models import Variable

    def is_prod():
        if stage := Variable.get('STAGE'):
            return stage.lower() == 'prod'
        return False


    def is_qual():
        if stage := Variable.get('STAGE'):
            return stage.lower() == 'qual'
        return False


    def get_python_path(name: str):
        if not is_prod() and not is_qual():
            for p in sys.path:
                if p.endswith('dags'):
                    return os.path.dirname(p)
        return f'/opt/airflow/dags/{name}.zip'
    """
    write_text_to_file(file_path=file_path, data=txt)
    

def create_default_file(file_path):
    txt = """
    from airflow.utils.dates import days_ago

    default_args = {
        'owner': 'USERNAME',  # The owner of the code or the person responsible for maintaining it
        'start_date': days_ago(1),  # The date the DAG should start running
        'catchup': False,  # Whether or not Airflow should run the DAG for the dates it missed while it wasn't running
    }
    """
    write_text_to_file(file_path=file_path, data=txt)


def create_dag_template(file_path):
    txt = f"""
    """
    write_text_to_file(file_path=file_path, data=txt)


def create_airflow_config(file_path):
    if not file_path.exists():
        airflow_port = input('Auf welchem Port soll Airflow laufen?:')
        logserver_port = input('Auf welchem Port soll der Log-Server laufen?:')
        txt = f"""
    [core]
    load_examples = False
     
    [database]
    load_default_connections = False
     
    [logging]
    worker_log_server_port = {logserver_port} # Auf freien Port anpassen!
    file_task_handler_new_folder_permissions = 0o700
    file_task_handler_new_file_permissions = 0o600
     
    [webserver]
    expose_config = True
    enable_swagger_ui = False
    web_server_port = {airflow_port} # Auf freien Port anpassen!
     
    [scheduler]
    parsing_processes = 1
    """
        write_text_to_file(file_path=file_path, data=txt)


def poetry_create_package(project_name: str):
    poetry_command = ['poetry', 'init', '--name', project_name]
    subprocess.run(poetry_command)


def poetry_add_dependencies(dependencies):
    for modul in dependencies:
        poetry_command = ['poetry', 'add', modul]
        subprocess.run(poetry_command)


def poetry_install_package():
    poetry_command = ['poetry', 'install']
    subprocess.run(poetry_command)


def create_project_structure():
    # Bestimme das aktuelle Verzeichnis
    current_dir = Path.cwd()
    project_name = current_dir.name

    create_folders(current_dir)

    (current_dir / project_name / '__init__.py').touch(exist_ok=True)

    if not (current_dir / 'pyproject.toml').exists():
        poetry_create_package(project_name)
        poetry_add_dependencies(DEPENDENCIES)
        poetry_add_dependencies(DEPENDENCIES_DEV)
    else:
        poetry_install_package()

    vscode_folder = current_dir / '.vscode'
    vscode_folder.mkdir(exist_ok=True)
    create_launch_file(vscode_folder, project_name=project_name)
    create_settings_file(vscode_folder, dag_path=str((current_dir / 'dags').resolve()))

    dags_folder = current_dir / 'dags'
    create_util_file(file_path=(dags_folder / 'util.py'))
    create_default_file(file_path=(dags_folder / 'default_args.py'))
    create_dag_template(file_path=(dags_folder / 'app.py'))

    create_airflow_config(Path('~/airflow/airflow.cfg'))

    print(f'Projektstruktur für '{current_dir.name}' wurde erstellt.')


def main():
    create_project_structure()


if __name__ == '__main__':
    main()
