# Landmark Generator

### Lucía Martín Fernández
#

Landmark Generator is a machine learning-based tool designed to automate the extraction of fixed landmark coordinates for the shape analysis of biological structures. 
This tool is particularly useful in the field of geometric morphometrics, where manual landmarking can be a tedious task. 

## Abstract

Geometric morphometrics is a powerful approach used in biological studies to analyze and compare the shape and form of biological structures in the context of evolutionary 
biology and ecology. 
This procedure includes landmark identification and digitization that serve as reference points for further shape analysis. 
TpsDIG (Rohlf, F. J. 2006) is a software tool designed for digitizing landmarks directly from digital images and obtaining the coordinates.
However, landmarks representing specific anatomical points are manually placed on the images using tpsDIG or other tools by clicking on the specific points.

Biologists typically need to perform this manual landmarking procedure on hundreds to thousands of photographs, which can be labor-intensive, error-prone, and time-consuming.

To address this, we developed a landmark generator program, a machine learning-based tool capable of generating a shape predictor model. 
With this model, we can then extract fixed landmarks coordinates in a standardized output format (.tps) for subsequent shape analysis of biological structures. 

## Table of Contents

...

## Requirements: 

- Python 3.9+
- Required Python packages are listed in [requirements.txt](requirements.txt).

¿Describe all Python packages here?


## Installation: 

1. Clone this repository to your local machine:

```
git clone https://github.com/luciamartinf/Landmarks_generator.git
cd landmark-generator
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```
or 
```
python3 -m pip install -r requirements.txt
```
or 
```
conda install --file requirements.txt
```


## Usage :

There are two main scripts that perform two different steps: 

- `train.py` is used for training a model with annotated images
- `predict.py` is used for extracting landmarks on new images.  


_The [example](example) directory contains some the files required and generated after running the examples commands._


### 1. Training the Model

To train a model we need some images that already have annotated landmarks. For basic usage of `train.py` we need:  

- A '_.tps_' file with manually annotated landmarks (`-f` option, see [Carabus_pronotum_train.txt](example/Carabus_pronotum_train.txt) as example)
- A directory containing the images referenced in the '_.tps_' file (`-i` option, see example [data](example/data) for an example dataset).
- A name for the model (`-m` option)

Therefore, the following command will generate a shape predictor model ([carabus.dat](example/carabus.dat)) that can be used to extract fixed landmarks on other _Carabus jasndo_ images.

```
./train.py -i example/data -m carabus -f example/Carabus_pronotum_train.txt -w example/ 
```

**Command Explanation**

```
usage: ./train.py -i DIR -m MODEL_NAME -f FILE [--model_version VERSION ] [--work_dir DIR ] [--params FILE] [--save_params]
```

**Input options**

* **`-f FILE`, `--file FILE`**

    &nbsp;&nbsp;&nbsp;&nbsp; Path to the input *[.tps / .txt](example/Carabus_pronotum_train.txt)* or *[.xml](example/all_data.xml)* file with annotated landmarks. Required

* **`-i DIR`, `--image_dir DIR`**

    &nbsp;&nbsp;&nbsp;&nbsp; Path to the input directory containing the training images. Required

* `--params FILE`, `-p FILE`

     Path to a [.txt file](example/params_carabus.txt) containing predefined hyperparameters for training the model. If not specified, the script will optimize hyperparameters automatically (this can be time-consuming)


**Output options**

* **`-m MODEL_NAME`, `--model_name MODEL_NAME`**

    &nbsp;&nbsp;&nbsp;&nbsp; Basename for output model file (without extension). Required

* `--model_version VERSION`, `-mv VERSION`
  
     Specifies the version of the model. If not provided, the next available version will be used.

* `--work_dir DIR`, `-w DIR`

     Specifies where output files should be written. Default is current working directory.

* `--save_params`, `-sp`

     Save best found hyperparameters params in a new file to reuse them when retraining the model e.g. with more images. See `--params FILE`


### 2. Predict landmarks in other images with the model

Now, we can predict more Landmarks in different images using our *carabus.dat* model:

```
./predict.py -i example/data -m example/carabus.dat -f example/Carabus_pronotum_pred.txt -w example/ --plot numbers
```



## 1. Train model




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


### *trial phase*`reorganize_coor.py`






## Requirements

**Python modules:**

* python==3.9.6
* dlib==19.24.4
* numpy==1.26.4 (dlib does not support numpy v2)

```
  python3 -m pip install numpy==1.26.4 
```

* matplotlib==3.9.1
* pillow==10.4.0

**Other files:** 

* `Config.py`. Can be modified by the user.
     - *PROCS* : Number of threads/cores we'll be using when training our models. -1 will also all available cores of the machine

     - *MAX_FUNC_CALLS* : Maximum number of trials we'll be performing when tuning our shape predictor hyperparameters. Higher numbers will result in better predictions but will also highly increase training time


## References 

Rohlf, F. J. (2006). tpsDig, Digitize Landmarks and Outlines, Version 2.10. Stony Brook, NY: Department of
Ecology and Evolution, State University of New York.

## Additional Notes

The program regenerates edited pictures for training and predicting that are deleted at the end of the execution. 
