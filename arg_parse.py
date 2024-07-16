#!/usr/bin/env python3

import argparse

def get_parser():

    """
    Function to collect arguments from command line using argparse
    """

    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')

    add = parser.add_argument

    # add('--mode', type=str, choices=['train', 'predict'], default='train',
    #     help = "Mode of using")

    add('-img', '--image_dir', required=True, help='Directory containing the images')
    
    add('-m', '--model_name', required=True,  # Deberia ser true para todos pero no para preprocess
        help='Model name')
        
    add( '-f', '--file',
        help = 'Tps or txt file with image scale and landmarks')
    
    add('--work_dir','-w', default='./', # podria ser './' por defecto
        help='Working directory')
    
    add('--model_version', '-mv', required=False, 
        help='Model version')
    
    
    # add('--version', action='version', version='%(prog)s 0.0.1')

    add('--preprocess', '-p', action='store_true',
        help='Preprocessing data and create train and test sets')

    return parser

def parse_args():
    parser = get_parser()
    return parser.parse_args()