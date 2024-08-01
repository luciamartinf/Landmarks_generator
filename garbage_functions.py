#!/usr/bin/env python3

import os
import sys
from Landmarks_module import Landmarks

def check_file_options(file):
    """
    Checks if a file exists and prompts the user for action if it does.
    """

    # Check if the file exists
    if os.path.isfile(file):
        # Enhanced error message
        print(f"WARNING: The file '{file}' already exists.")
        print("What do you want to do about it?")
        print("1. Override the existing file")
        print("2. Create a new version of the model")
        print("3. Exit training")

        # Get user input
        choice = input("Enter your choice (1/2/3): ")

        # Handle user choice
        if choice == '1':
            print(f"Overriding the existing file '{file}'...")
            # Remove the existing file
            os.remove(file)
            # Optionally create an empty file or handle accordingly
            open(file, 'a').close()
            print(f"File '{file}' has been overridden.")
        elif choice == '2':
            # Generate a new filename
            base, ext = os.path.splitext(file)
            new_file = base + "_new" + ext
            print(f"Creating a new version of the file '{new_file}'...")
            # Optionally create the new file or handle accordingly
            open(new_file, 'a').close()
            print(f"New version of the file '{new_file}' has been created.")
            return new_file
        elif choice == '3':
            print("Exiting training")
        else:
            print("Invalid choice. Going with default and creating a new version")
            sys.exit()
    else:
        print(f"Proceeding with training. Generating {file} model. ")
        


def rewrite_file(txt_lmfile):
    
    """
    Function to clean Landmarks input file
    """
    
    with open(txt_lmfile, 'r') as file:
        lines = file.readlines()
    
    new_file = 'Carabus_pronotumLM.txt'
    
    with open(new_file, 'w') as file:
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith("LM"):
                lm_list = []
                n_lm = int(line.split('=')[1])
                file.write(line+'\n')
                
                if n_lm == 0:
                    print("WARNING: No landmarks annotated for this image")
                    i += 1
                    continue
                
                i += 1
                for _ in range(n_lm):
                    lm = list(map(float, lines[i].strip().split()))
                    lm_list.append(lm)
                    file.write(lines[i])
                    i += 1
                
                if i < len(lines) and lines[i].startswith("IMAGE"):
                    image_name = lines[i].strip().split('=')[1]
                    file.write(lines[i])
                    
                    i += 1
                    if i < len(lines) and lines[i].startswith("ID"):
                        real_id = lines[i].strip().split('=')[1]
                        img_id = Landmarks.check_id_img(real_id, image_name)
                        file.write(f"ID={img_id}\n")
                    
                    i += 1
                    if i < len(lines) and lines[i].startswith("SCALE"):
                        file.write(lines[i])
                    
            i += 1


   # @staticmethod
    # def extract_image_list_from_xml(xml_file_path):
    #     # Parse the XML file
    #     tree = ET.parse(xml_file_path)
    #     root = tree.getroot()
        
    #     # Find all image elements and extract the file attribute
    #     images = root.findall('.//image')
    #     image_list = [os.path.basename(image.get('file')) for image in images]
        
    #     return image_list
    
    def check_for_negatives(self, model_path):

        """"
        Check for cropped images in the training set
        """
        
        total = len(self.img_list)
        per_10 = int(0.1 * total)

        for img in self.img_list:

            img_name = img.split('_')[1] # nos quedamos con ind429348.jpg

            image_path = os.path.join(self.flip_dir, img)

            image = Image.open(image_path)
            np_image = np.array(image)
            width, height = image.size
                
            full_rect = dlib.rectangle(left=0, top=0, right=width, bottom=height)
            predictor = dlib.shape_predictor(model_path)
            shape = predictor(np_image, full_rect)
            count = 0

            for i in range(shape.num_parts):
                p = shape.part(i)
                if float(p.x) < 0 :
                    print(f"WARNING: Image {img_name} may be cropped and negative landmarks are being generated. Excluding this picture from the training set")
                    # os.remove(image_path)
                    count +=1
                    break
                if float(p.y) < 0 :
                    print(f"WARNING: Image {img_name} may be cropped and negative landmarks are being generated. Setting {p.y} coordinate to 0")
                    # os.remove(image_path)
                    count +=1
                    break
            
            if count >= per_10:
                print("WARNING: More than the 10 percent of the images used in the training where cropped. Please try training the model again with the command: COMMAND")

if __name__ == "__main__":       
    
    rewrite_file('/Users/luciamf/Desktop/Landmarks_generator/Carabus_pronotumLANDMARKS.TXT')
    