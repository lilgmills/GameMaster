"""TileMap creator"""
"""Trying different patterns for painting tile maps"""
import numpy as np

def creator():
    tiles_x = 28
    tiles_y = 16

    row_of_ocean = [0 for _ in range(tiles_x)]
    start = 5
    length = 5
    row_of_island = [0 for _ in range(start)] + [1 for _ in range(length)] + [0 for _ in range(start + length, tiles_x)]

    tmpland = [row_of_ocean for _ in range(start)] + [row_of_island for _ in range(length)] + [row_of_ocean for _ in range(start + length, tiles_y) ]
    
    data = np.asarray(tmpland)
    print (data)

    return data

def main():
    creator()
    
if __name__ == "__main__":
    main()
    
