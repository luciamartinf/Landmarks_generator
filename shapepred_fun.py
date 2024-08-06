# !/usr/bin/python3

import dlib
import config
import os
from collections import OrderedDict 
import sys
import multiprocessing
from Landmarks_module import Landmarks

procs = multiprocessing.cpu_count()
procs = config.PROCS if config.PROCS > 0 else procs 

def test_shape_predictor_params(
        treeDepth, nu, cascadeDepth, featurePoolSize, numTestSplits, oversamplingAmount,
        train_set, temp_dat):
    
    """Test parameters with a new split of the data
    
    Reference: 
        https://pyimagesearch.com/2020/01/13/optimizing-dlib-shape-predictor-accuracy-with-find_min_global/
    """
    
    
    # Create a new val-train split
    train_xml, val_xml = train_set.split_data(tag = ['trn_val', 'validation'])

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

	# train the model using the current set of hyperparameters
    dlib.train_shape_predictor(train_xml, temp_dat, options)

	# take the newly trained shape predictor model and evaluate it on both our training and validating sets
    trainingError = dlib.test_shape_predictor(train_xml, temp_dat)
    testingError = dlib.test_shape_predictor(val_xml, temp_dat)
    
	# display the training and validation errors for the current trial
    print("[INFO] Train error (MSE): {}".format(trainingError))
    print("[INFO] Validation error (MSE): {}".format(testingError))
    sys.stdout.flush()
    
	# return the error on the testing set
    return testingError


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
    test_shape_predictor_params_with_fixed_args = lambda *params: test_shape_predictor_params(*params, *fixed_args)

    # utilize dlib to optimize our shape predictor hyperparameters
    (bestParams, bestLoss) = dlib.find_min_global(
        test_shape_predictor_params_with_fixed_args,
        bound1=lower,
        bound2=upper,
        is_integer_variable=isint,
        num_function_calls=config.MAX_FUNC_CALLS)
    
    # display the optimal hyperparameters so we can reuse them in our training script
    print("[INFO] optimal parameters: {}".format(bestParams))
    print("[INFO] optimal error: {}".format(bestLoss))

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

  
def measure_model_error(
    model, xml_annotations):
    
    """Measure MAE of the model"""

    error = dlib.test_shape_predictor(xml_annotations, model)
    print("{} MAE of the model: {} is {}".format(xml_annotations, model, error))
