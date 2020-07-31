"""
Some good good pygame credit to https://www.pygame.org/docs/tut/ChimpLineByLine.html
"""

import sys, os
import pygame
from pygame.locals import *

size = width, height = 448, 256
black = 0, 0, 0


screen = pygame.display.set_mode(size)
pygame.display.set_caption('pygame game')
"""
set display mode (with openGL rendering if desired)
"""

if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

def load_image(name, colorkey=None): #colorkey sets the transparent color for the image
    fullname = os.path.join('data', name) #in this example all the resources are in a 'data' subdirectory
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound



    
class Anchor():
    """There is one Anchor that is the center of the coordinate map we will use"""
    def __init__(self):
        self.coordinate = [0,0,0]

class SkyBox():
    def __init__(self, Anchor, radius):
        self.Anchor = Anchor
        self.radius = radius

class Player():
    def __init__(self):
        self.coordinate = [0,0,0]
        self.orientation = 0

class Camera():
    def __init__self(self, coordinate):
        self.coordinate = [0,0,0]


def main():
    pygame.init()
    load_image('cloud-image.png')

if __name__ == "__main__":
    main()


