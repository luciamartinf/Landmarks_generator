# Landmark Generator

### Lucía Martín Fernández
#

Landmark Generator is a machine learning-based tool designed to automate the extraction of fixed landmark coordinates for the shape analysis of biological structures. 
This tool is particularly useful in the field of geometric morphometrics, where manual landmarking can be a tedious task. 

## Abstract

Geometric morphometrics is a powerful approach used in biological studies to analyze and compare the shape and form of biological structures in the context of evolutionary 
biology and ecology. 
This procedure includes landmark identification and digitization that serve as reference points for further shape analysis. 
TpsDIG is a software tool designed for digitizing landmarks directly from digital images and obtaining the coordinates.
However, landmarks representing specific anatomical points are manually placed on the images using tpsDIG or other tools by clicking on the specific points.

Biologists typically need to perform this manual landmarking procedure on hundreds to thousands of photographs, which can be labor-intensive, error-prone, and time-consuming.

To address this, we developed a landmark generator program, a machine learning-based tool capable of generating a shape predictor model. 
With this model, we can then extract fixed landmarks coordinates in a standardized output format (*.tps) for subsequent shape analysis of biological structures. 

## Table of Contents

...

## Requirements: 

- Python 3.9+

**Python modules:**

Required Python packages are also listed in [requirements.txt](requirements.txt).

* dlib==19.24.4
     - CMake is necessary to install dlib. *link to install cmake*  (directly from cmake.org, the binary version for windows) 
* numpy==1.26.4 (dlib does not support numpy v2)
* matplotlib==3.9.1
* pillow==10.4.0
* scipy>=1.13.1
* scikit-learn>=1.6.1



## Installation: 

1. Install CMake, Python and Git. 

2. Clone this repository to your local machine:

     ```
     git clone https://github.com/luciamartinf/Landmarks_generator.git
     cd Landmarks-generator/
     ```

3. Install the required dependencies:

     ```
     pip install -r requirements.txt
     ```
     or 
     ```
     conda create -n dlib python=3.9.6
     conda activate dlib
     conda config --append channels conda-forge
     conda install --file requirements.txt
     ```


## Usage :

There are two main scripts that perform two different steps: 

- `train.py` is used for training a model with annotated images
- `predict.py` is used for extracting landmarks on new images.  



## 1. Training the Model

To train a model we need some images that already have annotated landmarks. For basic usage of `train.py` we need:  

- A '_*.tps_' file with manually annotated landmarks (`-f, --input_file` option; e.g., [Carabus_pronotum_train.txt](example_carabus/Carabus_pronotum_train.txt))
- A directory containing the images referenced in the '_*.tps_' file (`-i, --input_dir` option; e.g., [images](example_carabus/images)). Allowed image file formats are _.jpg, .jpeg, .png, .tiff_ or _.bmp_.
- A name for the model (`-m, --model` option)

Additionally, we can specify the output directory (`--output_dir` option).

Therefore, the following command will generate a shape predictor model ([carabus.dat](example_carabus/carabus.dat)) that can be used to extract the fixed landmarks from other _Carabus banonii_ images.

```
python train.py --input_file example_carabus/Carabus_pronotum_train.txt --input_dir example_carabus/images --model carabus --output_dir example_carabus/ 
```

**Input parameters**

* **`-f FILE`, `--input_file FILE`**

    &nbsp;&nbsp;&nbsp;&nbsp; Path to the input *[.tps / .txt](example_carabus/Carabus_pronotum_train.txt)* or *[.xml](example_carabus/all_data.xml)* file with annotated landmarks. Required

* **`-i DIR`, `--input_dir DIR`**

    &nbsp;&nbsp;&nbsp;&nbsp; Path to the input directory containing the training images. Allowed image file formats are _.jpg, .jpeg, .png, .tiff_ or _.bmp_. Required

