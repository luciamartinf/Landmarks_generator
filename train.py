#!/usr/bin/env python3

import sys
import os
import multiprocessing
import arg_parse
import config
import utils
from Landmarks_module import Landmarks
from cv import find_best_params, train_model, measure_mse
import time


def preprocessing(lmfile, image_dir):
    
    """Preprocessing steps for training 
        
    Returns:
        train_xml (str): xml file for training
        test_xml (str): xml file for testing
    """
    
    Landmarks.data_dir = os.path.abspath(image_dir)
    Landmarks.create_flipdir()
    input_data = Landmarks(lmfile)
    full_xml_name = os.path.join(Landmarks.work_dir, "all_data.xml")
    full_xml = input_data.write_xml(full_xml_name, 'all_data')
    train_xml, test_xml = input_data.split_data(split_size=[0.75,0.25])
    
    return train_xml, test_xml, full_xml


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
    
    if params:
        # Get parameters from file
        print(f"Using parameters from file {params}")
        best_params = params
    else:
        train_set = Landmarks(train_xml) # Check if i need something else here and if this works 
        # temp model
        temp = os.path.join(work_data, 'temp.dat')
        # Find best parameters
        best_params = find_best_params(train_set, temp)
        
    if save_params:
        params_file = os.join.path(Landmarks.work_dir, f"params_{model_name}.txt")
        utils.write_list_to_file(best_params, params_file)
        print(f"Saving best parameters to {params_file}")
    
    # Train model
    train_model(dat, train_xml, best_params)
    
    return dat, best_params
    

def main():
    
    start_time = time.time()
    
    parser = arg_parse.get_train_parser()
    
    # Reading arguments
    args = parser.parse_args()

    image_dir = os.path.abspath(args.input_dir)
    work_dir = os.path.abspath(args.output_dir)
    Landmarks.work_dir = work_dir

    model_name = args.model

    if args.model_version:
        model_version = int(args.model_version)
    else:
        model_version = 0
    
    input_file = args.input_file
    
    ext = utils.what_file_type(input_file)
    
    if ext in ['.tps', '.txt']:
        
        if Landmarks.check_forlm(input_file):
                print(".tps/.txt file with landmarks detected.")
                
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
    
    train_xml, test_xml, full_xml = preprocessing(input_file, image_dir)
    
    # Train model to get performance
    oos_dat, best_params = train('oos_temp', image_dir, train_xml, work_dir, model_version, params=params, save_params=False) 
    
    
    # Train final model with all data
    final_dat, final_params = train(model_name, image_dir, full_xml, work_dir, model_version, params=best_params, save_params=args.save_params)
    
    model_size = os.path.getsize(final_dat) / 1024
    
    # try: 
        
    #     train_xml, test_xml, full_xml = preprocessing(input_file, image_dir)
    #     oos_dat = train(model_name, image_dir, train_xml, work_dir, model_version, params=params, save_params=args.save_params) 
    
    # except:
        
    #     sys.stderr.write(f"\nERROR: Unable to train model with file {input_file}\n")
    #     parser.print_help()
    #     sys.exit(2)
    
    
    # Compute training and test errors of the model
    print("Calculating Errors of the model")
    
    train_set = Landmarks(train_xml)
    train_set.calculate_error(oos_dat, train_xml)
    measure_mse(oos_dat, train_xml) 
    
    test_set = Landmarks(test_xml)
    test_set.calculate_error(oos_dat, test_xml)
    # measure_mse(oos_dat, test_xml) 
    
    # This is just useful for me
    # full_set = Landmarks(full_xml)
    # full_set.calculate_error(oos_dat)
    # measure_mse(oos_dat, full_xml) 
    
    
    
    # Deleting flip_images from work_data path
    utils.delete_files(Landmarks.flip_dir)
    # Deleting work_data directory
    Landmarks.del_flipdir()
    # Delete oos_model
    os.remove(oos_dat)
    end_time = time.time()
    print("Done!")
    
    total_time = end_time - start_time
    print(f"Total time: {total_time}")
    print(f"Final model size: {model_size}GB")
        
if __name__ == "__main__":
    main()  