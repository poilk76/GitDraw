import os
import winreg
from pathlib import Path
from subprocess import check_output, run
from json import dump
import venv

CURRENT_PATH = Path(os.path.abspath(__file__)).parent
try:
    ORIGINAL_GIT_PATH = check_output(["where","git"])\
                                    .decode()\
                                    .strip()\
                                    .split('\n')[-1]
except: 
    ORIGINAL_GIT_PATH = "C:\\Program Files\\Git\\cmd\\git.exe"
KEY_PATH = r"Environment"
VENV_PATH = CURRENT_PATH / ".venv"
PYTHON_PATH = CURRENT_PATH / ".venv/Scripts/python.exe"
PROGRAM_PATH = CURRENT_PATH / "main.py"

def create_venv() -> None:

    if not VENV_PATH.exists():
        print("Creating virtual enviroment...")

        venv.create(
            VENV_PATH,
            with_pip=True
        )

        run(
            [
                PYTHON_PATH,
                "-m",
                "pip",
                "install",
                "-r",
                "./requirements.txt"
            ]
        )



def create_settings() -> None:

    print("Creating settings")

    with open('./settings.json','w+',encoding="UTF-8") as f:

        dump({"ORIGINAL_GIT_PATH":ORIGINAL_GIT_PATH},f)

def create_starting_file() -> None:

    print("Creating cmd starting file")

    with open(f'{CURRENT_PATH}/git.cmd','w+') as f:

         f.write(f"""
@echo off
{PYTHON_PATH} {PROGRAM_PATH} %*
""")

def add_program_path() -> None:

    print("Adding to PATHS")

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        KEY_PATH,
        0,
        winreg.KEY_READ | winreg.KEY_WRITE
    ) as key:

        try:
            path,_ = winreg.QueryValueEx(key,"Path")
        except:
            path = ""

        paths = path.split(";") if path else []

        if CURRENT_PATH not in paths:
            paths.insert(0,str(CURRENT_PATH))

            winreg.SetValueEx(
                key,
                "Path",
                0,
                winreg.REG_EXPAND_SZ,
                ";".join(paths)
            )

def main() -> None:

    create_venv()
    create_starting_file()
    add_program_path()
    create_settings()

    print("All done!")

if __name__ == "__main__":

    main()