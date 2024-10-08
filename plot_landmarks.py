#!/usr/bin/env python3

from Landmarks_module import Landmarks
import argparse
import os
import utils

def main():
    
    """
    Script to visualize landmarks on images. 
    Original images will not be override as new images will be generated. 
    """
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Script to visualize landmarks on images. Original images will not be override as new images will be generated. ') # Elaborate this description
    
    parser.add_argument('-f', '--input_file', required=True, 
                        help = '.xml or .txt file with annotated landmarks.')
    
    parser.add_argument('-i', '--input_dir', required=True, 
                        help='Input directory containing the reference images.')

    parser.add_argument('-o', '--output', 
                        help = "Output folder that will contain the new annotated images")
    
    parser.add_argument('--design', choices=['dots', 'numbers', 'combo'], default='dots', 
                        help = 'Choose design to plot the coordinates. Default is dots')
    
    args = parser.parse_args()
    
    inputfile = os.path.abspath(args.input_file)
    og_path = os.path.dirname(inputfile)
    basename = os.path.basename(inputfile)[1]
        
    if args.output:
        outfolder = os.path.abspath(args.output)
    else:
        outfolder = os.path.join(og_path, f'annotated_{basename}')
    
    
    utils.check_make_dir(outfolder)
    Landmarks.flip_dir = outfolder
    Landmarks.data_dir = os.path.abspath(args.input_dir)
    
    lm_data = Landmarks(inputfile, flip=False)
    
    
    
    lm_data.generate_images(args.design)
    
    

if __name__ == "__main__":
    main()  