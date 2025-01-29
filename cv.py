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
k = config.KFOLDS


def start_eval_file(eval_file):
    with open(eval_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(["cpu","Fold","Training_size", "Testing_size", "Tree_depth", "cascade_depth", "nu", "feature_pool_size", "num_test_splits", "oversampling_amount", "landmark_relative_padding_mode", "training_time", "training_error", "testing_error", "model_size"])


def eval_model(
        treeDepth, nu, cascadeDepth, featurePoolSize, numTestSplits, oversamplingAmount, landmark_relative_padding_mode,
        train_set, temp_dat):
    
    """Test parameters with a new split of the data and save results to a file
    
    Reference: 
        https://pyimagesearch.com/2020/01/13/optimizing-dlib-shape-predictor-accuracy-with-find_min_global/
    """
    
    eval_file = 'Evaluation.tsv'
    
    kf = KFold(n_splits=k)
    
    training_error = []
    validating_error = []
    
    train_list = train_set.img_list
    
    
    for i, (train_index, test_index) in enumerate(kf.split(train_list)):
        # print(f"Fold {i}:")
        
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
        options.landmark_relative_padding_mode = int(landmark_relative_padding_mode)

        # tell dlib to be verbose when training and utilize our supplied number of threads when training
        options.be_verbose = True	
        options.num_threads = procs
        
        # display the current set of options to our terminal
        # print("[INFO] starting training with another split...")
        # print(options)
        # sys.stdout.flush()

        start_time = time.time()
        # train the model using the current set of hyperparameters
        dlib.train_shape_predictor(train_xml, temp_dat, options)
        end_time = time.time()
        training_time = end_time - start_time
        
        model_size = os.path.getsize(temp_dat) / 1024
        
        # take the newly trained shape predictor model and evaluate it on both our training and validating sets
      
        training_error.append(dlib.test_shape_predictor(train_xml, temp_dat))
        validating_error.append(dlib.test_shape_predictor(val_xml, temp_dat))
        
        # display the training and validation errors for the current trial
        print("[INFO] Train error of all the folds (MSE): {}".format(training_error[-1]))
        print("[INFO] Validation error of all the folds (MSE): {}".format(validating_error[-1]))
        sys.stdout.flush()
        with open(eval_file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([procs, f"{i}/{k}", training_size, testing_size, treeDepth, cascadeDepth, nu, featurePoolSize, numTestSplits, oversamplingAmount, landmark_relative_padding_mode, training_time, training_error[-1], validating_error[-1], model_size])
        
    
    trainingError = np.mean(training_error)
    validatingError = np.mean(validating_error)
    print(options)
    sys.stdout.flush()
	# display the training and validation errors for the current trial
    print("[INFO] Train error of all the folds (MSE): {}".format(np.mean(trainingError)))
    print("[INFO] Validation error of all the folds (MSE): {}".format(np.mean(validatingError)))
    sys.stdout.flush()
    
    with open(eval_file, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([procs, "mean", training_size, testing_size, treeDepth, cascadeDepth, nu, featurePoolSize, numTestSplits, oversamplingAmount, landmark_relative_padding_mode, training_time, training_error[-1], validating_error[-1], model_size])
    
	# return the error on the testing set
    return validatingError



def find_best_params(
    train_set, temp_dat):
    
    """Find best hyperparameters for the shape predictor"""

    # Define hyperparameters range
    params = OrderedDict([
        ("tree_depth", (3, 8, True)),
        ("nu", (0.01, 0.3, False)),
        ("cascade_depth", (8, 18, True)),
        ("feature_pool_size", (200, 600, True)),
        ("num_test_splits", (50, 200, True)),
        ("oversampling_amount", (20, 100, True)), # In general we are working with small datasets. 
        ("landmark_relative_padding_mode", (0,1, True))
    ])    

    lower = [v[0] for (k, v) in params.items()]
    upper = [v[1] for (k, v) in params.items()]
    isint = [v[2] for (k, v) in params.items()]

    fixed_args = (train_set, temp_dat)

    test_shape_predictor_params_with_fixed_args = lambda *params: eval_model(*params, *fixed_args)
    
    start_eval_file("Evaluation.tsv")
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
    options.landmark_relative_padding_mode = int(params_list[6])

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