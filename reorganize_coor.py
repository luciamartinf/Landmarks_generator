#!/usr/bin/env python3

import numpy as np
import argparse
from scipy.optimize import linear_sum_assignment
from Landmarks_module import Landmarks
import os
import reorganize_fun

# No funciona porque estoy reorganizando algunas que no hacen falta y la lio mas

def main():
    
    parser = argparse.ArgumentParser(prog = '', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Predict and measure the error of a model') # Elaborate this description
    
    parser.add_argument('-f', '--file', required=True, 
                        help = '.xml or .txt file that contain landmarks')
    
    parser.add_argument('-o', '--output', 
                        help = "Output file that will contain the reorganized landmarks in .tps")
    
    args = parser.parse_args()
    
    filepath = os.path.abspath(args.file)
    
    folder = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    
    if args.output:
        outfile = os.path.abspath(args.output)
    else:
        outfile = f'sorted_{basename}'
        
    outpath = os.path.join(folder,outfile)
    
    landmarks = Landmarks(filepath, flip=False)
    
    landmarks_dict = Landmarks.nested_dict
    images = landmarks.img_list
    
    first_image = images[0]
    ref_shape = landmarks_dict[first_image]['LM']
    
    for img in images[1:]:
        input_shape = np.array(landmarks_dict[img]['LM'])
        
        lm_list, _ = reorganize_fun.order_shape(ref_shape, input_shape, [])
        
        if not np.array_equal(lm_list, input_shape):
            print(f"Reorganizing landmarks for image {img}") 
        
        landmarks.append_to_tps(img, lm_list, outpath) 
     

    # reorganize points so they all have same order, esto tambien en el predict script dentro de predict_landmarks en Landmarks_module
    # Esto igual no tiene sentido porque tendria que ordenarlo en funcion de la misma imagen anotada manualmente entonces no tengo una referencia y no puedo ordenarlo
    # Pero para eso tendria que meter como argumento en ese script tambien el train.txt

    # transform xml in .tps and viceversa
    
    # Puedo coger un archivo ya anotado y reorganizar todas las landmarks con el orden de la primera imagen 
    
    
    
    
if __name__ == "__main__":
    main()  