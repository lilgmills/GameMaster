"""TileMap creator"""
"""Trying different patterns for painting tile maps"""
import numpy as np
from PIL import Image
def creator(fname):
    image = Image.open(fname)
    data = np.asarray(image)
    
    data_dict = {}
    ID = 0
    j = 0
    i = 0
    for row in data:
        for point in row:
            if not str(point) in data_dict:
                data_dict[str(point)] = ID
                ID+=1
                with open("codes.txt", "a+") as f:
                    f.write(f"{ID}, {str(point)}")            
        
    tilemap = [[data_dict[str(point)] for point in data[i]] for i in range(data.shape[0])]

    return np.asarray(tilemap)

def read_tilemap(fname, TESTWIDTH, TESTHEIGHT):  #works with a csv created from a png
        with open (fname, 'r') as f:
            lines = f.readlines()
            tilemap_IDs_Data = [row.split(',')[:-1] for row in lines]

        tilemap_IDs_testcrop = tilemap_IDs_Data[:TESTHEIGHT][:TESTWIDTH]
        
        return tilemap_IDs_testcrop

def main():
    creator()
    
if __name__ == "__main__":
    main()
    
