

from dotenv import load_dotenv
from sys import argv
from os import getenv
from subprocess import run

load_dotenv()

REGULAR_GIT = getenv("REGULAR_GIT_PATH")
HANDLED_COMMANDS = [
    "commit",
    "push"
]

def main() -> None:

    if argv[1] in HANDLED_COMMANDS:

        with open("que.txt",'a+') as f:

            f.write(" ".join(argv[1:])+"\n")

    else:

        print(run(
            [REGULAR_GIT]+argv[1:],
            check=True
        ))


if __name__ == "__main__":

    main()