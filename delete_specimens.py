#!/usr/bin/env python3

import argparse
import os
import utils
from Landmarks_module import Landmarks

def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Predict and measure the error of a model') # Elaborate this description
    
    parser.add_argument('-f', '--file', required=True, 
                        help = '.xml or .txt file that contain landmarks')
    
    parser.add_argument('-l', '--list', required=True,
                        help = ".txt file that contains list of speciments to delete")
    
    parser.add_argument('-o', '--output', 
                        help = "Output file that will contain the reorganized landmarks in .tps")
    
    args = parser.parse_args()
    
    filepath = os.path.abspath(args.file)
    
    folder = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    
    if args.output:
        outfile = os.path.abspath(args.output)
    else:
        outfile = f'clean_{basename}'
        
    outpath = os.path.join(folder,outfile)

    list_file = os.path.abspath(args.list)
    
    del_list = utils.read_list_from_file(list_file, f=False)
    
    input = Landmarks(filepath, flip = False)
    
    clean_dict = input.del_items(del_list)
    
    for img, lm_list in clean_dict.items():
        
        input.append_to_tps(img, lm_list, outpath)
    
    
if __name__ == "__main__":
    main()  