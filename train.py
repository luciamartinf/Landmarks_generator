#!/usr/bin/env python3

import argparse
from Generate_model import find_best_params, train_model, measure_model_error
from utils import check_dir, check_for_xml_files
from Landmarks_module import Landmarks
import os
import multiprocessing
import utils
import generate_tps

import config
from preprocess import preprocessing


def train(model, image_dir, train_xml): # train_set is an object of Landmarks
    
    Landmarks.data_dir = image_dir
    Landmarks.create_flipdir()
    work_dir = Landmarks.flip_dir
    train_set = Landmarks(train_xml) # Check if i need something else here and if this works 
    
    # temp model
    temp = os.path.join(work_dir, 'temp.dat')
    # Find best parameters
    # aqui usar train para entrenar y val para testear
    best_params = find_best_params(train_set, temp)
    # Train model
    
    dat = os.path.join(work_dir, f'{model}.dat')
    # Check for file 
    # utils.check_file(dat)
    train_model(dat, train_xml, best_params)
    
    return dat
    
    

def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter, description= '')

    add = parser.add_argument

    add('-i','--image_dir', required=True, 
        help='Directory containing images')
    add('-o', '--model_name', required=True, 
        help = "Model name")
    add('-f', '--file', 
        help = 'Tps or txt file with image scale and landmarks.') # If not file as input, we need an scale
    add('--scale',
        help='Scale of all the images, all images must have the same scale')
    
    add('--preprocess', '-p', action='store_true',
        help='Preprocessing data and create train and test sets') # Change this help message
    add('--xml',
        help = "Required if preprocess flag is on. Xml file for training the model")
    

    args = parser.parse_args()

    
    procs = multiprocessing.cpu_count()
    procs = config.PROCS if config.PROCS > 0 else procs 
    
    image_dir = os.path.abspath(args.image_dir)
    lm_file = os.path.abspath(args.file)
    model_name = args.model_name
    
    if args.preprocess:
        train_xml = args.xml
        
    else:
        if args.file:
            print("TRUE")
            lm_file = os.path.abspath(args.file)
        else:
            lm_file = 'tps_file.txt'
            try:
                scale = args.scale
            except: 
                # Print introduce scale
                scale = str(0) # Default scale
            
            generate_tps.write_tpsfile(image_dir, lm_file, scale)
    
    
        train_xml, test_xml = preprocessing(image_dir, lm_file)
    
    model = train(model_name, image_dir, train_xml)
    
if __name__ == "__main__":
    main()          
            
    
    
    
    
    
    
    