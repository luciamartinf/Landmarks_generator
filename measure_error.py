#!/usr/bin/env python3

#### # !/usr/bin/python3

import numpy as np
from scipy.optimize import linear_sum_assignment
import os
import dlib

import argparse
import shapepred_fun 
from Landmarks_module import Landmarks


# TODO: complete this functions with notebook
# Calculate mean relative error and other types, mean standard deviation ...


# generate .tps prediction from xml_file =  output, only if output flag is on 


def measure_mae(
    model, xml_annotations):
    
    """Calculates Mean Absolute Error (MAE)"""
    
    error = dlib.test_shape_predictor(xml_annotations, model)
    print("{} MAE of the model: {} is {}".format(
        os.basename(xml_annotations), os.basename(model), error))


def get_shapes(
    dat, xml_file):
   
   set = Landmarks(xml_file) # img_list y lm_dict
   
   real_shapes = np.array((set.lm_dict).values())
   
   pred_shapes = set.predict_shapes(dat)
   
   return pred_shapes, real_shapes
   
    

def calculate_mean_relative_error(real_coords, estimated_coords):
    
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

def calculate_mean_relative_error_for_shapes(real_shapes, estimated_shapes):
    
    num_shapes = len(real_shapes)
    
    if num_shapes != len(estimated_shapes):
        raise ValueError("The number of real shapes and estimated shapes must be the same.")

    # List to store the MRE for each pair of shapes
    mre_values = []

    for real_coords, estimated_coords in zip(real_shapes, estimated_shapes):
        # Calculate the optimal order for the estimated coordinates to match the real coordinates
        # distance_matrix = np.linalg.norm(real_coords[:, np.newaxis] - estimated_coords, axis=2)
        # _, col_indices = linear_sum_assignment(distance_matrix)
        
        # # Reorganize the estimated coordinates
        # reorganized_estimated_coords = estimated_coords[col_indices]
        
        # Calculate MRE for the current pair of shapes
        mre = calculate_mean_relative_error(real_coords, reorganized_estimated_coords)
        mre_values.append(mre)

    # Calculate the mean MRE across all shape pairs
    mean_mre = np.mean(mre_values)

    return mean_mre




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
    
    pred_shapes, real_shapes = get_shapes(dat, xml)
    
    mean_mre = calculate_mean_relative_error_for_shapes(pred_shapes, real_shapes)
    
    print("{} MRE of the model: {} is {}".format(
        os.basename(xml), os.basename(dat), mean_mre))

    measure_mae(dat, xml)

if __name__ == "__main__":
    main()  