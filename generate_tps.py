#!/usr/bin/env python3

import argparse
import os

def write_tpsfile(folder, output, scale):
    
    """
    Write TPS like file to serve as input for predicting landmarks
    """

    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'] 

    with open(output, 'a') as f:
        for file in os.listdir(folder):
            basename = os.path.basename(file)
            if os.path.splitext(basename)[-1] in image_extensions:
                image_id = os.path.splitext(basename)[0].upper()
                f.write(f'LM=0\n')
                f.write(f'IMAGE={basename}\n')
                f.write(f'ID={image_id}\n')
                if scale:
                    f.write(f'SCALE={scale}\n')

    return output
    
                
def main():
    
    """
    This script generates a landmarks-empty .tps file with all the images in a directory. 
    This is a .tps file with LM=0 and ID, IMAGE and SCALE features
    """
    
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'This script generates a landmarks-empty .tps file with all the images in a directory.')

    add = parser.add_argument

    add('-i','--input_dir', required=True, 
        help='Path to the input directory containing the target images')
    
    add('--scale', # required=True, 
        help='Specify the scale of the images in the input directory. All images must have the same scale.')
    
    add('-o', '--output',  
        help= 'Name of the output .tps file.')

    args = parser.parse_args()

    folder = os.path.abspath(args.input_dir)
    folder_name = os.path.basename(folder)
    
    if args.scale: 
        scale = args.scale
    else: 
        print("\nWARNING: No input scale was specified")
        scale=False
    
    if args.output:
        output = args.output
    else:
        output = f'{folder_name}.tps'
    
    write_tpsfile(folder, output, scale)
        
    
if __name__ == "__main__":
    main()          
            
    


