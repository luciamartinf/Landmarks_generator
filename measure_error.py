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





def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Predict test landmarks using the model and evaluate its performance by calculating the error.') 
    
    parser.add_argument('-f', '--input_file', required=True, 
                        help = 'Reference _.tps_/_.xml_ file that contains landmarks')
    
    parser.add_argument('-i', '--input_dir', required = True,
                        help = 'Input directory containing the images')
    
    parser.add_argument('-m', '--model', required=True,
                        help = ".dat file path of the model.")
    
    # TODO generate .tps prediction from xml_file =  output, only if output flag is on 
        
    args = parser.parse_args()
    
    xml = os.path.abspath(args.input_file)
    dat = os.path.abspath(args.model)
    work_dir = os.path.dirname(dat)
    
    # Check that the model exist
    dat = utils.check_predmodel(dat, work_dir, parser)
    
    Landmarks.data_dir = args.input_dir
    Landmarks.create_flipdir()
    
    set = Landmarks(xml) # img_list y lm_dict
    
    mean_mre = set.calculate_error(dat)

    shapepred_fun.measure_mae(dat, xml)
    
    # Deleting flip_images from work_data path
    utils.delete_files(Landmarks.flip_dir)


if __name__ == "__main__":
    main()  