# Landmark Generator

### Lucía Martín Fernández
#

Shape Predictor Modeling algorithm to extract coordinates of fixed landmarks needed for shape analysis of biological structures. 

## Abstract

Geometric morphometrics is a powerful approach used in biological studies to analyze 
and compare the shape and form of biological structures in the context of evolutionary 
biology and ecology. This procedure includes landmark identification and digitization that serve as
reference points for further shape analysis. TpsDIG (Rohlf, F. J. 2006) is a software tool
designed for digitizing landmarks directly from digital images and obtaining the coordinates.
However, landmarks representing specific anatomical points are manually placed on the
images using tpsDIG or other tools by clicking on the specific points.

Biologists and entomologists typically need to perform this manual landmarking procedure
on hundreds to thousands of photographs, which can be tedious, labor-intensive, error-
prone, and time-consuming. To address this, our objective is to develop a shape predictor algorithm to yield species specific models
capable of extracting the coordinates of the fixed landmarks needed for shape
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
./predict.py -i example/data -m example/carabus.dat -f example/Carabus_pronotum_pred.txt -w example/ --plot numbers
```

The [example](example) folder contains the files required and generated after executing the commands above. 


## 1. Train model

```
usage: ./train.py -i DIR -m MODEL_NAME -f FILE [--model_version VERSION ] [--work_dir DIR ] [--params FILE] [--save_params]
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

To predict new landmarks we can execute `predict.py` in two ways:

- Using a *.txt / .tps* file as reference with *-f* (see example file [Carabus_pronotum_pred.txt](example/Carabus_pronotum_pred.txt))

     ```
     usage: ./predict.py -i IMAGE_DIR -m FILE [-f FILE] [--model_version MODEL_VERSION] [--work_dir WORK_DIR] [--output OUTPUT] [--plot [none, dots, numbers] ]
     ```

- Defining the scale of all the images with *-s SCALE* the needed *.txt / .tps*  file will be generated 

     ```
     usage: ./predict.py -i IMAGE_DIR -m FILE [-s SCALE] [--model_version MODEL_VERSION] [--work_dir WORK_DIR] [--output OUTPUT] [--plot]
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
     - `dots` will use red dots. Better aesthetics for publications
     - `numbers` will use color numbers. Useful for checking order of the coordinates
                                                           
## Other scripts

We also developed a series of scripts useful throughout the whole shape analysis. 

### `generate_tps.py`

Generates a landmarks-empty _.tps_ file with all the images in a directory. This is, a .tps file with LM=0 and ID, IMAGE and SCALE features. 

```
LM=0
IMAGE=Fc1045ind1.jpg
ID=FC1045IND1
SCALE=0.000394
```

This is script is useful to manually generate a blank _.tps_ file that serves as input for the `predict.py` program. However, this step is not necessary as `predict.py` can also generate a _.tps_ file when this is not specified as input (`--file`) but scale (`--scale`) is. 

**Arguments:**

* `-i DIR`, `--image_dir DIR`

     Directory with target images. Allowed image extensions are _.jpg, .jpeg, .png_ or _.bmp_
      Required. 


* `-s SCALE`, `--scale SCALE`

     Scale of all the images, all images must have the same scale.
  Required. 

* `-o FILE`, `--output FILE`

      Name of the output file. Recommended extensions are _.tps_ or _.txt_. Default is {image_dir}.tps


### `plot_landmarks.py`

Plot landmarks on images with desired design. Original images will not be override, new images will be generated and stored in a new directory. 

**Arguments:**

* `-i DIR`, `--image_dir DIR`,
  
     Input directory containing the reference images. Required.

* `-f FILE`, `--file FILE`

     .tps/.txt file with annotated landmarks. Required

* `--output OUTPUT`, `-o OUTPUT`

     Name of the output directory that will contain the new annotated images. By default it will take the input directory name (*annotated_{image_dir}*)
  
* `-d [dots, numbers]`, `--design [dots, numbers]`
      Choose design to plot the coordinates: 
     - `dots` will use red dots. Better aesthetics for publications. Default
     - `numbers` will use color numbers. Useful for checking order of the coordinates

### `delete_specimens.py`

Sometimes we need to remove some specimens from the tps file. Maybe because the automatically annotated landmarks are not accurate or because we don't want to consider this specimens for further analysis. This script will help you create a new _.tps_ file without the specified individuals. 

**Arguments:**

* `-i FILE`, `--input FILE`

     Reference _.tps_/_.txt_ file. Required

* `-l FILE`, `--list FILE`

     _.txt_ file that contains list of speciments to delete. Each item should be in a separate line. Required

* `-o OUTPUT`, `--output OUTPUT`

      Name of the output _.tps_ file. Recommended extensions are _.tps_ or _.txt_. Default is _clean_{input}.tps_


### `measure_error.py`

Predict test landmarks using the model and evaluate its performance by calculating the error. The measured error is included on the standard output.

**Arguments:**

* `-f FILE`, `--file FILE`

     Reference _.tps_/_.xml_ file that contains landmarks. Required

* `-i DIR`, `--image_dir DIR`

      Input directory containing the reference images. Required

* `-m FILE`, `--model_name FILE`

     _.dat_ file path of the  model. Required
  
* `-o OUTPUT`, `--output OUTPUT`

     Name of the output .tps/.txt file that will contain all predicted landmarks. By default it will take the model's name (*{model_name}_landmarks.txt*)


### _trial phase_`reorganize_coor.py`








## Requirements

Recommended Python modules versions:

* python==3.9.6
* dlib==19.24.4
* numpy==1.26.4 (dlib does not support numpy v2)

```
  python3 -m pip install numpy==1.26.4 
```

* matplotlib==3.9.1
* pillow==10.4.0

Other files: 

* `Config.py`. Can be modified by the user.
     - *PROCS* : Number of threads/cores we'll be using when training our models. -1 will also all available cores of the machine

     - *MAX_FUNC_CALLS* : Maximum number of trials we'll be performing when tuning our shape predictor hyperparameters. Higher numbers will result in better predictions but will also highly increase training time


## References 

Rohlf, F. J. (2006). tpsDig, Digitize Landmarks and Outlines, Version 2.10. Stony Brook, NY: Department of
Ecology and Evolution, State University of New York.

## Additional Notes

The program regenerates edited pictures for training and predicting that are deleted at the end of the execution. 
