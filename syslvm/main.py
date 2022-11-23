import subprocess


while True:
    key = input('P - Exit: ').lower()

    if key == 'q':
        break
    elif key == 'p':
        subprocess.run('pvs')

#if '__main__' == '__name__':

