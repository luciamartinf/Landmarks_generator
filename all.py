#!/usr/bin/env python3

from Generate_model import find_best_params, train_model, measure_model_error
from utils import check_dir, check_for_xml_files
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


parser, train_parser, predict_parser, protrain_parser = arg_parse.get_parser()
args = parser.parse_args()
# args = arg_parse.parse_args()

work_dir = os.path.abspath(args.work_dir)

image_dir = os.path.abspath(args.image_dir)

model_name = args.model_name
if args.model_version:
    model_version = int(args.model_version)
else:
    model_version = 0

mode = args.mode


if args.mode == 'train':
    
    if not args.xml: # en lugar de esto puede ser --file 
        
        # Another check trying to look for xml file
        print("WARNING: No xml file found")
        if args.file:
            lm_file = args.file
            if utils.what_file_type(lm_file) in ['.txt','.tps']:
                
                if Landmarks.check_forlm(args.file):
                    # protrain mode
                    print("TPS file detected, using protrain mode =  preprocessing + training ")
                    mode = 'protrain'
                    # lm_path = os.path.join(work_dir, lm_file) # check that this is the correct way of doing this
                    # train_xml, test_xml = preprocessing(lm_path, image_dir)
                    # dat = train(model_name, image_dir, train_xml, work_dir, model_version)
                    
                    
                else: 
                    print("WARNING: TPS file detected without landmarks. Trying predicting mode...")
                    dat = utils.check_predmodel(model_name, work_dir, model_version) 
                    mode = 'predict'
                    
            else:
                print("INSTRUCTION: Try using the -xml XML_FILE or --file TPS_FILE to enter preprocessing mode with a tps file")
                train_parser.print_help()
                sys.exit(1)
        else:
            print("INSTRUCTION: Try using the -xml XML_FILE or --file TPS_FILE to enter preprocessing mode with a tps file")
            parser.print_help()
            sys.exit(1)
            
        
    else:
        xml_file = args.xml
        print(utils.what_file_type(xml_file))
        if utils.what_file_type(xml_file) == '.xml':
            # Warning sobre si este xml es solo train o es todo el xml file
            # Puedo hacer una funcion para MERGE dos xml files que sean iguales
            # split xml file into train and test
            train_xml, test_xml = preprocessing(os.path.abspath(xml_file), image_dir)
            dat = train(model_name, image_dir, train_xml, work_dir, model_version)
        else:
            print(f"ERROR: Unable to train model with file {xml_file}")
            sys.exit(1)


# MEASURE ERROR OF MODEL

if mode == 'protrain':
    
    print('preprocess and train')
    
    # Check that this file tiene landmarks
    
    landmarks_file = args.file
    lm_path = os.path.join(work_dir, landmarks_file) # check that this is the correct way of doing this
    train_xml, test_xml = preprocessing(lm_path, image_dir)
        
    dat = train(model_name, image_dir, train_xml, work_dir, model_version)
    
    # MEASURE ERROR OF MODEL
    
    
if mode == 'predict':
    
    
    # Check that the model exist
    dat = utils.check_predmodel(model_name, work_dir, model_version)
    
    # Check that we can create a new tps file
    if not args.scale:
        print("ERROR: Please introduce scale")
    
    generate_tps.write_tpsfile(image_dir, 'input.tps', scale = args.scale)
    
    print('predicting')
    

    

## MEASURE ERROR

# if mode == 'train':
#     print(args.mode)
    
#     # Compute training and test MSE errors of the model
#     measure_model_error(dat, train_xml) # aqui usar train + val
#     measure_model_error(dat, test_xml) # aqui usar solo test
    
#     # input_data.check_for_negatives(dat)
    
   
    
    










