# !/usr/bin/python3

# import json
import os
# import random
# import shutil
# import rembg
from PIL import Image
# import cv2


def check_make_dir(folder_path):

    """
    Check if a directory exists and creates it if it doesn't
    """

    # Check if the folder exists
    if not os.path.exists(folder_path):

        # Create the folder if it doesn't exist
        os.makedirs(folder_path)



                


def what_file_type(file):

    """
    Get the extension of a file.
    
    Parameters:
        file_path (str): The path of the file.
    
    Returns:
        str: The file extension (including the dot).
    """
    _, extension = os.path.splitext(file)

    return extension

def start_xml_file(file, name):

    """
    Start xml file
    """

    with open(file, 'w') as f:
        f.write(f"<?xml version='1.0' encoding='ISO-8859-1'?>\n")
        f.write(f"<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n")
        f.write(f"<dataset>\n")
        f.write(f"<name>Carabus pronotum {name}</name>\n")
        f.write(f"<images>\n")

def append_to_xml_file(file, img, my_dict, folder):

    """
    Add image to xml file
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

    with open(file, 'a') as f:
        f.write(f"</images>\n")
        f.write(f"</dataset>\n")

