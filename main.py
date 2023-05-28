import os
import platform
import subprocess
import time
import venv
from distutils.dir_util import copy_tree
from typing import Dict

import inquirer
from halo import Halo
from rich.console import Console
from rich.text import Text

current_directory = os.path.dirname(os.path.realpath(__file__))
frameworks = os.path.join(current_directory, "src")

db = {
    "postgresql": "psycopg2",
    "mysql": "mysql-connector-python",
}
dots = {
    "interval": 80,
    "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
}


def main() -> None:
    """create-python-app entrypoint"""

    prompts = [
        inquirer.List(
            "framework",
            message="Choose a backend framework",
            choices=["FastAPI", "Flask", "DRF"],
            carousel=True,
        ),
        inquirer.List(
            "database",
            message="Choose a database",
            choices=["PostgreSQL", "MySQL", "SQLite"],
            carousel=True,
        ),
        inquirer.Text(
            "path",
            message="Path for application",
            default=current_directory,
        ),
    ]
    answers: Dict[str, str] = inquirer.prompt(prompts)

    start = time.time()
    console = Console()

    app_path = answers["path"]
    database = answers["database"].lower()
    framework = answers["framework"].lower()

    if os.path.isdir(app_path):
        text = Text.assemble("\n[", ("ERROR", "red"), "] Directory already exists")
        console.print(text)
        exit(0)
    framework_path = os.path.join(frameworks, framework)
    copy_tree(framework_path, app_path)
    text = Text.assemble("\n[", ("OK", "green"), "] Project Directory created")
    console.print(text)

    spinner = Halo(text="Creating virtual environment", spinner=dots)
    spinner.start()
    try:
        venv_path = os.path.join(app_path, "venv")
        venv.create(venv_path, with_pip=True)
    except:
        spinner.stop()
        text = Text.assemble(
            "\n[", ("ERROR", "red"), "] Unable to create virtual environment"
        )
        console.print(text)
        exit(0)
    spinner.stop()
    text = Text.assemble("[", ("OK", "green"), "] Virtual environment created")
    console.print(text)

    if database != "sqlite":
        with open(os.path.join(app_path, "requirements.txt"), mode="a") as reqs:
            reqs.write(db[database] + "\n")

    spinner = Halo(text="Installing dependencies", spinner=dots)
    spinner.start()
    try:
        os.chdir(app_path)
        if platform.system() == "Windows":
            subprocess.run(
                [r"venv\Scripts\pip", "install", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
        else:
            subprocess.run(
                [r"venv\bin\pip", "install", "-r", "requirements.txt"],
                cwd=app_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
    except:
        spinner.stop()
        text = Text.assemble(
            "\n[", ("ERROR", "red"), "] Unable to install dependencies"
        )
        console.print(text)
        exit(0)
    spinner.stop()
    text = Text.assemble("[", ("OK", "green"), "] Dependencies installed")
    console.print(text)

    end = time.time()
    text = Text.assemble(
        "[", ("INFO", "yellow"), f"] Completed in {end - start:.2f} seconds"
    )
    console.print(text)
