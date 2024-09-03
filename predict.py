#!/usr/bin/env python3

import os
import sys
import generate_tps as generate_tps
import utils
import arg_parse
from Landmarks_module import Landmarks

def predict(image_dir, file, dat, output, gen_images=False):
    
    """Predict Landmarks from tps unannotated file and images

    Parameters:
        image_dir (Directory): Directory that contains images 
        file (File): tps unannotated file
        dat (File): Machine Learning model to predict landmarks
    """
    
    Landmarks.data_dir = os.path.abspath(image_dir)
    Landmarks.create_flipdir()
    data = Landmarks(file)
    data.predict_landmarks(dat, output, generate_images=gen_images)



def main():
    
    # Reading arguments
    parser = arg_parse.get_predict_parser()
    args = parser.parse_args()

    image_dir = os.path.abspath(args.input_dir)
    work_dir = os.path.abspath(args.output_dir)
    Landmarks.work_dir = work_dir

    model_file = args.model
    model_name = os.path.splitext(os.path.basename(model_file))[0]

    
    # Check that the model exist
    dat = utils.check_predmodel(model_file, work_dir, parser)
    
    if args.input_file:
        
        if utils.what_file_type(args.input_file) not in ['.txt', '.tps']:
            
            if not args.scale:
                sys.stderr.print("\nERROR: Invalid input file and no scale specified. Unable to proceed with prediction\n")
                parser.print_help()
                sys.exit(2)
            
            else:
                print("\nWARNING: Invalid input file, but scale was specified.")
                print("Generating a new tps file with specified scale.")
                tpsfile = generate_tps.write_tpsfile(image_dir, 'input_images.tps', scale=args.scale)
        
        elif Landmarks.check_forlm(args.input_file):
            print("WARNING: This file already contains annotated landmarks")
            tpsfile = args.input_file
        
        else:
            tpsfile = args.input_file 
    
    elif args.scale: # If not tpsfile check that we can create a tps file
        tpsfile = generate_tps.write_tpsfile(image_dir, 'input_images.tps', scale = args.scale)
    
    else:
        sys.stderr.write("\nERROR: No input file and no scale specified. Unable to proceed with prediction\n")
        parser.print_help()
        sys.exit(2)
    
    if args.output_file:
        output = args.output_file
    else:
        output = f'{model_name}_landmarks.tps'
        
        
    ## Call predict function   
    print("Predicting Landmarks...")
    predict(image_dir, tpsfile, dat, output, args.plot)
    
    # Deleting flip_images from work_data path
    utils.delete_files(Landmarks.flip_dir)

    print("Done!")

if __name__ == "__main__":
    main()      