import numpy as np
import argparse
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


def order_shape(real_shape, pred_shape, optimal_order):
        
        "Get real and predicted shape"
        
        if len(optimal_order) == 0:
            optimal_order = calculate_optimal_order(np.array(real_shape), pred_shape)
            
        sorted_pred_shape = reorganize_points(pred_shape, optimal_order)
        
        return sorted_pred_shape, optimal_order
    

def reorganize_all(real_shapes, measured_shapes):
    
    """Reorganize all points in a set of shapes"""
    
    optimal_order = calculate_optimal_order(real_shapes[0], measured_shapes[0])
    
    sorted_shapes = []
    for shape in measured_shapes:
        points = reorganize_points(shape, optimal_order)
        sorted_shapes.append(points)
        
    return sorted_shapes

  
def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Predict and measure the error of a model') # Elaborate this description
    
    parser.add_argument('-f', '--file', required=True, 
                        help = '.xml or .txt file that contains real landmarks')
    
    parser.add_argument('-i', '--image_dir', required = True,
                        help = 'Input directory containing the images')
    
    parser.add_argument('-m', '--model', required=True,
                        help = ".dat file path of the LandmarkGen model.")
    
    parser.add_argument('-o', '--output', 
                        help = "Output file that will contain predicted landmarks in .tps")
    
    # reorganize points so they all have same order, esto tambien en el predict script dentro de predict_landmarks en Landmarks_module
    # Esto igual no tiene sentido porque tendria que ordenarlo en funcion de la misma imagen anotada manualmente entonces no tengo una referencia y no puedo ordenarlo
    # Pero para eso tendria que meter como argumento en ese script tambien el train.txt

    # transform xml in .tps and viceversa
    
    
    print("reorganize")
    
    
    
if __name__ == "__main__":
    main()  