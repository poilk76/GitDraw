from sys import argv
from subprocess import run
from json import load
from requests import post

with open('settings.json','r') as f:
    settings = load(f)

ORIGINAL_GIT_PATH = settings["ORIGINAL_GIT_PATH"]
HANDLED_COMMANDS = [
    "commit",
    "push"
]

def main() -> None:

    if argv[1] in HANDLED_COMMANDS:

        post("http://"+settings["QUE_SERVER"]+"/add",json={"command":[ORIGINAL_GIT_PATH]+argv[1:],"priority":0})

    elif argv[1] == 'first':

        post("http://"+settings["QUE_SERVER"]+"/add",json={"command":[ORIGINAL_GIT_PATH]+argv[2:],"priority":1})
        
    elif argv[1] == 'force':

        print(run(
                    [ORIGINAL_GIT_PATH]+argv[2:],
                    check=True
                ))
        
    else:

        print(run(
            [ORIGINAL_GIT_PATH]+argv[1:],
            check=True
        ))


if __name__ == "__main__":

    main()