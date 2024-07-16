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


args = arg_parse.parse_args()

if not args.work_dir:
    work_dir = os.getcwd()
else:
    work_dir = os.path.abspath(args.work_dir)
    

    
model_name = args.model_name
if args.model_version:
    model_version = int(args.model_version)
else:
    model_version = 0
print(f'version is: {model_version}')
# check if dat file already exists and create the appropiate version
dat = utils.check_file(model_name, work_dir, model_version)
