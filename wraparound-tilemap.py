"""
Some good good pygame credit to https://www.pygame.org/docs/tut/ChimpLineByLine.html
"""

import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image

import tilemap_creator as tmpc

size = width, height = 448, 256
black = 0, 0, 0
white = 255, 255, 255

x_pixels = 16
y_pixels = 16

Tiles_Max_X = width // x_pixels + 1
Tiles_Max_Y = height // y_pixels + 1

background = np.random.randint(255),np.random.randint(255),np.random.randint(255)
texture_farm = {0:"/water-plain-small.jpg",
                1:"/sand-texture-small.jpg"}

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
unused classes
"""

class Anchor():
    """There is one Anchor that is the center of the coordinate map we will use"""
    def __init__(self):
        self.coordinate = 0,0,0

class SkyBox():
    def __init__(self, Anchor, radius):
        self.Anchor = Anchor
        self.radius = radius
        

"""
Objects
"""

class Camera():
##    Hint:
##    Camera has coordinates and axes.
##    Camera should always point at the Anchor which stays at (0,0,0), and grounds the player and tilemap
##    If the Camera moves too far, it will no longer point at Anchor
##    The X- and Y- axes of Camera and Film coords are inverted from the Pixel Coords (top-left origin),
##    and the Z-axis is the optical axis
##    f is the focal distance from the viewing plane (film coords (x, y, f))
##   

    def __init__(self, coordinate = [0,0,0]):
        self.coordinate = coordinate

    def capture(self, globe, guy):
        try:
            self.coordinate_update(guy.velocity)
        except:
            pass
        globe.view(screen, [0,0], self.coordinate[:2])
        guy.view(screen, self.coordinate[:2])

    def coordinate_update(self, velocity):
        self.coordinate[0] -= velocity[0]
        self.coordinate[1] -= velocity[1]
        

    
class TileNode: 
    def __init__(self, down=None, right=None, up=None, left=None, ID=None, tile_position=None): 
        self.down = down # reference to down node in MLL 
        self.right = right
        self.up = up
        self.left = left
        
        self.ID = ID

class Tile():
    def __init__(self):
        '''model'''
        self.data = TileNode()
        '''view'''
        #color: texture or animation of textures
        '''control'''
        #collision components
        pass 

class Player():
    def __init__(self, coordinate = [0,0,0]):
        self.position = coordinate
        self.orientation = 0
        #zero orientation is down, 1 is right, 2 is up, 3 is left
        self.sprite_sheet = ["data/sprite-6-small.png", "data/sprite-5-small.png", "data/sprite-0-small.png", "data/sprite-9-small.png"]

        self.sprite = 'data/sprite-7-small.png'
        
    def view(self, screen, camera_coordinate):
        self.position[0] -= camera_coordinate[0]
        self.position[1] -= camera_coordinate[1] ##you are flagrantly misusing model and view representation here
        self.screen = screen
        fname = self.sprite
        new_surface = pygame.image.load(fname)
        new_surface = new_surface.convert()
        colorkey = new_surface.get_at((0,0))
        new_surface.set_colorkey(colorkey, RLEACCEL)
        
        self.screen.blit(new_surface, self.position[:2])

    def move(self, orientation=None):
        self.orientation = orientation
        self.velocity, self.sprite = self.from_orientation(self.orientation)
        self.update_position(self.velocity)      
        
    def from_orientation(self, orientation = None):
        
        velocity = [[0,1],[1,0],[0,-1],[-1,0]] #down, right, up, left

        if self.orientation is not None:
            return velocity[orientation], self.sprite_sheet[orientation]
        else: return [0,0], 'data/sprite-7-small.png'

    def update_position(self, velocity = None):
        self.position[0] += 0#self.velocity[0]
        self.position[1] += 0#self.velocity[1]
        
        
    
        
        
    
class Globe():
    """
    This will contain the whole ass world
    """
    def __init__(self, tilemap):
        self.Globe_Width = min(Tiles_Max_Y, tilemap.shape[0])
        self.Globe_Height = min(Tiles_Max_X, tilemap.shape[1])
        
        self.tilemap = tilemap

        self.raw_bytes_dict = {}
        
    def view(self, screen, origin = [0,0], camera_coordinate = [0,0]):          #origin tells where to start reading at the tilemap
        self.screen = screen
        self.drawing_head = camera_coordinate      

        self.set_viewable_tiles(origin)

        self.create_viewing_window(camera_coordinate)
        
    def set_viewable_tiles(self, origin):
        self.viewable_tiles = self.tilemap[origin[1]:origin[1] + self.Globe_Height, origin[0]:origin[0] + self.Globe_Width] # this is awful and confusing but too bad!

    def create_viewing_window(self, camera_coordinate = [0,0]):
        for row in self.viewable_tiles:
            for ID in row:
                if ID not in self.raw_bytes_dict:
                    image = Image.open('data' + texture_farm[ID])
                    self.raw_bytes_dict[ID] = (image.tobytes(), image.size, image.mode)
                new_surface = pygame.image.fromstring(*self.raw_bytes_dict[ID])
                self.screen.blit(new_surface, self.drawing_head)
                self.drawing_head[0] += x_pixels
            self.drawing_head[0] = camera_coordinate[0]
            self.drawing_head[1] += y_pixels

##    def update_viewing_model(self, Min_x = 0, Min_y = 0):
##        for j in range(self.Globe_Height):
##            for i in range(self.Globe_Width):
##                ## lol I still don't know whow to keep these indices straight
##                ## we should do the tilemap multiple-pointer method here to keep track of shifting camera movements and keep everything on the screen
            
     
"""
Run-once code
"""
def setup():
    pygame.init()
    tilemap = tmpc.creator()
    g = Globe(tilemap) # creates model for game environment
    main_guy = Player([width // 2, height //2, 0])
    g.view(screen)
    c = Camera()

    
    return g, main_guy, c
    
"""
Main Loop
"""
def handleEvents(interactiveVector = None):
    main_guy = interactiveVector[0]
    keyup= False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitted = True
            quit()
            pygame.quit()
            return

        if event.type == pygame.KEYUP:
            keyup = True
        
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] or keys[ord('s')]:
        main_guy.move(0)
    if keys[K_RIGHT] or keys[ord('d')]:
        main_guy.move(1)
    if keys[K_UP] or keys[ord('w')]:
        main_guy.move(2)
    if keys[K_LEFT] or keys[ord('a')]:
        main_guy.move(3)

    if keyup:
        main_guy.velocity = [0, 0]

    

    
            
            
        
def main():
    g, main_guy, c = setup()
    quitted = False
    while not quitted:
        
        handleEvents([main_guy])

        screen.fill(background)

        c.capture(g, main_guy)
        
        pygame.display.flip()

        clock.tick(framerate)        

        
if __name__ == "__main__":
    main()


