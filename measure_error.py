# !/usr/bin/python3

import argparse
from shapepred_fun import measure_model_error


# TODO: complete this functions with notebook
# Calculate mean relative error and other types, mean standard deviation ...

# reorganize points so they all have same order, esto tambien en el predict script

# transform xml in .tps and viceversa
# generate .tps prediction from xml_file =  output, only if output flag is on 


def measure_mae(dat, xml_file):
    
    """Calculates Mean Absolute Error (MAE)"""
    
    print("Calculating MSE error of the model")
    measure_model_error(dat, xml_file) # aqui usar train + val


def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= '')
    
    parser.add_argument('-f', '--file', required=True, 
                        help = '.xml or .txt file that contains real landmarks')
    
    parser.add_argument('-m', '--model', required=True,
                        help = ".dat file path of the LandmarkGen model.")
    
    parser.add_argument('-o', '--output', 
                        help = "Output file that will contain predicted landmarks in .tps")
        
    args = parser.parse_args()
    
    xml = args.file
    dat = args.model
    
    measure_mae(dat, xml)

if __name__ == "__main__":
    main()  