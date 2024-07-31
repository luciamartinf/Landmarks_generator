#!/usr/bin/env python3

from Generate_model import  measure_model_error
from utils import  what_file_type
from Landmarks_module import Landmarks
import os
import multiprocessing
import utils
import generate_tps
import config

from preprocess import preprocessing
from train import train
import arg_parse
import random
import sys


random.seed(5399) # Always same splits
# With the same number of max_func_calls deberia de obtener el mismo resultado no? 

#######################
### PARSE ARGUMENTS ###
#######################


parser, train_parser, predict_parser = arg_parse.get_parser()
args = parser.parse_args()
# args = arg_parse.parse_args()


image_dir = os.path.abspath(args.image_dir)
work_dir = os.path.abspath(args.work_dir)



model_name = args.model_name
if args.model_version:
    model_version = int(args.model_version)
else:
    model_version = 0

mode = args.mode

if not mode:
    sys.stderr.write("\nERROR: Please specify an executing mode\n")
    parser.print_help()
    print()
    train_parser.print_help()
    print()
    predict_parser.print_help()
    sys.exit(2)
    
    
    
if mode == 'train':
    
    input_file = os.path.join(work_dir, args.file) # TODO: hacer esto en todos los files
    
    ext = what_file_type(args.file)
    
    if ext in ['.tps', '.txt']:
        
        if Landmarks.check_forlm(args.file):
                print(".TPS file with landmarks detected.")
                
        else: 
            print("WARNING: TPS file detected without landmarks. Trying predicting mode...")
            # If it doesn't work it will exit
            dat = utils.check_predmodel(model_name, work_dir, model_version, parser) 
            mode = 'predict'
                
    elif ext == '.xml':
        
        print(".xml file detected")
   
    else:
        
        sys.stderr.write("\nERROR: No input file found. Unable to proceed in train mode\n")
        sys.stderr.write("\nINSTRUCTION: Try -xml XML_FILE to continue in train mode or --file TPS_FILE to enter preprocessing mode with a tps file\n")
        parser.print_help()
        train_parser.print_help()
        sys.exit(2)
    
    print('Train mode activated')
    

    if args.params:
        params = utils.read_list_from_file(args.params)
    else:
        params = False
    
    train_xml, test_xml = preprocessing(os.path.abspath(input_file), image_dir)
    dat = train(model_name, image_dir, train_xml, work_dir, model_version, params=params, save_params=args.save_params)
        
    try: 
        train_xml, test_xml = preprocessing(os.path.abspath(input_file), image_dir)
        dat = train(model_name, image_dir, train_xml, work_dir, model_version, params=params, save_params=args.save_params) 
    except:
        sys.stderr.write(f"\nERROR: Unable to train model with file {args.file}\n")
        parser.print_help()
        train_parser.print_help()
        sys.exit(2)
    
    # Compute training and test MSE errors of the model
    measure_model_error(dat, train_xml) # aqui usar train + val
    measure_model_error(dat, test_xml) # aqui usar solo test
    
    # input_data.check_for_negatives(dat)



if mode == 'predict':
    
    print('Predict mode activated')
    
    # Check that the model exist
    dat = utils.check_predmodel(model_name, work_dir, model_version, parser)
    
    if args.file:
        
        if what_file_type(args.file) not in ['.txt', '.tps']:
            
            if not args.scale:
                sys.stderr.print("\nERROR: Invalid input file and no scale specified. Unable to proceed in predict mode\n")
                predict_parser.print_help()
                sys.exit(2)
            
            else:
                print("\nWARNING: Invalid input file, but scale was specified.")
                print("Generating a new tps file with specified scale.")
                tpsfile = generate_tps.write_tpsfile(image_dir, 'input_images.tps', scale=args.scale)
        
        elif Landmarks.check_forlm(args.file):
            print("WARNING: This file already contains annotated landmarks")
            tpsfile = args.file
        
        else:
            
            tpsfile = args.file 
    
    elif args.scale:
        # If not tpsfile Check that we can create a tps file
        tpsfile = generate_tps.write_tpsfile(image_dir, 'input_images.tps', scale = args.scale)
    
    else:
        sys.stderr.print("\nERROR: No input file and no scale specified. Unable to proceed in predict mode\n")
        predict_parser.print_help()
        sys.exit(2)
    
    ## TODO: Call predict functions

    


    
   
    
    










