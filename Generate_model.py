# !/usr/bin/python3

# from Landmarks_module import Landmarks
import dlib
import config
import os
from collections import OrderedDict # investigar esto
import multiprocessing # esto es para los cores de las cpus
import sys
from Landmarks_module import Landmarks



# Determine the number of processes / threads to use
procs = multiprocessing.cpu_count()
procs = config.PROCS if config.PROCS > 0 else procs 


def test_shape_predictor_params(
        treeDepth, nu, cascadeDepth, featurePoolSize, numTestSplits, oversamplingAmount,
        # oversamplingTransJitter, padding, lambdaParam, 
        train_set, temp_dat):
    
   
    # https://pyimagesearch.com/2020/01/13/optimizing-dlib-shape-predictor-accuracy-with-find_min_global/

    # Split train into train and val
    train_xml, val_xml, train_list = train_set.split_data(tag = ['train_val', 'validation'])

	# grab the default options for dlib's shape predictor and then
	# set the values based on our current hyperparameter values,
	# casting to ints when appropriate
    options = dlib.shape_predictor_training_options()
    options.tree_depth = int(treeDepth)
    options.nu = nu
    options.cascade_depth = int(cascadeDepth)
    options.feature_pool_size = int(featurePoolSize)
    options.num_test_splits = int(numTestSplits)
    options.oversampling_amount = int(oversamplingAmount)

    # options.oversampling_translation_jitter = oversamplingTransJitter
    # options.feature_pool_region_padding = padding
    # options.lambda_param = lambdaParam

	# tell dlib to be verbose when training and utilize our supplied
	# number of threads when training
    options.be_verbose = True	
    options.num_threads = procs
    # display the current set of options to our terminal
    
    print("[INFO] starting training with another split...")
    print(options)
    sys.stdout.flush()

	# train the model using the current set of hyperparameters
    dlib.train_shape_predictor(train_xml, temp_dat, options)

	# take the newly trained shape predictor model and evaluate it on
 	# both our training and testing set
    trainingError = dlib.test_shape_predictor(
        train_xml, temp_dat)
    testingError = dlib.test_shape_predictor(
        val_xml, temp_dat)
    
    
	# display the training and testing errors for the current trial
    print("[INFO] Train error (MAE): {}".format(trainingError))
    print("[INFO] Validation error (MAE): {}".format(testingError))
    sys.stdout.flush()
	# return the error on the testing set
    return testingError

############## _____________________ ESTO SE PUEDE METER EN UNA FUNCION



def find_best_params(train_set, temp_dat):

    # define the hyperparameters to dlib's shape predictor that we are
    # going to explore/tune where the key to the dictionary is the
    # hyperparameter name and the value is a 3-tuple consisting of the
    # lower range, upper range, and is/is not integer boolean,
    # respectively

    params = OrderedDict([
       ("tree_depth", (3, 8, True)),
        ("nu", (0.001, 0.2, False)),
        ("cascade_depth", (8, 18, True)),
        ("feature_pool_size", (300, 1000, True)),
        ("num_test_splits", (20, 300, True)),
        ("oversampling_amount", (20, 100, True)), # In general we are working with small datasets. Maybe max to 50
        # ("oversampling_translation_jitter",  (0.0, 0.00000001, False)), # quiero quitar esto
        # ("feature_pool_region_padding", (0, 0.00000001, False)),
        # ("lambda_param", (0.1, 0.1000000001, False))
    ])    

    # use our ordered dictionary to easily extract the lower and upper
    # boundaries of the hyperparamter range, include whether or not the
    # parameter is an integer or not

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
    # display the optimal hyperparameters so we can reuse them in our
    # training script
    print("[INFO] optimal parameters: {}".format(bestParams))
    print("[INFO] optimal error: {}".format(bestLoss))

    
    # delete the temporary model file
    os.remove(temp_dat)
    
    # print(bestParams)
    return bestParams

def train_model(name, xml, params_list):

    options = dlib.shape_predictor_training_options()    
    options.tree_depth = int(params_list[0])
    options.nu = params_list[1]
    options.cascade_depth = int(params_list[2])
    options.feature_pool_size = int(params_list[3])
    options.num_test_splits = int(params_list[4])
    options.oversampling_amount = int(params_list[5])
    # options.oversampling_translation_jitter = params_list[6]
    # options.feature_pool_region_padding = params_list[7]
    # options.lambda_param = params_list[8]

    options.be_verbose = True  # tells what is happening during the training
    options.num_threads = 6    # number of the threads used to train the model
  
    # finally, train the model
    dlib.train_shape_predictor(xml, name, options)

  
def measure_model_error(model, xml_annotations):

    '''requires: the model and xml path.
    It measures the error of the model on the given
    xml file of annotations.'''
    error = dlib.test_shape_predictor(xml_annotations, model)
    print("{} Error of the model: {} is {}".format(xml_annotations, model, error))
