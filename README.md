# LandMarkgen

### Lucía Martín Fernández
#

Shape Predictor Model to extract coordinates of the most important landmarks needed for shape analysis of biological structures. 

## Abstract

Geometric morphometrics is a powerful approach used in biological studies to analyze 
and compare the shape and form of biological structures in the context of evolutionary 
biology and ecology. This procedure includes landmark identification and digitization that serve as
reference points for further shape analysis. TpsDIG (Rohlf, F. J. 2006) is a software tool
designed for digitizing landmarks directly from digital images and obtaining the coordinates.
However, landmarks representing specific anatomical points are manually placed on the
images using tpsDIG by clicking on the specific points.

Biologists and entomologists typically need to perform this manual landmarking procedure
on hundreds to thousands of photographs, which can be tedious, labor-intensive, error-
prone, and time-consuming. To address this, our objective is to develop a shape predictor model
that can extract the coordinates of the most important landmarks needed for shape
analysis of biological structures. 



## Usage Examples:

- **Step 1.** Train model from images

First we need to train a model with already annotated images. The following command will generate the shape predictor *carabus.dat*

```
./train.py -i example/data -m carabus -f example/Carabus_pronotum_train.txt -w example/ 
```

- **Step 2.** Predict other images with the model

Now, we can predict more Landmarks in different images using our *carabus.dat* model:

```
./predict.py -i example/data -m example/carabus.dat -f example/Carabus_pronotum_predict.txt -w example/ --plot numbers
```

The [example](example) folder contains the files required and generated after executing the commands above. 


## 1. Train model

**Option 1**

With `train.py`

```
usage: ./train.py -i DIR -m MODEL_NAME -f FILE [--model_version VERSION ] [--work_dir DIR ] [--params FILE] [--save_params]
```

**Option 2** (I will probably delete this)

With main script `landmarkgen.py`

```
Basic usage: ./landmarkgen.py train -i IMAGE_DIR -m MODEL_NAME -f FILE
```

With optional arguments
```
usage: python3 landmarkgen.py train -i IMAGE_DIR -m MODEL_NAME -f FILE [--model_version MODEL_VERSION] [--work_dir WORK_DIR] [--params PARAMS] [--save_params]
```

### Parameters 

* **`-i DIR`, `--image_dir DIR`,**
  
     Input directory containing the images for training. Required.

* **`-m MODEL_NAME`, `--model_name MODEL_NAME`**

     Name of the model (without extension). Required
  
* **`-f FILE`, `--file FILE`**

     *.tps* / *.txt* / *.xml* file with image names and their previously annotated landmarks. Required

#### Optional Parameters
   
* `--model_version VERSION`, `-mv VERSION`
  
     Version of the model. If the version already exists, next available version will be generated.

* `--work_dir DIR`, `-w DIR`

     Define working directory. By default it takes the current directory.

* `--params FILE`, `-p FILE`

     .txt file that contains already defined hyperparameters for training the model. If not defined, the program will look for the best hyperparameters in each case, but this will higly increase the training time. 

* `--save_params`, `-sp`

     Save best found hyperparameters params in a new file to reuse them when retraining the model e.g. with more images. See `--params FILE`


## 2. Predict Landmarks

**Option 1**

To predict new landmarks we can execute `predict.py` in two ways:

- Using a *.txt / .tps* file as reference with *-f* (see example file [Carabus_pronotum_pred.txt](example/Carabus_pronotum_pred.txt))

     ```
     usage: ./predict.py -i IMAGE_DIR -m FILE [-f FILE] [--model_version MODEL_VERSION] [--work_dir WORK_DIR] [--output OUTPUT] [--plot [none, dots, numbers] ]
     ```

- Defining the scale of all the images with *-s SCALE* the needed *.txt / .tps*  file will be generated 

     ```
     usage: ./predict.py -i IMAGE_DIR -m FILE [-s SCALE] [--model_version MODEL_VERSION] [--work_dir WORK_DIR] [--output OUTPUT] [--plot]
     ```

**Option 2** (I will probably delete this)

With main script `landmarkgen.py`

```
Basic usage: ./landmarkgen.py predict -i IMAGE_DIR -m MODEL_NAME -f FILE
```

With optional arguments
```
usage: python3 landmarkgen.py predict -i IMAGE_DIR -m MODEL_NAME -f FILE [--model_version MODEL_VERSION] [--work_dir WORK_DIR] [--params PARAMS] [--save_params]
```


### Parameters 

* **`-i DIR`, `--image_dir DIR`,**
  
     Input directory containing the images for predicting. Required.

* **`-m FILE`, `--model_name FILE`**

     .dat file path of the LandmarkGen model. Required
  
1. `-f FILE`, `--file FILE`

     .tps/.txt file with image names, scales and ID but no landmarks annotated. Required if scale is not defined.

2. `-s SCALE`, `--scale SCALE`

     Scale of all the images, all images must have the same scale. A .tps/.txt file will be generated using this scale and the input images.

#### Optional Parameters

* `--work_dir DIR`, `-w DIR`

     Define working directory. By default it takes the current directory.

* `--output OUTPUT`, `-o OUTPUT`

     Name of the output .tps/.txt file that will contain all predicted landmarks. By default it will take the model's name (*{model_name}_landmarks.txt*)
  
* `--plot [none, dots, numbers]`

     Plot landmarks on images with desired design. Original images will not be override, new images will be generated. 
     - Default is `none` and no images will be generated. 
     - `Dots` will use red dots. Better aesthetics for publications
     - `numbers` will use color numbers. Useful for checking order of the coordinates
                                                           

## Requirements

Recommended Python modules versions:

* python==3.9.6
* dlib==19.24.4
* numpy==1.26.4 (dlib does not support numpy==2)
  ` python3 -m pip install numpy==1.26.4 `
* matplotlib==3.9.1
* pillow==10.4.0

Other files: 

* `Config.py`. Can be modified by the user.
     - *PROCS* : Number of threads/cores we'll be using when training our models. -1 will also all available cores of the machine
     
     - *MAX_FUNC_CALLS* : Maximum number of trials we'll be performing when tuning our shape predictor hyperparameters. Higher numbers will result in better predictions but will also higly increase training time.

## References

Rohlf, F. J. (2006). tpsDig, Digitize Landmarks and Outlines, Version 2.10. Stony Brook, NY: Department of
Ecology and Evolution, State University of New York.
