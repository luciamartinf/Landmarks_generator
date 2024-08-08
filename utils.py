#!/usr/bin/env python3

import os
from PIL import Image
import sys
import numpy as np
from scipy.optimize import linear_sum_assignment

def determine_optimal_reordering(set1, set2):
    
    """Determine optimal reordering of set2 considering the order of set1"""
    
    # Calculate the pairwise distance matrix
    distance_matrix = np.linalg.norm(set1[:, np.newaxis] - set2, axis=2)

    # Use the Hungarian algorithm to find the optimal assignment
    _, col_indices = linear_sum_assignment(distance_matrix)

    return col_indices

def check_make_dir(folder_path):

    """
    Check if a directory exists and creates it if it doesn't
    """

    # Check if the folder exists
    if not os.path.exists(folder_path):

        # Create the folder if it doesn't exist
        os.makedirs(folder_path)

def check_dir(folder_path):

    """
    Just checks if a directory exists
    """

    # Check if the folder exists
    if not os.path.exists(folder_path):

        # Print error message
        print(f"ERROR: We could not find {folder_path}") # Make this error message better
        sys.exit()

def what_file_type(file):

    """
    Get the extension of a file.
    
    Parameters:
        file_path (str): The path of the file.
    
    Returns:
        str: The file extension (including the dot).
    """
    _, extension = os.path.splitext(file)

    return extension.lower()

def start_xml_file(file, name, item='Carabus pronotum'): # Tengo que quitar este default

    """
    Start xml file for the project 
    """

    with open(file, 'w') as f:
        f.write(f"<?xml version='1.0' encoding='ISO-8859-1'?>\n")
        f.write(f"<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n")
        f.write(f"<dataset>\n")
        f.write(f"<name>{item} {name}</name>\n")
        f.write(f"<images>\n")

def append_to_xml_file(file, img, my_dict, folder):

    """
    Add image code to xml file
    """

    with open(file, 'a') as f:
        image_path = os.path.join(folder, img)
        im = Image.open(image_path)
        width, height = im.size
        f.write(f"\t<image file='{image_path}' width='{int(width)}' height='{int(height)}'>\n")
        f.write(f"\t\t<box top='1' left='1' width='{int(width-2)}' height='{int(height-2)}'>\n")
        i = 0
        for lm in my_dict[img]:
            f.write(f"\t\t\t<part name='{i}' x='{int(lm[0])}' y='{int(lm[1])}'/> \n")
            i+=1
        f.write(f"\t\t</box>\n")
        f.write(f"\t</image>\n")
  

def end_xml_file(file):
    
    """
    Close xml file
    """

    with open(file, 'a') as f:
        f.write(f"</images>\n")
        f.write(f"</dataset>\n")

def which(line):
        
    """
    Defines type of line in a tps file
    """

    token = str(line.strip().split("=")[0])
    value = line.strip().split("=")[1]

    return token, value



def check_for_xml_files(folder_path):
    # Get the list of all files in the specified folder
    files_in_folder = os.listdir(folder_path)
    
    # Check if any file ends with .xml
    xml_files = [file for file in files_in_folder if file.endswith('.xml')]
    
    # Return True if there are any .xml files, False otherwise
    return xml_files

    
def check_trainmodel(model_name, work_dir, model_version):
    
    """
    Checks if a file exists and creates new version if it does. 
    """
    # A lo mejor puedo quitar algunos mensajes
    # A lo mejor puedo añadir esta funcion a la clase de Landmarks 

    # Check if the file exists
    if model_version != 0:
        file = os.path.join(work_dir, f'{model_name}_{model_version}.dat')
    else:
        file = os.path.join(work_dir, f'{model_name}.dat')
    while os.path.isfile(file):
        model_version += 1
        # Enhanced error message
        print(f"WARNING: The file '{os.path.basename(file)}' already exists.")
        # Generate a new filename
        filename = model_name + f"_{model_version}.dat"
        print(f"Creating a new version of the model '{filename}'...")
        # Optionally create the new file or handle accordingly
        file = os.path.join(work_dir, filename)
        
    else:
        # open(file, 'a').close()
        print(f"Proceeding with training. Generating {os.path.basename(file)} model. ")
    return file

def check_predmodel(file, work_dir, parser):
    
    """
    Checks if a file exists for predicting
    """

    # Check if the file exists
    if (os.path.isfile(file)) and (os.path.getsize(file) > 0):
        print("Proceeding with predicting Landmarks")
        return file
    else: 
        sys.stderr.write(f"\nERROR: Model '{os.path.basename(file)}' does not exist. Unable to predict landmarks with this model")
        sys.stderr.write(f"\nTry using another model or training a new model")
        parser.print_help()
        sys.exit(2)
        
def write_list_to_file(mylist, myfile):
    with open(myfile, 'w') as file:
        for item in mylist:
            file.write(f"{item}\n")


def read_list_from_file(myfile):
    with open(myfile, 'r') as file:
        data = file.readlines()
        data = [float(line.strip()) for line in data]
        
    return data
