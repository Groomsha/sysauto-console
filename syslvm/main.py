import subprocess


if __name__ == '__main__':
    while True:
        key = input('P - Exit: ').lower()

        if key == 'q':
            break
        elif key == 'p':
            subprocess.run('pvs')
