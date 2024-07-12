#!/usr/bin/env python3

import arg_parse
from Generate_model import find_best_params, train_model, measure_model_error
from utils import check_dir, check_for_xml_files
from Landmarks_module import Landmarks
import os
import multiprocessing

import config
import random

random.seed(5399) # Always same splits 

#######################
### PARSE ARGUMENTS ###
#######################

# python main.py -i ~/Desktop/model_3004 -d ~/Desktop/model_3004/data_nocrop -m model_3004 --mode predict -f /Users/luciamf/Desktop/model_3004/Carabus_pronotum.TXT
# python main.py -i ~/Desktop/model_3004 -d ~/Desktop/model_3004/data_nocrop -m model_3004 --mode train -f /Users/luciamf/Desktop/model_3004/Carabus_pronotumLANDMARKS.TXT


args = arg_parse.parse_args()

if not args.work_dir:
    work_dir = os.getcwd()
else:
    work_dir = os.path.abspath(args.work_dir)
    

    
model_name = args.model_name
# check if dat file exists or if just model name
dat = os.path.join(work_dir, f'{model_name}.dat')
# model_version = arguments.model_version

image_dir = os.path.abspath(args.image_dir)
# else:
#     image_dir = os.path.join(work_dir, 'data') # esto tambien puede ser un argumento
# check_dir(image_dir)

landmarks_file = args.file
lm_path = os.path.join(work_dir, landmarks_file)



##################################
### PREPROCESSING FOR TRAINING ###
##################################



# Initialize class variables. Indicate directories we are going to work in
Landmarks.data_dir = image_dir
Landmarks.create_flipdir() # Only creates work_dir if it doesn't exist already

# Creates Landmarks object with input data
input_data = Landmarks(lm_path)


# -train landmarks.txt

# Getting annotated file


work_data = os.path.join(image_dir, 'work_data/')

# FOR AVOIDING EXTRA PROCESSING
# xml_files = check_for_xml_files(work_data)

# if len(xml_files) > 0 :
    
#     train_xml = [file for file in xml_files if 'train' in file]
#     test_xml = [file for file in xml_files if 'test' in file]
    
# else:
#     train_xml, test_xml = input_data.split_data()

train_xml, test_xml = input_data.split_data()

train_set = Landmarks(train_xml)

# # test_set = Landmarks(test_xml) # Este no lo necesito


#######################
### MODEL GENERATOR ###
#######################

# Determine the number of processes / threads to use
procs = multiprocessing.cpu_count()
procs = config.PROCS if config.PROCS > 0 else procs 

# # temp model
# temp = os.path.join(work_dir, 'temp.dat')
# # Find best parameters
# # aqui usar train para entrenar y val para testear
# best_params = find_best_params(train_set, temp)
# # Train model

# train_model(dat, train_xml, best_params)


print(dat)
# ##################
# ### TEST MODEL ###
# ##################
# Compute training and test MSE errors of the model
measure_model_error(dat, train_xml) # aqui usar train + val
measure_model_error(dat, test_xml) # aqui usar solo test
input_data.check_for_negatives(dat)

###################
##### PREDICT #####
###################


# input_data.predict_landmarks(dat)
