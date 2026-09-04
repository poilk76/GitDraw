from sys import argv
from subprocess import run, check_output
from json import load,dumps
import os

SETTINGS_PATH = argv[1]
with open(SETTINGS_PATH,'r',encoding='UTF-8') as f:
    settings = load(f)
os.chdir(argv[2])
HANDLED_COMMANDS = [
    "push"
]

def cmd_add(branch,commit,remote,priority) -> None:

    if branch == None:
        print("Add push to que")
        return 

    sha = check_output([settings["ORIGINAL_PATH"],"rev-parse",commit],shell=True).decode().strip()

    if priority == 'now':

        i = argv.index('--priority')
        argv.pop(i+1)
        argv.pop(i)

        run([settings["ORIGINAL_PATH"]]+argv[3:],cwd=argv[2])

    else:

        with open(settings["PROGRAM_PATH"]+"/que.txt",'a+',encoding='UTF-8') as f:

            f.write(dumps({
                "repo_path": argv[2],
                "sha": sha,
                "remote": remote,
                "remote_branch": branch,
            })+'|\n')

def get_arg(argument:str) -> str | None:

    return argv[argv.index(argument)+1] if argument in argv else None

def main() -> None:

    if argv[3] in HANDLED_COMMANDS:

        cmd_add(
            branch=get_arg("--branch"),
            commit=get_arg("--commit") or "HEAD",
            remote=get_arg("--remote") or "origin",
            priority=get_arg("--priority") or "normal",
        )

    else:

        run([settings["ORIGINAL_PATH"]]+argv[3:],cwd=argv[2])


if __name__ == "__main__":

    main()