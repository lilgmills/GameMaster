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


TILESIZE = 8
TILESIZE_X = TILESIZE
TILESIZE_Y = 5

TILEMAP_W = width // TILESIZE_X + 1

TILEMAP_H = height // TILESIZE_Y + 1

MAP_TOTAL = (TILEMAP_W)*(TILEMAP_H)

COLORS, REALISTIC = 1, 2

DOWN, RIGHT, UP, LEFT, DOWNRIGHT, UPRIGHT, UPLEFT, DOWNLEFT= 0, 1, 2, 3, 4, 5, 6, 7

texture_f_name_list = lambda _list : [f'data/sprites/sprite-{i}-small.png' for i in _list]

WATER, LAND, SAND, GRASS = 0, 1, 2, 3

colors = [[0,0,150], [180, 180, 40],  [233, 245, 100], [00, 180, 39],]

SQRT2 = 1.42


player_anim_sprite = {DOWN: texture_f_name_list([6, 7, 8, 7]),
                    RIGHT: texture_f_name_list([3, 4, 5, 4]),
                    UP: texture_f_name_list([0, 1, 2, 1]),
                    LEFT: texture_f_name_list([9, 10, 11, 10]),
                    }

walking_velocity = [[0, 1], [1, 0], [0, -1], [-1, 0], [SQRT2/2, SQRT2/2], [SQRT2/2, -SQRT2/2], [-SQRT2/2, -SQRT2/2], [-SQRT2/2, SQRT2/2]]

WALKING_LOOP_LENGTH = 3
ANIMATION_SKIP_LENGTH = 5

class Player():
    def __init__(self, world_coordinate = [width // 2, height // 2]):
        self.X = world_coordinate[0]
        self.Y = world_coordinate[1]
        self.velocity = [0,0]
        self.viewable = True
        self.mode = DOWN
        self.walking = None
        self.sprite = player_anim_sprite[self.mode][1]
        self.walking_count = WALKING_LOOP_LENGTH
                

    def step_animation(self):
        
        self.walking_count -= 1
        if self.walking_count < 0:
            self.walking_count = WALKING_LOOP_LENGTH

        self.sprite = player_anim_sprite[self.mode][self.walking_count]

    def accelerate(self):
        self.velocity = walking_velocity[self.walking]
        print(self.velocity)

    def update_position(self):
        self.X += self.velocity[0]
        self.Y += self.velocity[1]
        
            
        

class LogicState():
    #A state should have at least three methods: handle its own events, update the game world, and draw something different on the screen
    def __init__(self, Player, screen, Tilemap):
        
        self.Player = Player
        self.screen = screen
        self.Tilemap = Tilemap

        self.keyup = False

        self.time_walk = 5

    """
    Main Loop
    """
    def event_listen(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                quit()
                pygame.quit()

            if event.type == pygame.KEYUP:
                self.keyup = True
            else:
                self.keyup = False
            
        keys = pygame.key.get_pressed()
            
        if keys[K_DOWN] or keys[ord('s')]:
            if keys[K_LEFT] or keys[ord('a')]:
                self.Player.mode = LEFT
                self.Player.walking = DOWNLEFT
                
            elif keys[K_RIGHT] or keys[ord('d')]:
                self.Player.mode = DOWN
                self.Player.walking = DOWNRIGHT
                
            else:
                self.Player.mode = self.Player.walking = DOWN
                            
            
        elif keys[K_RIGHT] or keys[ord('d')]:
            if keys[K_UP] or keys[ord('w')]:
                self.Player.mode = RIGHT
                self.Player.walking = UPRIGHT
                
            else:
                self.Player.mode = self.Player.walking = RIGHT
                      
            
        elif keys[K_UP] or keys[ord('w')]:
            if keys[K_LEFT] or keys[ord('a')]:
                self.Player.mode = UP
                self.Player.walking = UPLEFT
                
            else:
                self.Player.mode = self.Player.walking = UP

        elif keys[K_LEFT] or keys[ord('a')]:
            self.Player.mode = self.Player.walking = LEFT
            

        if not keys[K_LEFT] and not keys[K_UP] and not keys[K_RIGHT] and not keys[K_DOWN]:
            if not keys[ord('s')] and not keys[ord('d')] and not keys[ord('w')] and not keys[ord('a')]:
                self.Player.walking = None
            

        
    def update_logic_state(self):

        
        
        if self.Player.walking != None:
            self.time_walk -= 1
            if self.time_walk < 0:
                
                self.Player.step_animation()
                    
                self.time_walk = 5

                
            self.Player.accelerate()
            self.Player.update_position()
            

        else:
            self.Player.sprite = player_anim_sprite[self.Player.mode][1]
            self.Player.velocity = [0,0]
            

    def Draw(self):
        temp_draw_Tilemap = self.Resize_Tilemap_to_window()
        
        self.Render_Tilemap(temp_draw_Tilemap)          

        self.Draw_Player()
        
    def Render_Tilemap(self, temp_draw_Tilemap = [[1,0,1],[0,1,0],[1,0,1]], photomode = COLORS):

        screen_offset_x = 0
        screen_offset_y = 0
        for Left_start_col in temp_draw_Tilemap:
            for topmost_ID in Left_start_col:
                if photomode == REALISTIC:
                    new_surface = pygame.image.load(textures[topmost_ID][1])
                    self.screen.blit(new_surface, [screen_offset_x, screen_offset_y])
                if photomode == COLORS:
                    new_rect = pygame.Rect(screen_offset_x, screen_offset_y, TILESIZE_X, TILESIZE_Y)
                    new_surface = pygame.draw.rect(self.screen, colors[topmost_ID], new_rect)
                    
                screen_offset_y += TILESIZE_Y
                
            screen_offset_x += TILESIZE_X
            screen_offset_y = 0

             #vertical scan lines!
                
    def Draw_Player(self):
        if self.Player.viewable:
            new_surface = pygame.image.load(self.Player.sprite)
            new_surface = new_surface.convert()
            colorkey = new_surface.get_at((0,0))
            new_surface.set_colorkey(colorkey, RLEACCEL)
            
            self.screen.blit(new_surface, [self.Player.X, self.Player.Y])

    def Resize_Tilemap_to_window(self):
        if self.Tilemap.shape[0] > TILEMAP_W or self.Tilemap.shape[1] > TILEMAP_H:
            temp_draw_Tilemap = self.Tilemap[:TILEMAP_W, :TILEMAP_H]
            
        else: temp_draw_Tilemap = Tilemap
        return temp_draw_Tilemap
    
    
def main():
    pass
if __name__ == "__main__":
    main()
