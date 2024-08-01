#!/usr/bin/env python3

import argparse


def get_parser():

    """Define arguments and modes using argparse

    Returns:
        parser (argparse.ArgumentParser): main parser
        train_parser (argparse.ArgumentParser): train mode parser
        predict_parser (argparse.ArgumentParser): predict mode parser
    """

    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')
    subparsers = parser.add_subparsers(dest='mode',
                                       help='Available modes')
    
    add = parser.add_argument
    
    add('--version', action='version', version='%(prog)s 0.0.1')
    
    add('--verbose', action='store_true', help='Enable verbose mode')

    add('-img', '--image_dir', required=True, 
        help='Directory containing the images')
    
    add('-m', '--model_name', required=True,
        help='Model name')
    
    add('--model_version', '-mv', required=False, type=int,
        help='Model version')
    
    add('--work_dir','-w', default='./', 
        help='Working directory')
    

    # Train mode
    
    train_parser = subparsers.add_parser('train', help="Train model")
    
    train_parser.add_argument( '-f', '--file', required = True,
          help = 'Tps, txt or xml file with image scale and landmarks')
    
    train_parser.add_argument('--params', 
                              help = 'Params for training model')
    
    train_parser.add_argument('--save_params', '-s', action='store_true', 
                              help = "Save training params in a new file")
    
   
    
    # Predict mode
    
    predict_parser = subparsers.add_parser('predict', help="Predict Landmarks with model")
    
    predict_parser.add_argument( '-f', '--file',
                                help = 'Tps or txt file with image scale')
    
    predict_parser.add_argument('-s', '--scale', 
                                help = 'Scale of all the images, all images must have the same scale')
    
    predict_parser.add_argument('--output', '-o',
                                help = "Output tps file that contains landmarks")
    
    predict_parser.add_argument('--plot', action='store_true', 
                              help = "Plot images with landmarks")

    
    # Return all modes
    
    return parser, train_parser, predict_parser
