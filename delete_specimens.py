#!/usr/bin/env python3

import argparse
import os
import utils
from Landmarks_module import Landmarks

def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Delete specimens from .tps file') # Elaborate this description
    
    parser.add_argument('-f', '--input_file', required=True, 
                        help = 'Reference .tps file')
    
    parser.add_argument('-l', '--input_list', required=True,
                        help = ".txt file that contains list of specimens to delete")
    
    parser.add_argument('-o', '--output', 
                        help = "Name of the output .tps file")
    
    args = parser.parse_args()
    
    filepath = os.path.abspath(args.input_file)
    
    folder = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    
    if args.output:
        outfile = os.path.abspath(args.output)
    else:
        outfile = f'clean_{basename}'
        
    outpath = os.path.join(folder,outfile)

    list_file = os.path.abspath(args.input_list)
    
    del_list = utils.read_list_from_file(list_file, f=False)
    
    input = Landmarks(filepath, flip = False)
    
    clean_dict = input.del_items(del_list)
    
    for img, lm_list in clean_dict.items():
        
        input.append_to_tps(img, lm_list, outpath)
    
    
if __name__ == "__main__":
    main()  