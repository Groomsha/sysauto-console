import subprocess


if __name__ == '__main__':
    while True:
        key = input('P - Exit: ').lower()

        if key == 'q':
            break
        elif key == 'p':
            password = input("Please enter your password: ")
            p = subprocess.Popen('ls'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate(password.encode())

            print(p.returncode)
            print(p.stdout)

