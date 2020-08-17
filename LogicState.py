import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
import time

size = width, height = 448, 256
black = 0, 0, 0
white = 255, 255, 255

background = 0, 140, 178

TILESIZE = 16
TILESIZE_X = TILESIZE
TILESIZE_Y = TILESIZE

PLAYERSIZE = 16
PLAYERSIZE_X = PLAYERSIZE
PLAYERSIZE_Y = PLAYERSIZE

PLAYER_OFFSET_X = PLAYERSIZE_X//2
PLAYER_OFFSET_Y = PLAYERSIZE_Y*7//9                                         #The proportional offset of the sprite's feet from the top-left corner of the sprite 

TILEMAP_W = width // TILESIZE_X + 2

TILEMAP_H = height // TILESIZE_Y + 2

MAP_TOTAL = (TILEMAP_W)*(TILEMAP_H)

DOWN, RIGHT, UP, LEFT= 0, 1, 2, 3
DOWNRIGHT, UPRIGHT, UPLEFT, DOWNLEFT= 4, 5, 6, 7

WATER, LAND, GRASS, SAND, ROCK, SHALLOWS, TREE, CLIFF = 0, 1, 2, 3, 4, 5, 6, 7

colors = {WATER:[50,50,200],
          LAND:[180, 180, 40],
          GRASS:[30, 150, 9],
          SAND:[233, 245, 100],
          ROCK:[150, 150, 150],
          SHALLOWS:[80, 60, 220],
          TREE:[93, 90, 0],
          CLIFF:[203, 150, 100]}

staminagreen = [85, 255, 5]
staminared = [255, 20, 40]

SQRT2 = 1.42
TWOPI = 6.28

ON_LAND, IN_WATER = 0, 1

walking_velocity = [[0, 1], [1, 0], [0, -1], [-1, 0], [SQRT2/2, SQRT2/2], [SQRT2/2, -SQRT2/2], [-SQRT2/2, -SQRT2/2], [-SQRT2/2, SQRT2/2]]
swimming_velocity = [[vel[0]*.7, vel[1]*.7] for vel in walking_velocity] 

sprite_f_name_list = lambda _list : [f'data/sprites/sprite-{i}-small.png' for i in _list]
player_anim_sprite = {DOWN: sprite_f_name_list([6, 7, 8, 7]),
                    RIGHT: sprite_f_name_list([3, 4, 5, 4]),
                    UP: sprite_f_name_list([0, 1, 2, 1]),
                    LEFT: sprite_f_name_list([9, 10, 11, 10])}

player_swim_sprite = {DOWN: 'data/sprites/sprite-6-swim.png',
                    RIGHT: 'data/sprites/sprite-3-swim.png',
                    UP: 'data/sprites/sprite-0-swim.png',
                    LEFT: 'data/sprites/sprite-10-swim.png'}

ANIMATION_SKIP_LEN = 5
WALKING_LOOP_LEN = 3

SLOW_ANIM_SKIP_LEN = 8
WATER_DANGER_ANIM_LEN = 4

WATER_ANIM_LOOP_LEN = 4

water_detail = [f"data/sprites/swim-detail-{i}.png" for i in range(WATER_ANIM_LOOP_LEN + 1)]

STAMINA_MAX = 100
STAMINA_DANGER = 40
STAM_FULL_DANGER = 25

STAM_DEPLETE_TIMING_LEN = 12

