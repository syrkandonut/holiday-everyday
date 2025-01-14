import os 
import subprocess
import sys

from black import main as black
from mypy import main as mypy
from ruff.__main__ import find_ruff_bin

CHECK_FOLDERS = ("app",)


def main() -> None:
    ruff = find_ruff_bin()
    subprocess.run([os.fsdecode(ruff), "check", *CHECK_FOLDERS])

    black.main([*CHECK_FOLDERS, "--check"],  standalone_mode=False)

    mypy.main(
        stdout=sys.stdout,
        stderr=sys.stderr,
        args=[*CHECK_FOLDERS],
        clean_exit=True,
    )

if __name__ == "__main__":
    main()