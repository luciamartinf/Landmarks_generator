# !/usr/bin/python3

from typing import Dict, List, Any
import os
from PIL import Image # type: ignore

from utils import check_make_dir, start_xml_file, end_xml_file, append_to_xml_file, what_file_type
import random

class Landmarks:

    data_dir: str = None
    flip_dir: str = None
    nested_dict: Dict[str, Dict[str, Any]] = {} 

    """
    Class for managing landmarks
    """

    def __init__(self, file: str, img_list: List = [], lm_dict: Dict = {}, nested_dict = {}) -> None:

        """
        Initializes Landmark object with a txtfile.
        """

        self.lm_dict: Dict[str, List] = lm_dict
        self.img_list: List[List[float, float]] = img_list
        
        
        # Landmarks.nested_dict: Dict[str, Dict[str, Any]] = {} 

        # En lugar de hacer esto podemos hacer una funcion tambien que sea what_type
        ext = what_file_type(file)
        print(ext)

        if ext == '.xml':

            self.xmlfile = file

            # read xml file
            print("WARNING: Initializing from xml file. Some attributes may be missing")

        else:

            if Landmarks.check_forlm(file):

                self.txt_lmfile: str = file  # complete filepath

                self.lm_dict, self.img_list, Landmarks.nested_dict = self.readtxt_lmfile()
            
            else: # The input txt file does not contain the landmarks yet

                self.txt_imgfile: str = file

                self.lm_dict, self.img_list, Landmarks.nested_dict = self.readtxt_imgfile()

        # Esta variable de clase se inicializa con el primer documento que leemos. 
        # Revisar esto porque si lo iniciamos con el que no tiene las landmarks no tiene sentido. 
        # Tengo que hacer mas funciones para inicializar cada uno de los atributos y variables de manera independiente
        if len(Landmarks.nested_dict) == 0:
            Landmarks.nested_dict = nested_dict
            
        ## Necesito algo para inicializar sin ningun archivo. 
        ## Inicializar desde folder con imagenes y una escala determinada


    @classmethod
    def create_flipdir(
            cls):

        """
        Initializes the flip directory and creates it if it does not exist
        """

        flip_dir = os.path.join(Landmarks.data_dir, 'flip_images')
        check_make_dir(flip_dir)
        Landmarks.flip_dir = flip_dir

    @staticmethod
    def check_id_img(
        real_id, img_name):

        """
        Check that img_name and annotated id are the same
        """
        # img_name es del tipo ind2784.jpg
        img_id = img_name.split('.')[0].upper() # nos quedamos con IND2934584

        if real_id != img_id:

            print(f"WARNING: ID={real_id} doesn't correspond to IMAGE={img_name}. Forcing ID to {img_id}")

        return img_id

    @staticmethod
    def check_forlm(
        file_name
            ):

        """
        Checks if the txt files already contains the landmarks
        """

        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith("LM"):
                    n_lm = int(line.strip().split('=')[1])
                    if n_lm == 0:
                        return False
                    else:
                        return True

    
    def readtxt_lmfile(
            self):
        
        """
        Read Landmarks text file 
        """

        with open(self.txt_lmfile, 'r') as file:
            for line in file:
                if line.startswith("LM"):
                    lm_list = []
                    n_lm = int(line.strip().split('=')[1])

                    if n_lm == 0:
                        print(f"WARNING: No landmarks annotated for this image")
                        # HACER ALGO AL RESPECTO

                    i = 0
                    while i < n_lm:
                        for line in file: # read all the landmarks
                            lm = line.strip().split()
                            lm_list.append([float(lm[0]), float(lm[1])])
                            break
                        i+=1

                    # REMEMBER: Change these ifs to  try
                    next_line = file.readline()
                    if next_line.startswith("IMAGE"):
                        image_name = str(next_line.strip().split('=')[1])
                        image = self.flip_image(image_name) # we are flipping the image and saving it in the dictionary we are going to work with
                        self.lm_dict[image] = lm_list
                        self.img_list.append(image)

                        # A LO MEJOR EN EL NESTED DICTIONARY TIENE MAS SENTIDO TENER EL NOMBRE ORIGINAL QUE ES EL QUE VAMOS A USAR DESPUES
                        self.nested_dict[image_name] = {}
                        self.nested_dict[image_name]["LM"] = lm_list
                        # self.nested_dict[image]["n_LM"] = n_lm # Creo que esto no lo necesito

                    next_line = file.readline()
                    if next_line.startswith("ID"):
                        real_id = str(next_line.strip().split('=')[1])
                        img_id = Landmarks.check_id_img(real_id, image_name)
                        self.nested_dict[image_name]["ID"] = img_id
                    
                    next_line = file.readline()
                    if next_line.startswith("SCALE"):
                        scale = next_line.strip()
                        self.nested_dict[image_name]["SCALE"] = scale

        return self.lm_dict, self.img_list, self.nested_dict
    
    def readtxt_imgfile(
            self):
        
        """
        Read text file 
        """

        with open(self.txt_imgfile, 'r') as file:
            for line in file:
                if line.startswith("LM"):
                    n_lm = int(line.strip().split('=')[1])

                    if n_lm > 0:
                        print(f"WARNING: There are some Landmarks already annotated for this image")
                        # HACER ALGO AL RESPECTO


                    # REMEMBER: Change these ifs to  try
                    next_line = file.readline()
                    if next_line.startswith("IMAGE"):
                        image = str(next_line.strip().split('=')[1])
                        self.lm_dict[image] = []
                        self.img_list.append(image)
                        self.nested_dict[image] = {}
                        self.nested_dict[image]["LM"] = []
                        # self.nested_dict[image]["n_LM"] = n_lm # Creo que esto no lo necesito

                    next_line = file.readline()
                    if next_line.startswith("ID"):
                        real_id = str(next_line.strip().split('=')[1])
                        img_id = Landmarks.check_id_img(real_id, image)
                        self.nested_dict[image]["ID"] = img_id
                    
                    next_line = file.readline()
                    if next_line.startswith("SCALE"):
                        scale = next_line.strip()
                        self.nested_dict[image]["SCALE"] = scale


        return self.lm_dict, self.img_list, self.nested_dict
    
    def write_xml(
            self, file, folder, name):

        """
        Write xml file from image and landmarks dictionary
        """
        self.xmlfile = file

        with open(self.xmlfile, 'w') as f:
            f.write(f"<?xml version='1.0' encoding='ISO-8859-1'?>\n")
            f.write(f"<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n")
            f.write(f"<dataset>\n")
            f.write(f"<name>Carabus pronotum {name}</name>\n")
            f.write(f"<images>\n")

            for img in self.img_list:
                image_path = os.path.join(folder, img)
                im = Image.open(image_path)
                width, height = im.size
                f.write(f"\t<image file='{image_path}' width='{int(width)}' height='{int(height)}'>\n")
                f.write(f"\t\t<box top='1' left='1' width='{int(width-2)}' height='{int(height-2)}'>\n")
                
                i = 0
                for lm in Landmarks.nested_dict[img]["LM"]:
                    f.write(f"\t\t\t<part name='{i}' x='{int(lm[0])}' y='{int(lm[1])}'/> \n")
                    i+=1
                f.write(f"\t\t</box>\n")
                f.write(f"\t</image>\n")

            f.write(f"</images>\n")
            f.write(f"</dataset>\n")
    
        return self.xmlfile



    def flip_image(
            self, img):

        # Read original image
        img_path = os.path.join(Landmarks.data_dir, img)
        original = Image.open(img_path)
        
        # Flip image
        vertical = original.transpose(method=Image.FLIP_TOP_BOTTOM)
        new_image = f'flip_{img}'
        new_imgpath = os.path.join(Landmarks.flip_dir, new_image)

        vertical.save(new_imgpath)

        return new_image
    
    def split_data(self, tag = ['train', 'test'], split_size = [0.7, 0.3]):

        """
        Splits data into 2 new xml files 
        """
        train_list = []
        test_list = []

        # We are not using folders
        train_xml = os.path.join(Landmarks.flip_dir, f'{tag[0]}.xml')
        test_xml = os.path.join(Landmarks.flip_dir, f'{tag[-1]}.xml')

        start_xml_file(train_xml, tag[0])
        start_xml_file(test_xml, tag[-1])

        # # Define a list of image extensions
        # image_extensions = ['.jpg', '.jpeg', '.png', '.bmp'] 
        # imgs_list = [filename for filename in os.listdir(train_folder) if os.path.splitext(filename)[-1] in image_extensions]

        random.shuffle(self.img_list) # comprobar seed

        train_size = int(len(self.img_list) * split_size[0])
        print(train_size)

        # Copy image files to each list
        # and append image to xml file
        for i, img in enumerate(self.img_list):
            # print(i)
            if i < train_size:
                file = train_xml
                train_list.append(img)
            else:
                file = test_xml
                test_list.append(img)
            
            # append to xml file
            append_to_xml_file(file, img, self.lm_dict, Landmarks.flip_dir)

        
        end_xml_file(train_xml)
        end_xml_file(test_xml)

        print('another split')
        return train_xml, test_xml, train_list



