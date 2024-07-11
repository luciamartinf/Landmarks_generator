import os


# TRAIN_PATH = '/Users/luciamf/Desktop/beetle_classification/model1/data/model_train/train.xml'

# TEST_PATH = '/Users/luciamf/Desktop/beetle_classification/model1/data/model_train/val.xml'

# TEMP_MODEL_PATH = '/Users/luciamf/Desktop/beetle_classification/model1/temp.dat'

# TRAIN_FOLDER = '/Users/luciamf/Desktop/beetle_classification/model1/data/model_train/'

# Number of threads/cores we'll be using when training our models. 
PROCS = -1 # Investigar esto un poco mas antes de activarlo. Si esta como -1 significa que vamos a usar todos los cores de la maquina

# Maximum number of trials we'll be performing when tuning our shape predictor hyperparameters
MAX_FUNC_CALLS = 1 # a lo mejor esto lo puedo tunear
