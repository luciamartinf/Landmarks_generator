#!/usr/bin/env python3

import numpy as np
from scipy.optimize import linear_sum_assignment


def determine_optimal_reordering(set1, set2):
    
    """Determine optimal reordering of set2 considering the order of set1"""
    
    # Calculate the pairwise distance matrix
    distance_matrix = np.linalg.norm(set1[:, np.newaxis] - set2, axis=2)

    # Use the Hungarian algorithm to find the optimal assignment
    _, col_indices = linear_sum_assignment(distance_matrix)

    return col_indices

def calculate_mre(real_coords, estimated_coords):
        
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
