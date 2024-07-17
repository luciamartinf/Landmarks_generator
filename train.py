#!/usr/bin/env python3

import argparse
from Generate_model import find_best_params, train_model
from Landmarks_module import Landmarks
import os
import multiprocessing
import generate_tps
import config
from preprocess import preprocessing
import utils


def train(model_name, image_dir, train_xml, work_dir, model_version): # train_set is an object of Landmarks
    
    procs = multiprocessing.cpu_count()
    procs = config.PROCS if config.PROCS > 0 else procs 
    
    # check if dat file already exists and create the appropiate version
    dat = utils.check_trainmodel(model_name, work_dir, model_version)
    
    if not Landmarks.data_dir :
        Landmarks.data_dir = image_dir
        
    Landmarks.create_flipdir() # Only creates flip_dir if it doesn't exist 
    
    work_data = Landmarks.flip_dir
    train_set = Landmarks(train_xml) # Check if i need something else here and if this works 
    
    # temp model
    temp = os.path.join(work_data, 'temp.dat')
    
    # Find best parameters
    best_params = find_best_params(train_set, temp)
    
    # Train model
    train_model(dat, train_xml, best_params)
    
    
    
    return dat
    
    

def main():
    
    # Este main lo tengo que modificar
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter, description= '')

    add = parser.add_argument

    add('-i','--image_dir', required=True, 
        help='Directory containing images')
    add('-o', '--model_name', required=True, 
        help="Model name")
    add('-f', '--file', 
        help = 'Tps or txt file with image scale and landmarks.') # Para entrenar necesito si o si las landmarks
    # add('--scale',
    #     help='Scale of all the images, all images must have the same scale')
    
    add('--preprocess', '-p', action='store_true',
        help='Preprocessing data and create train and test sets') # Change this help message
    add('--xml',
        help = "Required if preprocess flag is on. Xml file for training the model")
    

    args = parser.parse_args()

    
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
            
    
    
    
    
    
    
    