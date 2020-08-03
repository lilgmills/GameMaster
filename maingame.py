
import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
from Logicstate import size, black, white, background, width, height, TILESIZE, TILEMAP_W, TILEMAP_H, Player, Logicstate, COLORS, REALISTIC

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

    Tmap = np.transpose(worldmap_array) #access column (x) first, then row

    State = Logicstate(main_guy, Tmap)

    while True:

        screen.fill(background)
        
        State.event_listen()

        State.update_logic_state()
        
        State.DrawRender(screen)
                
        pygame.display.flip()
        clock.tick(framerate)
        
if __name__ == "__main__":
    main()
