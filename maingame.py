
import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
from Logicstate import size, black, white, background, width, height, TILESIZE, TILEMAP_W, TILEMAP_H, Camera, Player, Logicstate, COLORS, REALISTIC

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
    S = Logicstate(main_guy) # the darkness on the face of the deep
    
    worldmap_array = tmapc.creator('data/region-1.png')

    Tmap = np.transpose(worldmap_array) #access column (x) first, then row
    
    C = Camera()

    while True:

        screen.fill(background)
        
        S.event_listen()

        S.update_logic_state()
        
        C.DrawRender(screen, main_guy, Tmap[50:, 5:], photomode = COLORS)
                
        pygame.display.flip()
        clock.tick(framerate)
        
if __name__ == "__main__":
    main()
