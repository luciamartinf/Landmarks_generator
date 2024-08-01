#!/usr/bin/env python3

import argparse
from Generate_model import find_best_params, train_model
from Landmarks_module import Landmarks
import os
import multiprocessing
import generate_tps
import config
import utils

def preprocessing(lmfile, image_dir):
    
    """Preprocessing steps for training 
    
    Parameters:
        lmfile (str): tps, xml or txt file with annotated landmarks
        image_dir (str): Directory that contains images
        
    Returns:
        train_xml (str): xml file for training
        test_xml (str): xml file for testing
    """
    
    Landmarks.data_dir = os.path.abspath(image_dir)
    Landmarks.create_flipdir()
    input_data = Landmarks(lmfile)
    train_xml, test_xml = input_data.split_data()
    
    return train_xml, test_xml


def train(model_name, image_dir, train_xml, work_dir, model_version, params = False, save_params = False): # train_set is an object of Landmarks
    
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
    
    
    if params:
        # Get parameters from file
        print(f"Using parameters from file {params}")
        best_params = params
    else:
        # Find best parameters
        best_params = find_best_params(train_set, temp)
        
    if save_params:
        params_file = f"params_{model_name}.txt"
        utils.write_list_to_file(best_params, params_file)
        print(f"Saving best parameters to {params_file}")
    
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
    
    print(f"COMPLETE: {model} has been generated") # lo de complete no me gusta


if __name__ == "__main__":
    main()          
            
    
    
    
    
    
    
    