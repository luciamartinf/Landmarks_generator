#!/usr/bin/env python3

import arg_parse
from Generate_model import find_best_params, train_model, measure_model_error
from utils import check_dir, check_for_xml_files
from Landmarks_module import Landmarks
import os
import multiprocessing

import config


def train_model(model, train_xml, test_xml, ):
    