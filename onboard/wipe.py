import os


def wipedir(directory):
    for item in os.listdir(directory):
        try:
            os.remove(directory + '/' + item)
        except Exception as e:
            wipedir(directory + '/' + item)
    os.rmdir(directory)


def clear():
    if 'program' in os.listdir():
        wipedir('program')

clear()
