import numpy as np
from scipy.optimize import linear_sum_assignment


def calculate_optimal_order(real_shape, measured_shape):
    
    """Calculate the optimal order of points in the measured shape to match the real shape."""
    
    # Calculate the pairwise distance matrix
    distance_matrix = np.linalg.norm(real_shape[:, np.newaxis] - measured_shape, axis=2)

    # Use the Hungarian algorithm to find the optimal assignment
    _, col_indices = linear_sum_assignment(distance_matrix)

    return col_indices

def reorganize_points(measured_shape, optimal_order):
    
    """Reorganize the points in the measured shape according to the optimal order."""
    
    return measured_shape[optimal_order]

def reorganize_all(real_shapes, measured_shapes):
    
    """Reorganize all points in a set of shapes"""
    
    optimal_order = calculate_optimal_order(real_shapes[0], measured_shapes[0])
    
    sorted_shapes = []
    for shape in measured_shapes:
        points = reorganize_points(shape, optimal_order)
        sorted_shapes.append(points)
        
    return sorted_shapes

  
def main():
    
    # reorganize points so they all have same order, esto tambien en el predict script dentro de predict_landmarks en Landmarks_module
    # Pero para eso tendria que meter como argumento en ese script tambien el train.txt

    # transform xml in .tps and viceversa
    
    
    print("reorganize")
    
    
    
if __name__ == "__main__":
    main()  