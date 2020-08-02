import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image

size = width, height = 448, 256
black = 0, 0, 0
white = 255, 255, 255

background = 0, 140, 178

TILESIZE = TILESIZE_X, TILESIZE_Y = 120, 120

TILEMAP_W = width // TILESIZE_X

TILEMAP_H = height // TILESIZE_Y

class Event():
    def __init__(self, condition):
        self.condition = condition

    def EventFuntion():
        print("a simple event")
        

class Logicstate():
    #A state should have at least three methods: handle its own events, update the game world, and draw something different on the screen
    def __init__(self):
        self.origin = [0,0]

        self.Events = {'keyup': Event(False),'keydown': Event(False)}

    """
    Main Loop
    """
    def handleEvents(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                quit()
                pygame.quit()

            if event.type == pygame.KEYUP:
                self.Events['keyup'].condition = True

            if event.type == pygame.KEYDOWN:
                self.Events['keydown'].condition = True        
            
        keys = pygame.key.get_pressed()
            
        if keys[K_DOWN] or keys[ord('s')]:
            pass
        if keys[K_RIGHT] or keys[ord('d')]:
            pass
        if keys[K_UP] or keys[ord('w')]:
            pass
        if keys[K_LEFT] or keys[ord('a')]:
            pass

        
    def ResetEvent(self, Event):
        Event.EventFunction()
        Event.condition = False

    def update_events(self, Globe):
        for event_key in self.Events:
            event_handle = self.Events[event_key] 
            if event_handle.condition:
                self.ResetEvent(event_handle)
        

def main():
    pass
if __name__ == "__main__":
    main()
