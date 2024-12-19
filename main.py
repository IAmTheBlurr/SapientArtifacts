""" Main file that will be used to run the program. """
from modules import TargetVideo

if __name__ == '__main__':
    target = TargetVideo('dQw4w9WgXcQ', 'super-special-video')
    target.download_captions()
