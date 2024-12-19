""" Main file that will be used to run the program. """
from modules import TargetVideo

if __name__ == '__main__':
    target = TargetVideo('piJkuavhV50', 'four_d_geometry_sadness')
    target.download_captions()
