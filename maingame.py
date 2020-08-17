
import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
from LogicState import size, black, white, background, width, height, TILESIZE, TILEMAP_W, TILEMAP_H, Player, LogicState

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
        
            
def main():
    pygame.init()

    main_guy = Player()    
        
    worldmap_array = tmapc.creator('data/region-1.png')
    worldmap_array = worldmap_array[1:] #remove colorcode row at the top

    Tmap = np.transpose(worldmap_array) #access column (x) first, then row

    State = LogicState(main_guy, screen, Tmap) # the darkness on the face of the deep
    
    while True:

        screen.fill(background)
        
        State.event_listen()

        State.update_logic_state()
        
        State.Draw()
                
        pygame.display.flip()
        
        clock.tick(framerate)
        
if __name__ == "__main__":
    main()
