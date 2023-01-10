import os
import subprocess
from typing import Dict
from elevate import elevate

from lvm_menu import LVM_menu


def is_root() -> None:
    if os.getuid() != 0:
        elevate(graphical=False)

def cmd_command(command:str) -> Dict:
    cmd = subprocess.run(command.split(), shell=True, encoding='utf-8',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    return {'returncode': cmd.returncode,
            'stdout': cmd.stdout,
            'stderr': cmd.stderr}


if __name__ == '__main__':
    cmd_menu = LVM_menu()
    current_menu = cmd_menu.main_menu()

    # is_root()

    while True:
        subprocess.run(['clear'], shell=True)
        print('Utility for Fast Configuration of LVM v0.3')

        key = input(f"{current_menu}\nPlease Select Menu: ").lower()

        match key:
            case 'p': current_menu = cmd_menu.physical_menu()
            case 'l': current_menu = cmd_menu.logical_menu()
            case 'r': current_menu = cmd_menu.main_menu()
            case 'q': break