* `--params FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to a _.txt_ file containing predefined hyperparameters for training the model (e.g., [params_carabus.txt](example_carabus/params_carabus.txt)). 
     &nbsp;&nbsp;&nbsp;&nbsp; If not specified, the script will optimize hyperparameters automatically. Take into consideration that this can be time-consuming. 


**Output parameters**


* **`-m MODEL_BASENAME`, `--model MODEL_BASENAME`**

    &nbsp;&nbsp;&nbsp;&nbsp; Basename for output model file (without extension). Required

* `--model_version MODEL_VERSION`
  
     &nbsp;&nbsp;&nbsp;&nbsp; Define version of the model manually. If not provided, the next available version will be used.

* `--ouput_dir DIR`

     &nbsp;&nbsp;&nbsp;&nbsp; Specifies where output files will be written. Default is current working directory.

* `--save_params`

     &nbsp;&nbsp;&nbsp;&nbsp; Save optimized hyperparameters in a new '[params_{model_name}.txt](example_carabus/params_carabus.txt)' file for future use e.g., when retraining a model with more images.

**Configuration file** 

`Config.py`. Can be modified by the user.

     - *PROCS* : Number of threads we'll be using when training our models. -1 will also all available cores of the machine minus 1

     - *MAX_FUNC_CALLS* : Maximum number of trials we'll be performing when tuning our shape predictor hyper-parameters. Higher numbers will result in better predictions but will also highly increase training time

     - *KFOLDS: Number of folds of the training set on each of the tuning calls. 


## 2. Predict landmarks

Once we have a trained model, we can use it to extract fixed landmarks on new images that depict the same biological structure. For basic usage, we need: 

-  A model file (`-m, --model` option; e.g., [carabus.dat](example_carabus/carabus.dat))

-  A directory containing the target images (`-i, --input_dir` option; e.g., [images](example_carabus/images))

Additionally, `predict.py` also takes as input one of the followings options: 

1. If all images are in the same scale, the user can use the `--scale` option and a landmarks-empty _*.tps_ file will be automatically generated. 

```
python predict.py --input_dir example_carabus/images --model example_carabus/carabus.dat --scale 0.000394 --output_dir example_carabus/
```

2. Otherwise, a landmarks-empty _*.tps*_ file (e.g., [Carabus_pronotum_pred.txt](example_carabus/Carabus_pronotum_pred.txt)) should be generated manually using TpsDIG. The user can then specify  the input with the `-f, --input_file` option. _ask Danae and Giannis how to do this with TpsDIG_

```
python predict.py --input_dir example_carabus/images --model example_carabus/carabus.dat --input_file example_carabus/Carabus_pronotum_pred.txt --output_dir example_carabus/ 
```


**Input parameters**

* **`-i DIR`, `--input_dir DIR`,**
  
     &nbsp;&nbsp;&nbsp;&nbsp; Input directory containing the target images. Allowed image file formats are _.jpg, .jpeg, .png, .tiff_ or _.bmp_. Required.

* **`-m FILE`, `--model FILE`**

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the trained model; e.g., a _.dat_ file like [carabus.dat](example_carabus/carabus.dat). Required

Moreover, depending on the input data, the user needs to choose one of the following input options:

1. **`-s, --scale SCALE_FLOAT`**

     &nbsp;&nbsp;&nbsp;&nbsp; Specify an uniform scale for all images in the input directory. When using this option, all images must have the same scale.
     
     &nbsp;&nbsp;&nbsp;&nbsp; The script will automatically generate a landmarks-empty *.tps* file: 'input_{input_dir}.tps'


2. **`-f FILE`, `--input_file FILE`**

     &nbsp;&nbsp;&nbsp;&nbsp; Provide a reference landmarks-empty _*.tps_ file (e.g.,  [Carabus_pronotum_pred.txt](example_carabus/Carabus_pronotum_pred.txt)). 
     &nbsp;&nbsp;&nbsp;&nbsp; This option is required when the images in the input directory don't have the same scale.


**Output parameters**

* `--output_dir DIR`

    &nbsp;&nbsp;&nbsp;&nbsp; Specifies where output files will be written. Default is current working directory.

* `--output_file OUTPUT`

     &nbsp;&nbsp;&nbsp;&nbsp; Name of the output _*.tps_ file that will contain all predicted landmarks. 
     &nbsp;&nbsp;&nbsp;&nbsp; By default it will use the model name as '{model_basename}_landmarks.tps' (e.g., [carabus_landmarks.tps](example_carabus/carabus_landmarks/carabus_landmarks.tps).
  
* `--plot [none, dots, numbers]`

     &nbsp;&nbsp;&nbsp;&nbsp; Option to visualize landmarks on images. Original images will not be override as new images will be generated. The user can choose between the following `--plot` options:
     - `none`: No visualization (default).
     - `dots`: Red dots for aesthetic visualization. 
     - `numbers`: Colored numbers for verification of landmark's order. 
     - `combo`: Red dots + colored numbers. 
                                                           
## Other scripts

We also developed a series of scripts useful throughout the whole shape analysis. 

#### `delete_specimens.py`

Sometimes we need to remove some specimens entry from a **.tps* file. Maybe because the automatically annotated landmarks are not accurate or because we don't want to consider these specimens for further analysis. This script will help the user to create a new _*.tps_ file without the specified individuals. To do this, the user needs to create a _.txt_ file containing a line-separated list of the images to delete (e.g., [del_list.txt](example_carabus/del_list.txt)). 

**Usage**

````
python delete_specimens.py -f INPUT_FILE -l FILE_LIST [-o OUTPUT]
````


**Arguments:**

* `-f FILE`, `--input_file FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the reference _*.tps_ file. Required

