#!/usr/bin/env python3

from Generate_model import find_best_params, train_model, measure_model_error
from utils import check_dir, check_for_xml_files, what_file_type
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
    sys.exit(2)
    
if mode == 'train':
    
    if not args.xml: # en lugar de esto puede ser --file y luego intentar averiguar el tipo de archivo que es en el codigo con la extension
        
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
                    dat = utils.check_predmodel(model_name, work_dir, model_version, parser) 
                    mode = 'predict'
                    
            else:
                # DUDA: Es esto un standard error?
                sys.stderr.write("\nERROR: No input file found. Unable to proceed in train mode\n")
                sys.stderr.write("\nINSTRUCTION: Try -xml XML_FILE to continue in train mode or --file TPS_FILE to enter preprocessing mode with a tps file\n")
                train_parser.print_help()
                protrain_parser.print_help()
                sys.exit(2)
        else:
            sys.stderr.write("\nERROR: No input file found. Unable to proceed in train mode\n")
            sys.stderr.write("\nINSTRUCTION: Try -xml XML_FILE to continue in train mode or --file TPS_FILE to enter preprocessing mode with a tps file\n")
            train_parser.print_help()
            protrain_parser.print_help()
            sys.exit(2)
            
        
    else:
        xml_file = args.xml
        print(utils.what_file_type(xml_file))
        if utils.what_file_type(xml_file) == '.xml':
            # # Warning sobre si este xml es solo train o es todo el xml file
            # # Puedo hacer una funcion para MERGE dos xml files que sean iguales
            # split xml file into train and test
            print("Activating train mode")
            train_xml, test_xml = preprocessing(os.path.abspath(xml_file), image_dir)
            dat = train(model_name, image_dir, train_xml, work_dir, model_version)
        
        else:
            sys.stderr.write(f"\nERROR: Unable to train model with file {xml_file}\n")
            train_parser.print_help()
            sys.exit(2)


if mode == 'protrain':
    
    landmarks_file = args.file
    lm_path = os.path.join(work_dir, landmarks_file) # TODO: hacer esto en todos los files
    
    if utils.what_file_type(lm_path) in ['.tps', '.txt']:
    
        if Landmarks.check_forlm(lm_path):
        
            print('Protrain mode activated')
            print('Processing now...')
            train_xml, test_xml = preprocessing(lm_path, image_dir)
            print('Starting training...')
            dat = train(model_name, image_dir, train_xml, work_dir, model_version)
        
        else:
            sys.stderr.write("WARNING: TPS file detected without landmarks. Trying predicting mode...")
            # If this fails it will exit 
            dat = utils.check_predmodel(model_name, work_dir, model_version, parser) 
            mode = 'predict'
    else:
        sys.stderr.write(f"\nERROR: Unable to train model with file {args.file}\n")
        protrain_parser.print_help()
        sys.exit(2)
        
        
    
    
## MEASURE ERROR

if mode in ['train', 'protrain']:
    
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
    
    else:
        # If not tpsfile Check that we can create a tps file
        if not args.scale:
            sys.stderr.print("\nERROR: No input file and no scale specified. Unable to proceed in predict mode\n")
            predict_parser.print_help()
            sys.exit(2)
        else:
            tpsfile = generate_tps.write_tpsfile(image_dir, 'input_images.tps', scale = args.scale)
    
    
    

    


    
   
    
    










