#!/usr/bin/env python3

import argparse
import os

def write_tpsfile(folder, output, scale):
    
    """
    Write TPS like file to serve as input for predicting landmarks
    """

    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp'] 

    with open(output, 'w') as f:
        for file in os.listdir(folder):
            basename = os.path.basename(file)
            if os.path.splitext(basename)[-1] in image_extensions:
                image_id = os.path.splitext(basename)[0].upper()
                f.write(f'LM=0\n')
                f.write(f'IMAGE={basename}\n')
                f.write(f'ID={image_id}\n')
                f.write(f'SCALE={scale}\n')
    
                
def main():
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter, description= '')

    add = parser.add_argument

    add('-i','--image_dir', required=True, help='Directory containing images')
    add('--scale', required=True, help='Scale of all the images, all images must have the same scale')
    add('-o', '--output',  help="Name of the output file. Recommended extensions are .tps or .txt")

    args = parser.parse_args()

    folder = os.path.abspath(args.image_dir)
    scale = args.scale
    if args.output:
        output = args.output
    else:
        output = 'InputImagesFile.txt'
    
    write_tpsfile(folder, output, scale)
        
    
if __name__ == "__main__":
    main()          
            
    


# Arguments = directory with images, scale
# Hacer un main porque puede ser util llamarlo tambien desde el otro main

# 1. Read images in directory. Extensions jpg, png...
# 2. For each image create an entry in the file
# LM=0
# IMAGE=Fc1045ind1.jpg
# ID=FC1045IND1
# SCALE=0.000394
# LM=0