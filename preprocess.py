#!/usr/bin/env python3

import argparse
from Generate_model import find_best_params, train_model, measure_model_error
from utils import check_dir, check_for_xml_files
from Landmarks_module import Landmarks
import os
import multiprocessing
import utils
import generate_tps

import config

def preprocessing(lmfile, image_dir):
    
    Landmarks.data_dir = os.path.abspath(image_dir)
    Landmarks.create_flipdir()
    input_data = Landmarks(lmfile)
    train_xml, test_xml = input_data.split_data()
    
    return train_xml, test_xml