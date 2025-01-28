#!/usr/bin/env python3

import dlib
import config
import os
from collections import OrderedDict 
import sys
import multiprocessing
import numpy as np
import time
import csv
from sklearn.model_selection import KFold

procs = multiprocessing.cpu_count()
procs = config.PROCS if config.PROCS > 0 else (procs-1) 


def start_eval_file(eval_file):
    with open(eval_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(["cpu","Training_size", "Testing_size", "Tree_depth", "cascade_depth", "nu", "feature_pool_size", "num_test_splits", "oversampling_amount", "training_time", "training_error", "testing_error", "model_size"])


def eval_model(
        treeDepth, nu, cascadeDepth, featurePoolSize, numTestSplits, oversamplingAmount,
        train_set, temp_dat):
    
    """Test parameters with a new split of the data and save results to a file
    
    Reference: 
        https://pyimagesearch.com/2020/01/13/optimizing-dlib-shape-predictor-accuracy-with-find_min_global/
    """
    
    eval_file = 'Evaluation.tsv'
    # split_per = [0.6, 0.4]
    kf = KFold(n_splits=5)
    
    training_error = []
    validating_error = []
    for i, (train_index, test_index) in enumerate(kf.split(train_set)):
        print(f"Fold {i}:")
        
        training_size = len(train_index)
        testing_size = len(test_index)
    
        # Create a new val-train split
    
        train_xml, val_xml = train_set.fold_data(train_index, test_index, tag = ['trn_val', 'validation'])
    
        # Define options that we are going to tune
        options = dlib.shape_predictor_training_options()
        options.tree_depth = int(treeDepth)
        options.nu = nu
        options.cascade_depth = int(cascadeDepth)
        options.feature_pool_size = int(featurePoolSize)
        options.num_test_splits = int(numTestSplits)
        options.oversampling_amount = int(oversamplingAmount)

        # tell dlib to be verbose when training and utilize our supplied number of threads when training
        options.be_verbose = True	
        options.num_threads = procs
        
        # display the current set of options to our terminal
        print("[INFO] starting training with another split...")
        print(options)
        sys.stdout.flush()

        start_time = time.time()
        # train the model using the current set of hyperparameters
        dlib.train_shape_predictor(train_xml, temp_dat, options)
        end_time = time.time()
        training_time = end_time - start_time
        
        model_size = os.path.getsize(temp_dat) / 1024
        
        # take the newly trained shape predictor model and evaluate it on both our training and validating sets
      
        training_error.append(dlib.test_shape_predictor(train_xml, temp_dat))
        validating_error.append(dlib.test_shape_predictor(val_xml, temp_dat))
        trainingError = np.mean(training_error)
        validatingError = np.mean(validating_error)
    
	# display the training and validation errors for the current trial
    print("[INFO] Train error (MSE): {}".format(np.mean(trainingError)))
    print("[INFO] Validation error (MSE): {}".format(np.mean(validatingError)))
    sys.stdout.flush()
    
    with open(eval_file, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([procs, training_size, testing_size, treeDepth, cascadeDepth, nu, featurePoolSize, numTestSplits, oversamplingAmount, training_time, trainingError, validatingError, model_size])
    
	# return the error on the testing set
    return validatingError



def find_best_params(
    train_set, temp_dat):
    
    """Find best hyperparameters for the shape predictor"""

    # Define hyperparameters range
    params = OrderedDict([
        ("tree_depth", (3, 8, True)),
        ("nu", (0.001, 0.2, False)),
        ("cascade_depth", (8, 18, True)),
        ("feature_pool_size", (200, 1000, True)),
        ("num_test_splits", (20, 300, True)),
        ("oversampling_amount", (20, 100, True)), # In general we are working with small datasets. 
    ])    

    lower = [v[0] for (k, v) in params.items()]
    upper = [v[1] for (k, v) in params.items()]
    isint = [v[2] for (k, v) in params.items()]

    fixed_args = (train_set, temp_dat)
    #test_shape_predictor_params_with_fixed_args = lambda *params: test_shape_predictor_params(*params, *fixed_args)
    test_shape_predictor_params_with_fixed_args = lambda *params: eval_model(*params, *fixed_args)
    
    start_eval_file("eval_3.tsv")
    # utilize dlib to optimize our shape predictor hyperparameters
    (bestParams, bestLoss) = dlib.find_min_global(
        test_shape_predictor_params_with_fixed_args,
        bound1=lower,
        bound2=upper,
        is_integer_variable=isint,
        num_function_calls=config.MAX_FUNC_CALLS
        # solver_epsilon=35.0
        )
    
    # display the optimal hyperparameters so we can reuse them in our training script
    print("[INFO] optimal parameters: {}".format(bestParams))
    print("[INFO] optimal error: {}".format(bestLoss)) # bestLoss is just lower ValidatingError

    # delete the temporary model file
    os.remove(temp_dat)
    
    return bestParams


def train_model(
    name, xml, params_list):
    
    """Train model with the best hyperparameters"""

    options = dlib.shape_predictor_training_options()    
    options.tree_depth = int(params_list[0])
    options.nu = params_list[1]
    options.cascade_depth = int(params_list[2])
    options.feature_pool_size = int(params_list[3])
    options.num_test_splits = int(params_list[4])
    options.oversampling_amount = int(params_list[5])

    options.be_verbose = True  
    options.num_threads = procs 
  
    print(f"Training final model {name}")
    dlib.train_shape_predictor(xml, name, options)

  
def measure_mse(
    model, xml_annotations):
    
    """Measure MSE (mean square error)  of the model"""

    error = dlib.test_shape_predictor(xml_annotations, model)
    print("{} MSE of the model: {} is {}".format(os.path.basename(xml_annotations), os.path.basename(model), error))


def measure_mre(real_coords, estimated_coords):
        
    """Calculate Mean Relative Error"""
    
    # Calculate Euclidean distances (errors) between corresponding points
    errors = np.linalg.norm(real_coords - estimated_coords, axis=1)
    
    # Calculate magnitudes of the real coordinates
    magnitudes = np.linalg.norm(real_coords, axis=1)
    
    # Avoid division by zero by setting small magnitudes to a small number
    magnitudes[magnitudes == 0] = 1e-10
    
    # Calculate relative errors
    relative_errors = errors / magnitudes
    
    # Calculate Mean Relative Error
    mean_relative_error = np.mean(relative_errors)

    return mean_relative_error

def calculate_mae(real_coords, estimated_coords):
        
    """Calculate Mean Absolute Error manually"""
    
    # Calculate Euclidean distances (errors) between corresponding points
    errors = np.linalg.norm(real_coords - estimated_coords, axis=1)
    
    mae = np.mean(errors)
   
    return mae