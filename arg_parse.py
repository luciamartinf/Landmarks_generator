#!/usr/bin/env python3

import argparse

def get_train_parser():
    
    """Parser for train"""
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')
    
    add = parser.add_argument
    
    add('--version', action='version', version='%(prog)s 0.0.1')
    
    add('--verbose', action='store_true', help='Enable verbose mode')

    add('-i', '--image_dir', required=True, 
        help='Input directory containing the images for training.')
    
    add( '-f', '--file', required = True,
        help = '.tps/.txt/.xml file with image names and their previously annotated landmarks.')
    
    add('-m', '--model_name', required=True,
        help='Name of the model (without extension).') 

    
    add('--model_version', '-mv', required=False, type=int,
        help='Version of the model. If the version already exists, next available version will be generated.')
    
    add('--work_dir','-w', default='./', 
        help='Define working directory. By default it takes the current directory.')
    
    add('--params', '-p', help = ' .txt file that contains already defined hyperparameters for training the model.')
    
    add('--save_params', '-sp', action='store_true', 
        help = "Save best found hyperparameters params in a new .txt file")
    
    return parser


def get_predict_parser():
    
    """"Parser for prediction"""
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')
    
    add = parser.add_argument
    
    add('--version', action='version', version='%(prog)s 0.0.1')
    
    add('--verbose', action='store_true', help='Enable verbose mode')

    add('-i', '--image_dir', required=True, 
        help='Input directory containing the images for predicting.')
    
    add('-m', '--model', required=True,
        help='.dat file path of the LandmarkGen model') 
    
    add( '-f', '--file',
        help = '.tps/.txt file with image names, scales and ID but no landmarks annotated. Required if scale is not defined.')
    
    add('-s', '--scale', 
        help = 'Scale of all the images, all images must have the same scale.')
    
    add('--work_dir','-w', default='./', 
        help='Define working directory. By default it takes the current directory')
    
    add('--output', '-o',
        help = " Name of the output .tps/.txt file that will contain all predicted landmarks.")
    
    # add('--plot', action='store_true', 
    #     help = "Plot landmarks on images.")
    
    add('--plot', type=str, choices = ['none', 'dots', 'numbers'], default='none',
        help = "Plot landmarks on images with desired design. See README for full description of designs")
    
    return parser