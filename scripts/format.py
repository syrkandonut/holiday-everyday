import os
import subprocess
import sys

from black import main as black
from ruff.__main__ import find_ruff_bin


CHECK_FOLDERS = ("app",)

def main() -> None:
    ruff = find_ruff_bin()
    subprocess.run([os.fsdecode(ruff), "check", "--fix", *CHECK_FOLDERS])

    black.main(CHECK_FOLDERS)

if __name__ == "__main__":
    main()