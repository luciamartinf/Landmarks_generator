#!/usr/bin/env python3

import os
import sys
import dlib 
import random
import shutil
import numpy as np # numpy==1.26.4 because version 2 does not work with dlib
import matplotlib.pyplot as plt 
import xml.etree.ElementTree as ET
from PIL import Image
from utils import check_make_dir, start_xml_file, end_xml_file, append_to_xml_file, what_file_type
import utils
import reorganize_fun
import cv

class Landmarks:
    
    """A class use to process Landmarks"""

    data_dir = None # Original input directory
    flip_dir = None # directory with flip images and files that we are going to use
    work_dir = None # Working directory
    nested_dict = {} # Nested Dictionary with ID, SCALE and LM for every image (og_name)

    def __init__(self, 
                file, flip=True) -> None:
        
        """Constructs all necessary instance attributes"""

        # Initialize with an empty list or dictionary if no argument is provided
        self.img_list = []
        self.lm_dict = {}
        
        ext = what_file_type(file)

        if ext == '.xml':

            self.xmlfile = file
            self.lm_dict, self.img_list = self.read_xmlfile()
            

        elif ext in ['.tps', '.txt']:
            
            if Landmarks.check_forlm(file):
            
                self.txt_lmfile: str = file 
                self.lm_dict, self.img_list, Landmarks.nested_dict = self.readtxt_lmfile(flip=flip)
                
            else: 
            
                # predict with tps without landmarks
                # The input txt file does not contain the landmarks yet
                self.txt_imgfile: str = file
                self.img_list, Landmarks.nested_dict = self.readtxt_imgfile()
                
        else:
            
            sys.exit(2)
            

    @classmethod
    def create_flipdir(cls, name='work_data'):

        """Initializes flip_dir attribute and creates the directory it if it does not exist"""
        
        flip_dir = os.path.join(Landmarks.data_dir, name)
        check_make_dir(flip_dir)
        Landmarks.flip_dir = flip_dir

    @classmethod
    def del_flipdir(cls):
        
        """Delete Landmarks.flip_dir"""
        
        dir_path = Landmarks.flip_dir
        
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                print(f"Directory '{dir_path}' and all its contents have been deleted.")
            else:
                print(f"Directory '{dir_path}' does not exist.")
                
        except Exception as e:
            print(f"Error: {e}")

    
    @staticmethod
    def check_id_img(
        real_id, img_name):
        
        """Check that img_name and annotated id are the same

        Returns:
            img_id (str): Correct id for the image
        """

        # img_name es del tipo ind2784.jpg
        img_id = img_name.split('.')[0].upper() # The ID is like IND2934584

        if real_id != img_id:
            print(f"WARNING: ID={real_id} doesn't correspond to IMAGE={img_name}. Forcing ID to {img_id}")

        return img_id


    @staticmethod
    def check_forlm(
        file_name):

        """Checks if the txt files already contains the landmarks"""

        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith("LM"):
                    n_lm = int(line.strip().split('=')[1])
                    if n_lm == 0:
                        return False
                    else:
                        return True
 
        
    def readtxt_lmfile(self, flip=True):
        
        """Parse tps or txt file that contains landmarks
        
        Returns:
            self.lm_dict (Dict): Dictionary that contains flip_images (basename) as keys and landmarks as values
            self.img_list (List): List of flip_images (basename)
            Landmarks.nested_dict (Dict): Nested Dictionary with ID, SCALE and LM for every image (og_name)
        """
        check = False # If n_lm != 12, we dont consider that image
        with open(self.txt_lmfile, 'r') as file:
      
            for line in file:
                
                # Process expected line, "LANDMARKS" 
                if line.startswith("LM"):
                    lm_list = []
                    n_lm = int(line.strip().split('=')[1])
                    
                    if n_lm == 0:
                        print(f"WARNING: No landmarks annotated for this image. Skipping...")
                        check = True
                        # TODO
                        # HACER ALGO AL RESPECTO
                        # Hacer un count y si mas de x imagenes o porcentaje de imagenes no estan anotadas terminar el script
                    
                    # Read all the landmarks
                    else: 
                        i = 0
                        while i < n_lm:
                            landmark_line = next(file).strip().split() 
                            lm_list.append([float(landmark_line[0]), float(landmark_line[1])])
                            i+=1
                    
                    # if n_lm != 12: # TODO make generic, not 12
                    #     check = True
                    # else: 
                    #     check = False
                    
                elif line.startswith("IMAGE"):
                    image_name = str(line.strip().split('=')[1])
                        
                    # if check == True:
                    #     print(f'Image {image_name} has only {n_lm} landmarks annotated')
                        
                    if flip:
                        try:
                            # we are flipping the image and saving it in the dictionary we are going to work with  
                            image, image_path = self.flip_image(image_name) 
                        except Exception as e:
                            print(f"Error flipping image: {e}")
                            continue # Discard this image
                    else:
                        image = image_name
                        
                    if check == False:
                        self.lm_dict[image] = lm_list
                        self.img_list.append(image)
                        Landmarks.nested_dict[image_name] = {"LM": lm_list}
                    
                elif line.startswith("ID"):
                    real_id = str(line.strip().split('=')[1])
                    img_id = Landmarks.check_id_img(real_id, image_name)
                        
                    if check == False:
                        Landmarks.nested_dict[image_name]["ID"] = img_id
    
                # Process the next expected line, "SCALE"
        
                elif line.startswith("SCALE"):
                    scale = line.strip().split("=")[1]
                    if check == False:
                        Landmarks.nested_dict[image_name]["SCALE"] = scale
                
                else: 
                    print(f"Ignoring {line}")
                    continue
                
                

        return self.lm_dict, self.img_list, Landmarks.nested_dict


    def readtxt_imgfile(self):
        
        """Parse tps or txt file without landmarks
        
        Returns:
            self.img_list (List): List of flip_images (basename)
            Landmarks.nested_dict (Dict): Nested Dictionary with ID, SCALE and LM for every image (og_name)
        """
        
        with open(self.txt_imgfile, 'r') as file:
            
            for line in file:
                
                # Process expected line, "LM"
                if line.startswith("LM"):
                    n_lm = int(line.strip().split('=')[1])

                    if n_lm > 0:
                        print(f"WARNING: There are some Landmarks already annotated for this image")
                        # TODO HACER ALGO AL RESPECTO

                    
                elif line.startswith("IMAGE"):
                    image_name = str(line.strip().split('=')[1])
                        
                    try:
                        image, image_path = self.flip_image(image_name) # we are flipping the image and saving it in the dictionary we are going to work with  
                    except:
                        break
                        
                    self.img_list.append(image_name)
                    Landmarks.nested_dict[image_name] = {}
                    Landmarks.nested_dict[image_name]["LM"] = []
                    
                elif line.startswith("ID"):
                    real_id = str(line.strip().split('=')[1])
                    img_id = Landmarks.check_id_img(real_id, image_name)
                    Landmarks.nested_dict[image_name]["ID"] = img_id
                      
                elif line.startswith("SCALE"):
                    scale = line.strip().split("=")[1]
                    Landmarks.nested_dict[image_name]["SCALE"] = scale
                
                else: 
                    print(f"Ignoring {line}")
                    continue

        return self.img_list, Landmarks.nested_dict
    
    
    def read_xmlfile(self):
        
        """Parse images and ladmarks from xml file

        Returns:
            self.lm_dict (Dict): Dictionary that contains flip_images (basename) as keys and landmarks as values
            self.img_list (List): List of flip_images (basename)
        """
    
        tree = ET.parse(self.xmlfile)
        root = tree.getroot()

        for image in root.findall('.//image'):
            
            image_path = image.get('file')
            image_name = os.path.basename(image_path)
            self.img_list.append(image_name)
            self.lm_dict[image_name] = []
            
            for part in image.findall('.//part'):
                x = float(part.get('x'))
                y = float(part.get('y'))
                
                self.lm_dict[image_name].append([x,y])

        return self.lm_dict, self.img_list
    
    
    def write_xml(self, 
                  file, name):

        """Write xml file from image and landmarks dictionary"""
        
        self.xmlfile = file

        with open(self.xmlfile, 'w') as f:
            
            f.write(f"<?xml version='1.0' encoding='ISO-8859-1'?>\n")
            f.write(f"<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n")
            f.write(f"<dataset>\n")
            f.write(f"<name>Carabus pronotum {name}</name>\n")
            f.write(f"<images>\n")

            for img in self.img_list:
                
                image_path = os.path.join(Landmarks.flip_dir, img)
                im = Image.open(image_path)
                width, height = im.size
                
                f.write(f"\t<image file='{image_path}' width='{int(width)}' height='{int(height)}'>\n")
                f.write(f"\t\t<box top='1' left='1' width='{int(width-2)}' height='{int(height-2)}'>\n")
                
                i = 0
                for lm in self.lm_dict[img]:
                    
                    f.write(f"\t\t\t<part name='{i}' x='{int(lm[0])}' y='{int(lm[1])}'/> \n")
                    i+=1
                    
                f.write(f"\t\t</box>\n")
                f.write(f"\t</image>\n")

            f.write(f"</images>\n")
            f.write(f"</dataset>\n")
    
        return self.xmlfile


    def flip_image(self, 
                   img, save=True):
        
        """Flip images because landmarks' coordinates are flipped"""

        # Read original image
        img_path = os.path.join(Landmarks.data_dir, img)
        original = Image.open(img_path)
        
        # Flip image
        vertical = original.transpose(method=Image.FLIP_TOP_BOTTOM)
        new_image = f'flip_{img}'
        new_imgpath = os.path.join(Landmarks.flip_dir, new_image)

        if save:
            vertical.save(new_imgpath)

        return new_image, new_imgpath
    
    def split_data(self, 
                   tag = ['train', 'test'], split_size = [0.7, 0.3]):

        """Splits data in two sets"""

        train_list = []
        test_list = []

        train_xml = os.path.join(Landmarks.flip_dir, f'{tag[0]}.xml')
        test_xml = os.path.join(Landmarks.flip_dir, f'{tag[-1]}.xml')

        start_xml_file(train_xml, tag[0])
        start_xml_file(test_xml, tag[-1])

        random.shuffle(self.img_list)

        train_size = int(len(self.img_list) * split_size[0])
        print(f'Training with {train_size} images')

        # Add images to each list
        for i, img in enumerate(self.img_list):
            if i < train_size:
                file = train_xml
                train_list.append(img)
            else:
                file = test_xml
                test_list.append(img)
            
            # append image to corresponding xml file
            append_to_xml_file(file, img, self.lm_dict, Landmarks.flip_dir)

        end_xml_file(train_xml)
        end_xml_file(test_xml)

        return train_xml, test_xml
    
    def fold_data(self, train_index, test_index,
                   tag = ['train', 'test']):

        """Splits data in two folds"""

        train_list = []
        test_list = []

        train_xml = os.path.join(Landmarks.flip_dir, f'{tag[0]}.xml')
        test_xml = os.path.join(Landmarks.flip_dir, f'{tag[-1]}.xml')

        start_xml_file(train_xml, tag[0])
        start_xml_file(test_xml, tag[-1])


        train_size = len(train_index)
        print(f'Training with {train_size} images')

        # Add images to each list
        for i, img in enumerate(self.img_list):
            if i in train_index:
                file = train_xml
                train_list.append(img)
            elif i in test_index:
                file = test_xml
                test_list.append(img)
            
            # append image to corresponding xml file
            append_to_xml_file(file, img, self.lm_dict, Landmarks.flip_dir)

        end_xml_file(train_xml)
        end_xml_file(test_xml)

        return train_xml, test_xml
    

    def predict_landmarks(self, 
                          model_path, outfile, generate_images=False):
        
        """Predict new landmarks based on a model"""

        model_file = os.path.basename(model_path)
        model_name = model_file[:model_file.rindex('.')]

        landmarks_folder = os.path.join(Landmarks.work_dir, f'{model_name}_landmarks')
        
        check_make_dir(landmarks_folder)
        
        outpath = os.path.join(landmarks_folder, outfile)
        outpath = utils.check_file(outpath)


        for img in self.img_list:
            
            lm_array, image = self.predict_shape(model_path, img)
            
            
            lm_list = list(lm_array)
            
            if generate_images != 'none':
                
                self.plot_landmarks(image, img, lm_list, landmarks_folder, mode=generate_images)

            self.append_to_tps(img, lm_list, outpath)
      
        return outpath

    def calculate_error(self, 
                    model_path, file):
        
        """Predict new landmarks based on a model"""

        optimal_order = []
        all_mre = []
        all_mae = []
        
        for img, real_lm in self.lm_dict.items():
            
            pred_array, image = self.predict_shape(model_path, img)
            
            
            real_shape = np.array(real_lm)
            
            pred_shape, optimal_order = reorganize_fun.order_shape(real_shape, pred_array, optimal_order)
            
            mre = cv.measure_mre(real_shape, pred_shape)
            all_mre.append(mre)
            
            mae = cv.calculate_mae(real_shape, pred_shape)
            all_mae.append(mae)

        all_mre_array = np.array(all_mre)
        mean_mre = all_mre_array.mean()
        print("{} MRE of the model: {} is {}".format(
            os.path.basename(file), os.path.basename(model_path), mean_mre))
        
        all_mae_array = np.array(all_mae)
        mean_mae = all_mae_array.mean()
        print("{} MAE of the model: {} is {}".format(
            os.path.basename(file), os.path.basename(model_path), mean_mae))
    
        return all_mae_array, all_mre_array
        
    def predict_shape(self, dat, img):
        
        """Predict shape from image using a dlib's shape predictor"""
        
        if not 'flip' in img:
            img = f'flip_{img}'
        
        image_path = os.path.join(Landmarks.flip_dir, f'{img}')
        
        image = Image.open(image_path)
        np_image = np.array(image)
        width, height = image.size
            
        full_rect = dlib.rectangle(left=0, top=0, right=width, bottom=height)
        predictor = dlib.shape_predictor(dat)
        
        shape = predictor(np_image, full_rect)
        
        pred_lm = []
        for i in range(shape.num_parts):
            p = shape.part(i)
            if float(p.x) < 0 :
                print(f"WARNING: Image {img} may be cropped and negative landmarks are being generated. Changing {p.x} coordinate to 0")
                p.x = 0
            if float(p.y) < 0 :
                print(f"WARNING: Image {img} may be cropped and negative landmarks are being generated. Setting {p.y} coordinate to 0")
                p.y = 0
            pred_lm.append([p.x, p.y])
            
        return np.array(pred_lm), image
        
    def append_to_tps(self, img, lm_list, outpath):
        
        """Append image with landmarks to a .tps file"""
        
        with open(outpath, 'a') as f:
                
            f.write(f'LM={int(len(lm_list))}\n')
                
            for lm in lm_list:
                f.write(f'{lm[0]:.5f} {lm[1]:.5f}\n')
                
            f.write(f'IMAGE={img}\n')
            f.write(f'ID={Landmarks.nested_dict[img]["ID"]}\n')
            if "SCALE" in Landmarks.nested_dict[img].keys():
                f.write(f'SCALE={Landmarks.nested_dict[img]["SCALE"]}\n')
                

    def plot_landmarks(self, 
                       image, img_name, lm_list, folder, mode='dots'):
        
        """Plot landmarks in an image"""
        
        width, height = image.size
        
        plt.figure()
        plt.ylim(0, height)
        plt.xlim(0, width)
        plt.imshow(image)
        
        add = 0.025*width

        # Plot colored numbers
        if mode == 'numbers':
            for i, lm in enumerate(lm_list):
                plt.scatter(lm[0], lm[1], marker="$"+str(i+1)+"$")
                
        # Plot red dots
        elif mode == 'dots':
            for lm in lm_list:
                plt.plot(lm[0], lm[1], '.', color='red')
        
        elif mode == 'combo':
            for i, lm in enumerate(lm_list):
                plt.plot(lm[0], lm[1], '.', color='red')
                plt.scatter(lm[0]+add, lm[1], marker="$"+str(i+1)+"$")
                
        
        lm_img_path = os.path.join(folder, f'{img_name}')
        plt.savefig(lm_img_path)
        plt.close()
        
    def generate_images(self, mode='dots'):
        
        for img, lm_list in self.lm_dict.items():
            
            
            image_path = os.path.join(Landmarks.data_dir, f'{img}')
        
            original = Image.open(image_path)
            vertical = original.transpose(method=Image.FLIP_TOP_BOTTOM)
            
            self.plot_landmarks(vertical, img, lm_list, Landmarks.flip_dir, mode)
    
    
    def del_items(self, mylist):
        
        for img in mylist:
            
            try:
                # self.img_list.remove(img)
                del self.lm_dict[img]
            except:
                print(f'{img} was not found')
        
        return self.lm_dict
    
   