import os
import winreg
from pathlib import Path
from subprocess import check_output

def main() -> None:

    current_path = Path(os.path.abspath(__file__)).parent
    git_path = check_output(["where","git"])

    print(str(git_path.decode()))

    with open('.env','w+') as f:

        f.write(f'REGULAR_GIT_PATH="{git_path.decode().strip().split("\n")[-1]}"')

    key_path = r"Environment"

    with open(f'{current_path}\\git.cmd','w+') as f:

        f.write(f"""
@echo off
python {current_path}\\main.py %*
""")

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        key_path,
        0,
        winreg.KEY_READ | winreg.KEY_WRITE
    ) as key:

        try:
            path,_ = winreg.QueryValueEx(key,"Path")
        except FileNotFoundError:
            path = ""

        paths = path.split(";") if path else []

        if current_path not in paths:
            paths.insert(0,str(current_path))

            winreg.SetValueEx(
                key,
                "Path",
                0,
                winreg.REG_EXPAND_SZ,
                ";".join(paths)
            )
        

    print("All done!")

if __name__ == "__main__":

    main()