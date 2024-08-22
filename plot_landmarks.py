#!/usr/bin/env python3

from Landmarks_module import Landmarks
import argparse
import os
import utils

def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Plot landmarks') # Elaborate this description
    
    parser.add_argument('-f', '--file', required=True, 
                        help = '.xml or .txt file that contains landmarks')
    
    parser.add_argument('-i', '--image_dir', required=True, 
                        help='Input directory containing the reference images.')

    parser.add_argument('-o', '--output', 
                        help = "Output folder that will contain the new annotated images")
    
    parser.add_argument('-d', '--design', choices=['dots', 'numbers'], default='dots', 
                        help = 'Choice design of points. Default is dots')
    
    args = parser.parse_args()
    
    inputfile = os.path.abspath(args.file)
    og_path = os.path.dirname(inputfile)
    basename = os.path.basename(inputfile)[1]
        
    if args.output:
        outfolder = os.path.abspath(args.output)
    else:
        outfolder = os.path.join(og_path, f'annotated_{basename}')
    
    
    utils.check_make_dir(outfolder)
    Landmarks.flip_dir = outfolder
    Landmarks.data_dir = os.path.abspath(args.image_dir)
    
    lm_data = Landmarks(inputfile, flip=False)
    
    
    
    lm_data.generate_images(args.design)
    
    

if __name__ == "__main__":
    main()  