* `-l FILE`, `--input_list FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to a _.txt_ file containing a line-separated list of the images to remove from the _*.tps_ file. Required

* `-o OUTPUT`, `--output OUTPUT`

     &nbsp;&nbsp;&nbsp;&nbsp; Name of the output _*.tps_ file. Recommended extensions are _*.tps_ or _.txt_. 
     &nbsp;&nbsp;&nbsp;&nbsp; By default it will take the input file name as '*clean_{input_filename}.tps*'



#### `generate_tps.py`

This script generates a landmarks-empty _*.tps_ file with all the images in a directory. This is a _*.tps_ file with LM=0 and ID, IMAGE and SCALE features that looks as:

```
LM=0
IMAGE=Fc1045ind1.jpg
ID=FC1045IND1
SCALE=0.000394
...
```
This script is useful to manually generate a landmarks-empty _*.tps_ file that serves as input for the `predict.py` script. However, this step is not necessary as `predict.py` can also generate a _*.tps_ file with the `--scale` option. 

**Usage**
```
python generate_tps.py -i INPUT_DIR --scale SCALE_FLOAT [-o OUTPUT]
```
All images must have been taken with the same scale. If scale is not provided as an argument, the program will use scale=1, so no scaling will be applied in the downstream analysis. 

**Arguments:**

* `-i DIR`, `--input_dir DIR`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the input directory containing the target images. Allowed image file formats are _.jpg, .jpeg, .png, .tiff_ or _.bmp_. Required. 


* `-s SCALE`, `--scale SCALE_FLOAT`

     &nbsp;&nbsp;&nbsp;&nbsp; Specify the scale of the images in the input directory. All images must have the same scale. 

* `-o OUTPUT`, `--output OUTPUT`

     &nbsp;&nbsp;&nbsp;&nbsp; Name of the output _*.tps_ file. Recommended file formats are _*.tps_ or _.txt_. 
     &nbsp;&nbsp;&nbsp;&nbsp; By default it will use the input directory name as '{input_dir}.tps' 


#### `plot_landmarks.py`

Script to visualize landmarks on images. Original images will not be override as new images will be generated. The user can choose between the following `--design` options:
- `dots`: Red dots for aesthetic visualization. 
- `numbers`: Colored numbers for verification of landmark's order. 
- `combo`: Red dots + colored numbers. 


**Usage**
```
python plot_landmarks.py -f FILE -i INPUT_DIR [-o OUTPUT] [--design {dots,numbers}]
```

**Arguments:**

* `-f FILE`, `--input_file FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the input **.tps* file with annotated landmarks. Required

* `-i DIR`, `--input_dir DIR`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the input directory containing the target images. Allowed image file formats are _.jpg, .jpeg, .png, .tiff_ or _.bmp_. Required. 

* `-o OUTPUT, --output OUTPUT`, 

     &nbsp;&nbsp;&nbsp;&nbsp; Name of the output directory that will contain the new annotated images. 
     &nbsp;&nbsp;&nbsp;&nbsp; By default it will take the input directory name as '*annotated_{image_dir}*'
  
* `--design [dots, numbers]`
     
     &nbsp;&nbsp;&nbsp;&nbsp; Option to choose how to visualize landmarks. Available designs are: 
     - `dots`: Red dots for aesthetic visualization. 
     - `numbers`: Colored numbers for verification of landmark's order. 


#### `measure_error.py`

This script is used to evaluate the performance of a trained model. It takes as input a manually generated _*.tps_ file and generates landmarks with the trained model. It then compares the manual and the automatic landmarks to calculate the mean relative error (MRE) and the mean absolute error (MAE) that are included on the standard output. 

**Usage**

```
python measure_error.py -f INPUT_FILE -i INPUT_DIR -m MODEL 
```
**example_carabus**
```
python measure_error.py -f example_carabus/all_data.xml -i example_carabus/images -m example_carabus/carabus.dat 
```

**Arguments:**

* `-f FILE`, `--input_file FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the input _.xml_ file containing manually annotated landmarks. Required. 

* `-i DIR`, `--input_dir DIR`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the input directory containing the reference images. Allowed image file formats are _.jpg, .jpeg, .png, .tiff_ or _.bmp_. Required. 

* `-m FILE`, `--model FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to the trained model, a _.dat_ file like [carabus.dat](example_carabus/carabus.dat). Required.


## Additional Notes

The program regenerates edited pictures for training and predicting that are deleted at the end of the execution. 

## *.tps file

Tps files are test files in of the standard formats for geometric morphometrics (see Rohlf 2010). This program supports two-dimensional landmarks coordinates designated by the identifier "LM=". 

This program reads 'LM=', 'IMAGE=', 'ID=' and 'SCALE=' fields, all other information that can be contained in tps files (comments, variables, radii, etc.) is ignored.


Landmarks coordinates are multiplied by their scale factor if this is provided for all specimens. If one or more specimens are missing the scale factor, landmarks are treated in their original units. 

_If no scale is provided, we can leave the scale space empty in the file and give an appropiate warning message_
