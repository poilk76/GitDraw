from sys import argv
from subprocess import run
from json import load
import os

SETTINGS_PATH = argv[1]
with open(SETTINGS_PATH,'r',encoding='UTF-8') as f:
    settings = load(f)
os.chdir(argv[2])
HANDLED_COMMANDS = [
    "push"
]

def main() -> None:

    if argv[3] in HANDLED_COMMANDS:

        print(argv[3:])
        
    else:

        print(run(
            [settings["ORIGINAL_PATH"]]+argv[3:]
        ))


if __name__ == "__main__":

    main()