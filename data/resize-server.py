from PIL import Image
from os import getcwd, listdir

import numpy as np

def resize(fname):
    start, ending = fname.split(".")
    if ending == "py": pass
    else:    
        im = Image.open(fname)
        width, height = im.size
        
        if width > 16 or height > 16:
            
            newsize = (16, 16)            
            im1 = im.resize(newsize)
            name = (f"{start}-small", ending)
            im1.save(".".join(name))

def image_slice(name, num_rows, num_cols):
    im = Image.open(name)
    data = np.asarray(im)

    M = data.size[0] // n_rows
    N = data.size[1] // n_cols

    tiles = [data[x:x+M,y:y+N] for x in range(0,data.shape[0],M) for y in range(0,data.shape[1],N)]

    tiles = np.asarray(tiles)

    for i in range(tiles.shape[0]):
        im2 = Image.fromarray(tiles[i])
        im2.save(f"sprite-{i}.png")
        

def main():
    img_dir = getcwd()

    for i in range(12):
        resize(f"sprite-{i}.png")

    
        

if __name__ == "__main__":
    main()
