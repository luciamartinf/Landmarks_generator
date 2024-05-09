import argparse

def check_arg():

    """
    Function to collect arguments from command line using argparse
    """

    parser = argparse.ArgumentParser(prog = 'predictor', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')

    add = parser.add_argument

    add('--mode', type=str, choices=['train', 'predict'], default='train',
        help = "Mode of using")

    add('--inputdir','-i', required=True, # podria ser './' por defecto
        help='Input main directory')
    
    add('--input_file', '-f',
        help = 'Input file')
    
    add('--model_name', '-m', required=True, 
        help='Model name')
    
    # add('--model_version', '-mv', required=True, 
    #     help='Model version')
    
    
    add('--version', action='version', version='%(prog)s 0.0.1')

    add('--data_dir', '-d', help='Preprocess data and create flip_images')

    add('--preprocess', '-p', action='store_true',
        help='Preprocessing data and create train and test sets')

    return parser.parse_args()