#!/usr/bin/env python3

import argparse

def get_train_parser():
    
    """Parser for train"""
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= 'Train a model with landmark-annotated images')
    
    add = parser.add_argument
    
    add('--version', action='version', version='%(prog)s 0.0.1')
    
    add('--verbose', action='store_true', help='Enable verbose mode')
    
    add( '-f', '--input_file', required = True,
        help = 'Path to the input .tps or .xml file with annotated landmarks')

    add('-i', '--input_dir', required=True, 
        help='Path to the input directory containing the training images')
    
    add('-m', '--model', required=True,
        help='Basename for output model file (without extension)') 

    add('--model_version', required=False, type=int,
        help='Define version of the model manually')
    
    add('--output_dir', default='./', 
        help='Specify where output files will be written')
    
    add('--params', help = 'Path to a .txt file containing predefined hyperparameters for training the model')
    
    add('--save_params', action='store_true', 
        help = "Save optimized hyperparameters in a new .txt file")
    
    return parser


def get_predict_parser():
    
    """"Parser for prediction"""
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= 'Extract fixed landmarks from images using a trained model')
    
    add = parser.add_argument
    
    add('--version', action='version', version='%(prog)s 0.0.1')
    
    add('--verbose', action='store_true', help='Enable verbose mode')

    add('-i', '--input_dir', required=True, 
        help='Input directory containing the target images')
    
    add('-m', '--model', required=True,
        help='Path to the trained model') 
    
    add('-s', '--scale', 
        help = 'Specify an uniform scale for all images in the input directory. All images must have the same scale')
    
    add( '-f', '--input_file',
        help = 'Provide a reference landmarks-empty .tps file.')
    
    add('--output_dir', default='./', 
        help='Specify where output files will be written')
    
    add('--output_file',
        help = " Name of the output .tps/.txt file that will contain all predicted landmarks.")
    
    # add('--plot', action='store_true', 
    #     help = "Plot landmarks on images.")
    
    add('--plot', type=str, choices = ['none', 'dots', 'numbers', 'combo'], default='none',
        help = "Option to visualize landmarks on images. See README for full description of designs")
    
    return parser