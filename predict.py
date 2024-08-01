#!/usr/bin/env python3


from Landmarks_module import Landmarks
import os


def predict(image_dir, file, dat, output, gen_images=False):
    
    """Predict Landmarks from tps unannotated file and images

    Args:
        image_dir (Directory): Directory that contains images 
        file (File): tps unannotated file
        dat (File): Machine Learning model to predict landmarks
    """
    
    Landmarks.data_dir = os.path.abspath(image_dir)
    Landmarks.create_flipdir()
    data = Landmarks(file)
    data.predict_landmarks(dat, output, generate_images=gen_images)



def main():
    
    # TODO: Complete
    print("Predicting landmarks")
    

if __name__ == "__main__":
    main()      