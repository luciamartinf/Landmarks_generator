#!/usr/bin/env python3

#### # !/usr/bin/python3 # comprobar que esto no esta en ninguno

import numpy as np
import os
import dlib

import shapepred_fun
import argparse
from Landmarks_module import Landmarks
import utils


# TODO: complete this functions with notebook
# Calculate mean relative error and other types, mean standard deviation ...


# generate .tps prediction from xml_file =  output, only if output flag is on 


def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Predict and measure the error of a model') # Elaborate this description
    
    parser.add_argument('-f', '--file', required=True, 
                        help = '.xml or .txt file that contains real landmarks')
    
    parser.add_argument('-i', '--image_dir', required = True,
                        help = 'Input directory containing the images')
    
    parser.add_argument('-m', '--model', required=True,
                        help = ".dat file path of the LandmarkGen model.")
    
    parser.add_argument('-o', '--output', 
                        help = "Output file that will contain predicted landmarks in .tps")
        
    args = parser.parse_args()
    
    xml = os.path.abspath(args.file)
    dat = os.path.abspath(args.model)
    
    Landmarks.data_dir = args.image_dir
    Landmarks.create_flipdir()
    
    set = Landmarks(xml) # img_list y lm_dict
    mean_mre = set.calculate_error(dat)

    shapepred_fun.measure_mae(dat, xml)
    
    # Deleting flip_images from work_data path
    utils.delete_files(Landmarks.flip_dir)


if __name__ == "__main__":
    main()  