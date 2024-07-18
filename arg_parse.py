#!/usr/bin/env python3

import argparse

def add_common_arguments(subparser):
    
    add = subparser.add_argument
    
    add('-img', '--image_dir', required=True, 
        help='Directory containing the images')
    
    add('-m', '--model_name', required=True,  # Deberia ser true para todos pero no para preprocess
        help='Model name')
    
    add('--model_version', '-mv', required=False, type=int,
        help='Model version')
    
    add('--work_dir','-w', default='./', # podria ser './' por defecto
        help='Working directory')
    


def get_parser():

    """
    Function to collect arguments from command line using argparse
    """

    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')

    add = parser.add_argument
    
    add('--version', action='version', version='%(prog)s 0.0.1')
    
    
    subparsers = parser.add_subparsers(dest='mode',
                                       help='Available modes')
    
    # Only train mode
    train_parser = subparsers.add_parser('train', help="Train model")
    add_common_arguments(train_parser)
    train_parser.add_argument( '-f', '--file', 
          help = 'Tps or txt file with image scale and landmarks')
    train_parser.add_argument( '--xml', # '--file', '-f',
                              # '-f', '--file',
        help = "Xml files for training the model when skipping preprocessing")
    train_parser.add_argument('--params', 
                              help = 'Params for training model')
    
    
    
    # Preprocess and train
    protrain_parser = subparsers.add_parser('protrain', help="Preprocess data and train model")
    add_common_arguments(protrain_parser)
    protrain_parser.add_argument( '-f', '--file', required = True,
        help = 'Tps or txt file with image scale and landmarks')
    protrain_parser.add_argument('--params', 
                              help = 'Params for training model')
   
    
    # Predict mode
    predict_parser = subparsers.add_parser('predict', help="Predict Landmarks with model")
    add_common_arguments(predict_parser)
    predict_parser.add_argument( '-f', '--file',
                                help = 'Tps or txt file with image scale')
    predict_parser.add_argument('-s', '--scale', 
                                help = 'Scale of all the images, all images must have the same scale')

    
    # All mode

    return parser, train_parser, predict_parser, protrain_parser

def parse_args():
    parser = get_parser()
    return parser.parse_args()