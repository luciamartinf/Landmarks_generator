#!/usr/bin/env python3

import config
import utils
import sys
import os
import multiprocessing
import arg_parse
from Landmarks_module import Landmarks
from Generate_model import find_best_params, train_model, measure_model_error


def preprocessing(lmfile, image_dir):
    
    """Preprocessing steps for training 
        
    Returns:
        train_xml (str): xml file for training
        test_xml (str): xml file for testing
    """
    
    Landmarks.data_dir = os.path.abspath(image_dir)
    Landmarks.create_flipdir()
    input_data = Landmarks(lmfile)
    train_xml, test_xml = input_data.split_data(split_size=[0.8,0.2])
    
    return train_xml, test_xml


def train(
    model_name, image_dir, train_xml, work_dir, model_version, 
    params = False, save_params = False): 
    
    """Training shape predictor model
    
    Returns:
        dat (str): shape predictor model
    """
    
    procs = multiprocessing.cpu_count()
    procs = config.PROCS if config.PROCS > 0 else procs 
    
    # check if dat file already exists and create the appropiate version
    dat = utils.check_trainmodel(model_name, work_dir, model_version)
    
    if not Landmarks.data_dir :
        Landmarks.data_dir = image_dir
        
    Landmarks.create_flipdir() # Only creates flip_dir if it doesn't exist 
    
    work_data = Landmarks.flip_dir
    train_set = Landmarks(train_xml, img_list=[]) # Check if i need something else here and if this works 
    
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
    
    parser = arg_parse.get_train_parser()
    
    # Reading arguments
    args = parser.parse_args()

    image_dir = os.path.abspath(args.image_dir)
    work_dir = os.path.abspath(args.work_dir)
    Landmarks.work_dir = work_dir

    model_name = args.model_name

    if args.model_version:
        model_version = int(args.model_version)
    else:
        model_version = 0
    
    input_file = args.file
    
    ext = utils.what_file_type(input_file)
    
    if ext in ['.tps', '.txt']:
        
        if Landmarks.check_forlm(input_file):
                print(".TPS file with landmarks detected.")
                
        else: 
            sys.stderr.write("\nERROR: TPS file detected without landmarks. Unable to proceed with training\n")
            parser.print_help()
            sys.exit(2)
                
    elif ext == '.xml':
        
        print(".xml file detected")
   
    else:
        
        sys.stderr.write("\nERROR: No input file found. Unable to proceed with training\n")
        parser.print_help()
        sys.exit(2)
    

    if args.params:
        params = utils.read_list_from_file(args.params)
    else:
        params = False
  
    try: 
        
        train_xml, test_xml = preprocessing(input_file, image_dir)
        dat = train(model_name, image_dir, train_xml, work_dir, model_version, params=params, save_params=args.save_params) 
    
    except:
        
        sys.stderr.write(f"\nERROR: Unable to train model with file {input_file}\n")
        parser.print_help()
        sys.exit(2)
    
    # Compute training and test MSE errors of the model
    print("Calculating MSE error of the model")
    measure_model_error(dat, train_xml) # aqui usar train + val
    measure_model_error(dat, test_xml) # aqui usar solo test
    
    print("Done!")
        
if __name__ == "__main__":
    main()  