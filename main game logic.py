"""
Some good good pygame credit to https://www.pygame.org/docs/tut/ChimpLineByLine.html
"""

import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
from Logicstate import *

import tilemap_creator as tmapc

screen = pygame.display.set_mode(size)
"""
set display mode (with openGL rendering, if desired)
"""


clock = pygame.time.Clock()
framerate = 60
"""
set framerate below with clock.tick
"""

if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

def load_image(name, colorkey=None): #colorkey sets the transparent color for the image
    fullname = os.path.join('data', name) #in this example all the resources are in a 'data' subdirectory
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


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

"""
Objects
"""

class Camera():
    def __init__(self, world_coordinate = [0,0]):
        self.world_coordinate = world_coordinate #the camera will be required to stay on the globe 
        self.velocity = [0,0]   
        
    def coordinate_update(self, velocity):
        self.coordinate[0] += velocity[0]
        self.coordinate[1] += velocity[1]

    def draw_colored_tiles(self, viewable_tile_flat):
        pass

    def capture(self, Globe):        #camera coordinate tells where to start reading at the tilemap       
        self.drawing_head = []
        self.color_header = {}
        
class tilemap():    
    def __init__(self, fname):
        self.tilemap_IDs_atlas = np.asarray(self.read_tilemap(fname))
        
        self.size = self.global_width, self.global_height = self.get_size()
        self.linear_index = self.get_viewable_tiles_linear_index()
        
    def get_size(self):
        size = len(self.tilemap_IDs_atlas[0]), len(self.tilemap_IDs_atlas)
        
        return size

    def read_tilemap(self, fname, TESTWIDTH = 30, TESTHEIGHT = 30):  #works with a csv created from a png
        with open (fname, 'r') as f:
            lines = f.readlines()
            tilemap_IDs_Data = [row.split(',')[:-1] for row in lines]

        tilemap_IDs_testcrop = tilemap_IDs_Data[:TESTHEIGHT][:TESTWIDTH]
        
        return tilemap_IDs_testcrop

    def get_viewable_tiles_linear_index(self, world_coord_at_top_left = [0,0]):
        linear_index = []

        i = world_coord_at_top_left[1]
        j = world_coord_at_top_left[0]

        Max_Tile_Y = min((i + TILEMAP_H), self.global_height)
        Max_Tile_X = min((j + TILEMAP_W), self.global_width)
        
        while i < Max_Tile_Y:
            while j < Max_Tile_X:
                linear_index.append(self.global_height * i + j)
                j += 1
            i+=1
            j=world_coord_at_top_left[0]

        print("length of linear index:", len(linear_index))
        return linear_index
        
class Player():
    def __init__(self, Globe):
        self.position = [width // 2, height // 2] #dont confuse world coords and camera coords
        self.orientation = 0
        #zero orientation is down, 1 is right, 2 is up, 3 is left
        
        self.sprite_sheet = ["data/sprite-6-small.png", "data/sprite-5-small.png", "data/sprite-0-small.png", "data/sprite-9-small.png"]

        self.sprite = 'data/sprite-6-small-underwater.png'
        self.velocity = [0,0]

        self.velocity_dict = {}
        
    def view(self):        
        new_surface = pygame.image.load(self.sprite)
        new_surface = new_surface.convert()
        colorkey = new_surface.get_at((0,0))
        new_surface.set_colorkey(colorkey, RLEACCEL)
        
        screen.blit(new_surface, self.position[:2])
        
        
class Ocean():
    def __init__(self):
        pass

    def animate(self):
        pass
            
class Globe():
    """
    This will contain the whole ass world
    """
    def __init__(self, Tilemap):
        self.ocean = Ocean()

    
def main():
    pygame.init()
    
    S = Logicstate() # the darkness on the face of the deep
    
    T = tilemap('tilemap.csv') 
    
    G = Globe(T)

    main_guy = Player(G)

    C = Camera()
    
    while True:

        screen.fill(background)
        S.handleEvents()
        S.update_events(G)
        
        C.capture(G)
                
        pygame.display.flip()
        clock.tick(framerate)
        
if __name__ == "__main__":
    main()
