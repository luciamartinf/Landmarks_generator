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
    
    """
    This script is used to evaluate the performance of a trained model. 
    It takes as input a manually generated .tps file and generates landmarks with the trained model. 
    It then compares the manual and the automatic landmarks to calculate the mean relative error (MRE) and the mean absolute error (MAE) that are included on the standard output.
    """
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= 'Evaluate the performance of a trained model') 
    
    parser.add_argument('-f', '--input_file', required=True, 
                        help = 'Path to the input .tps file containing manually annotated landmarks.')
    
    parser.add_argument('-i', '--input_dir', required = True,
                        help = 'Path to the input directory containing the reference images. ')
    
    parser.add_argument('-m', '--model', required=True,
                        help = "Path to the target trained model")
    
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