class Player():
    def __init__(self, world_coordinate = [width // 2, height // 2]):
        self.X = world_coordinate[0]
        self.Y = world_coordinate[1]

        self.U = self.X     #camera/screen coordinates
        self.V = self.Y

        self.cached_X = self.X
        self.cached_Y = self.Y
        
        self.alive = True
        self.screen_X = self.X
        self.screen_Y = self.Y
        self.velocity = [0,0]
        self.viewable = True
        self.mode = DOWN
        self.moving = None
        self.sprite = player_anim_sprite[self.mode][1]

        self.water_detail_texture = water_detail[WATER_ANIM_LOOP_LEN]
        
        self.walking_count = WALKING_LOOP_LEN
        self.walking_anim_wait = ANIMATION_SKIP_LEN
        
        self.detail_anim_counter = WATER_ANIM_LOOP_LEN
        self.detail_anim_wait = SLOW_ANIM_SKIP_LEN

        self.land_mode = ON_LAND

        self.Stamina = STAMINA_MAX
        self.stamina_frame_wait = STAM_DEPLETE_TIMING_LEN
                
    def update_movement(self):
        self.accelerate()
        self.update_position()

    def accelerate(self):
        if self.moving != None:
            if self.land_mode == ON_LAND:
                self.velocity = walking_velocity[self.moving]
            elif self.land_mode == IN_WATER:
                self.velocity = swimming_velocity[self.moving]
        else:
            if self.land_mode == ON_LAND:                
                self.velocity = [0,0]
                
            elif self.land_mode == IN_WATER:
                if not abs(self.velocity[0]) + abs(self.velocity[1]) < .02: 
                    self.velocity = [self.velocity[i]*.95 for i in range(2)]
                else:
                    self.velocity = [0,0]

    def update_position(self):
       #TODO: add boundaries so dude doesn't go off the map
        self.X += self.velocity[0]
        self.Y += self.velocity[1]

    def update_animation(self):

        if self.land_mode == ON_LAND:
            if self.moving != None:      
                self.walking_anim_wait -= 1
                if self.walking_anim_wait < 0:              
                    self.step_animation()                 
                    self.walking_anim_wait = ANIMATION_SKIP_LEN
            else:
                self.sprite = player_anim_sprite[self.mode][1]
                self.walking_count = WALKING_LOOP_LEN
                self.walking_anim_wait = ANIMATION_SKIP_LEN

                    
        elif self.land_mode == IN_WATER:
            self.sprite = player_swim_sprite[self.mode]                
            self.detail_anim_wait -= 1
            if self.detail_anim_wait < 0:
                self.detail_step_animation()
                if self.Stamina < STAM_FULL_DANGER:
                    self.detail_anim_wait = WATER_DANGER_ANIM_LEN
                else:
                    self.detail_anim_wait = SLOW_ANIM_SKIP_LEN
        
    def step_animation(self):        
        self.walking_count -= 1
        if self.walking_count < 0:
            self.walking_count = WALKING_LOOP_LEN

        self.sprite = player_anim_sprite[self.mode][self.walking_count]

    def detail_step_animation(self):        
        self.detail_anim_counter -= 1
        if self.detail_anim_counter < 0:
            self.detail_anim_counter = WATER_ANIM_LOOP_LEN
        self.water_detail_texture = water_detail[self.detail_anim_counter]

    def update_stamina(self):
        if self.land_mode == IN_WATER:
            self.deplete_stamina()          

        if self.land_mode == ON_LAND:
            if (self.Stamina < STAMINA_MAX):
                self.refill_stamina()
            
    def deplete_stamina(self):
        self.stamina_frame_wait -= 1
        if self.stamina_frame_wait < 0:
            self.Stamina -= 1
            self.stamina_frame_wait = STAM_DEPLETE_TIMING_LEN

    def refill_stamina(self):
        self.Stamina += 1

    def update_life_or_death(self):
        if (self.Stamina < 0):
            self.die()
        if self.alive == False:
            self.reset()

    def die(self):
        self.alive = False
        if self.land_mode == IN_WATER:      
            self.viewable = False
        
    def reset(self):
        self.X = self.cached_X
        self.Y = self.cached_Y

        self.U = self.X
        self.V = self.Y

        self.alive = True
        self.viewable = True
        self.Stamina = STAMINA_MAX

    def current_tile_index(self):
        
        index_x = (self.X + PLAYER_OFFSET_X )// TILESIZE_X
        index_y = (self.Y + PLAYER_OFFSET_Y )// TILESIZE_Y  #Our guy is actually not as big as his tilesize, so place the sensor approximately at his "feet"
                                                          # conveniently, the player's head will be at about the same position as his feet when he is swimming       
        return int(index_x), int(index_y)
        
        
class LogicState():
    #A state should have at least three methods: handle its own events, update the game world, and draw something different on the screen
    def __init__(self, Player, screen, Tilemap):
        
        self.Player = Player
        self.screen = screen
        self.Tilemap = Tilemap

        self.keyup = False
        self.Camera_Offset_X = self.Player.X - width //2
        self.Camera_Offset_Y = self.Player.Y - height//2

        self.Max_Camera_Offset_X = self.Tilemap.shape[0]*TILESIZE_X - width
        self.Max_Camera_Offset_Y = self.Tilemap.shape[1]*TILESIZE_Y - height

        self.Min_Camera_Offset_X = 0
        self.Min_Camera_Offset_Y = 0

       

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
        
        self.direction_listen(keys)
        
                
    def update_logic_state(self):
        active_tile_value = self.Tilemap[self.Player.current_tile_index()]
        if active_tile_value == WATER:          
            self.Player.land_mode = IN_WATER           
        else: self.Player.land_mode = ON_LAND

        self.Player.update_movement()
        self.Player.update_animation()
        self.Player.update_stamina()
        self.Player.update_life_or_death()

    def Draw(self):
        self.update_Camera_position()
        
        self.Render_Tilemap()

        self.Draw_Player()

    def grid_index(self, x, y):
        index_x = (x)// TILESIZE_X
        index_y = (y)// TILESIZE_Y

        return index_x, index_y

    def update_Camera_position(self):
        self.Camera_Offset_X = self.Player.X - width //2
        self.Camera_Offset_Y = self.Player.Y - height//2                                                #The camera follows the player by translating them to the center  

        self.camera_closest_grid_index = self.grid_index(self.Camera_Offset_X, self.Camera_Offset_Y)    #Find the place in the grid to start drawing tiles
                                                                                                        

        self.slicestart = self.camera_closest_grid_index[:]                                             #create a shallow copy to the grid index so we don't modify it
        self.slicestart = [max(self.slicestart[i], 0) for i in range(2)]                                #modify slicestart to be on the tilemap
        
        
        self.scanline_u = self.slicestart[0]*TILESIZE_X - self.Camera_Offset_X                          #If you think about this long enough, it makes sense          
        self.scanline_v = self.slicestart[1]*TILESIZE_Y - self.Camera_Offset_Y

        self.sliceend = []
        self.sliceend.append(self.slicestart[0] + TILEMAP_W)
        self.sliceend.append(self.slicestart[1] + TILEMAP_H)                                            #these slice indices might also go off the screen

        self.sliceend = [min(self.sliceend[i], self.Tilemap.shape[i]) for i in range(2)]                #the slice or end of the tilemap, whichever comes first

        self.viewport = self.Tilemap[int(self.slicestart[0]):int(self.sliceend[0]), int(self.slicestart[1]):int(self.sliceend[1])] #slice it
        
    
    def Render_Tilemap(self):
        
        for Left_start_col in self.viewport:
            for topmost_ID in Left_start_col:
                new_rect = pygame.Rect(self.scanline_u, self.scanline_v, TILESIZE_X, TILESIZE_Y)
                new_surface = pygame.draw.rect(self.screen, colors[topmost_ID], new_rect)
                    
                self.scanline_v += TILESIZE_Y               
                
            self.scanline_u += TILESIZE_X
            self.scanline_v = self.slicestart[1]*TILESIZE_Y - self.Camera_Offset_Y

            #vertical scan lines!
        
                
    def Draw_Player(self):
        if self.Player.viewable:
            if self.Player.land_mode == IN_WATER:
                water_detail_surface = pygame.image.load(self.Player.water_detail_texture)
                water_detail_surface = water_detail_surface.convert()
                colorkey = water_detail_surface.get_at((0,0))
                water_detail_surface.set_colorkey(colorkey, RLEACCEL)
            
                self.screen.blit(water_detail_surface, [self.Player.U, self.Player.V])

            if self.Player.Stamina < STAMINA_MAX:
                if self.Player.Stamina < STAM_FULL_DANGER:
                    pygame.draw.arc(self.screen, staminared, [self.Player.U - 15, self.Player.V - 12, 10, 10], TWOPI/5, (TWOPI/5 + self.Player.Stamina*TWOPI/100), 1)
                else:
                    pygame.draw.arc(self.screen, staminagreen, [self.Player.U - 15, self.Player.V - 12, 10, 10], TWOPI/5, (TWOPI/5 + self.Player.Stamina*TWOPI/100), 1)
        
        
            
            player_sprite_surface = pygame.image.load(self.Player.sprite)
            
            player_sprite_surface = player_sprite_surface.convert()
            colorkey = player_sprite_surface.get_at((0,0))
            player_sprite_surface.set_colorkey(colorkey, RLEACCEL)
            
            self.screen.blit(player_sprite_surface, [self.Player.U, self.Player.V])

    def direction_listen(self, keys):
        if keys[K_DOWN] or keys[ord('s')]:
            if keys[K_LEFT] or keys[ord('a')]:
                self.Player.mode = LEFT
                self.Player.moving = DOWNLEFT
                
            elif keys[K_RIGHT] or keys[ord('d')]:
                self.Player.mode = RIGHT
                self.Player.moving = DOWNRIGHT
                
            else:
                self.Player.mode = self.Player.moving = DOWN
                            
            
        elif keys[K_RIGHT] or keys[ord('d')]:
            if keys[K_UP] or keys[ord('w')]:
                self.Player.mode = RIGHT
                self.Player.moving = UPRIGHT
                
            else:
                self.Player.mode = self.Player.moving = RIGHT
                      
            
        elif keys[K_UP] or keys[ord('w')]:
            if keys[K_LEFT] or keys[ord('a')]:
                self.Player.mode = LEFT
                self.Player.moving = UPLEFT
                
            else:
                self.Player.mode = self.Player.moving = UP

        elif keys[K_LEFT] or keys[ord('a')]:
            self.Player.mode = self.Player.moving = LEFT
            

        if not keys[K_LEFT] and not keys[K_UP] and not keys[K_RIGHT] and not keys[K_DOWN]:
            if not keys[ord('s')] and not keys[ord('d')] and not keys[ord('w')] and not keys[ord('a')]:
                self.Player.moving = None


def main():
    pass
if __name__ == "__main__":
    main()
