# !/usr/bin/python3

from arg_parse import check_arg
from Generate_model import find_best_params, train_model, measure_model_error
from Landmarks_module import Landmarks
import os
import multiprocessing

import config


#######################
### PARSE ARGUMENTS ###
#######################

# python predictor.py -i ./ -m flip_lm -mv 2


# Crear modos de ejecucion

arguments = check_arg()



model_name = arguments.model_name
# model_version = arguments.model_version


main_dir = arguments.inputdir

# Get full directory name if we are refering as a relative path
if main_dir.startswith('.'):
    main_dir = os.path.abspath(main_dir)


data_dir = os.path.join(main_dir, 'data') # esto tambien puede ser un argumento

# Initialize class variables. Indicate directories we are going to work in
Landmarks.data_dir = data_dir
Landmarks.create_flipdir()



##################################
### PREPROCESSING FOR TRAINING ###
##################################

# -train landmarks.txt

# Getting annotated file
landmarks_file = 'Carabus_pronotumLANDMARKS.TXT' # esto deberia ser otro argumento pero de momento lo vamos a dejar asi
lm_path = os.path.join(main_dir, landmarks_file)

input_data = Landmarks(lm_path)


train_xml, test_xml, train_list = input_data.split_data()
print("Creating train and test xml files")
print(train_xml)

train_set = Landmarks(train_xml, img_list=train_list)

# # test_set = Landmarks(test_xml) # Este no lo necesito


#######################
### MODEL GENERATOR ###
#######################

# Determine the number of processes / threads to use
procs = multiprocessing.cpu_count()
procs = config.PROCS if config.PROCS > 0 else procs 

# temp model
temp = os.path.join(main_dir, 'temp.dat')

# Find best parameters
# aqui usar train para entrenar y val para testear

best_params = find_best_params(train_set, temp)

# Train model
dat = os.path.join(main_dir, f'{model_name}.dat')
train_model(dat, train_xml, best_params)
print(dat)


# ##################
# ### TEST MODEL ###
# ##################

# Compute training and test MSE errors of the model
measure_model_error(dat, train_xml) # aqui usar train + val
measure_model_error(dat, test_xml) # aqui usar solo test
