import os
import subprocess
from elevate import elevate


def is_root():
        if os.getuid() != 0:
            elevate()

if __name__ == '__main__':
    is_root()

    # while True:
    #     key = input('P - Exit: ').lower()

    #     if key == 'q':
    #         break
    #     elif key == 'p':
    #         pass
    #         # password = input("Please enter your password: ")
            # p = subprocess.Popen('ls'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # p.communicate(password.encode())

            # print(p.returncode)
            # print(p.stdout)
