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
_To run the example commands `cd example`_



## 1. Training the Model

To train a model we need some images that already have annotated landmarks. For basic usage of `train.py` we need:  

- A '_.tps_' file with manually annotated landmarks (`-f, --input_file` option; e.g., [Carabus_pronotum_train.txt](example/Carabus_pronotum_train.txt))
- A directory containing the images referenced in the '_.tps_' file (`-i, --input_dir` option; e.g., [data](example/data))
- A name for the model (`-m, --model` option)

Additionally, we can specify the output directory (`--output_dir` option).

Therefore, the following command will generate a shape predictor model ([carabus.dat](example/carabus.dat)) that can be used to extract fixed landmarks on other _Carabus jasndo_ images.

```
./train.py --input_file example/Carabus_pronotum_train.txt --input_dir example/data --model carabus --output_dir example/ 
```

**Command Explanation**

```
usage: ./train.py -i DIR -m MODEL_BASENAME -f FILE [--model_version VERSION ] [--output_dir DIR ] [--params FILE] [--save_params]
```

**Input parameters**

* **`-f FILE`, `--input_file FILE`**

    &nbsp;&nbsp;&nbsp;&nbsp; Path to the input *[.tps / .txt](example/Carabus_pronotum_train.txt)* or *[.xml](example/all_data.xml)* file with annotated landmarks. Required

* **`-i DIR`, `--input_dir DIR`**

    &nbsp;&nbsp;&nbsp;&nbsp; Path to the input directory containing the training images. Required

* `--params FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; Path to a [_.txt_ file](example/params_carabus.txt) containing predefined hyperparameters for training the model. If not specified, the script will optimize hyperparameters automatically (this can be time-consuming)


**Output parameters**


* **`-m MODEL_BASENAME`, `--model MODEL_BASENAME`**

    &nbsp;&nbsp;&nbsp;&nbsp; Basename for output model file (without extension). Required

* `--model_version MODEL_VERSION`
  
     &nbsp;&nbsp;&nbsp;&nbsp; Specifies the version of the model. If not provided, the next available version will be used.

* `--ouput_dir DIR`

     &nbsp;&nbsp;&nbsp;&nbsp; Specifies where output files should be written. Default is current working directory.

* `--save_params`

     &nbsp;&nbsp;&nbsp;&nbsp; Save best found hyperparameters params in a new file [params_{model_name}.txt](example/params_carabus.txt) for future use e.g., when retraining a model with more images.


## 2. Predict landmarks

Once we have a trained model, we can use it to extract fixed landmarks on new images that depict the same biological structure. For basic usage, we need: 

-  A model file (`-m, --model` option; e.g., [carabus.dat](example/carabus.dat))

-  A directory containing the target images (`-i, --input_dir` option; e.g., [data](example/data))

Additionally, `predict.py` also takes as input one of the followings options: 

1. If all images are in the same scale, you can specify it with the `--scale` option and a _.tps_ blank file will be automatically generated. 

```
./predict.py --input_dir example/data --model example/carabus.dat --SCALE 0.000394 --output_dir example/
```

2. Otherwise, you should generate a [blank _.tps_ file](example/Carabus_pronotum_pred.txt) manually using TpsDIG and use the `-f, --input_file` option. _ask Danae and Giannis how to do this with TpsDIG_

```
./predict.py --input_dir example/data --model example/carabus.dat --input_file example/Carabus_pronotum_pred.txt --output_dir example/ 
```

**Command explanation**

Therefore, we can define two usages of `predict.py`

1. Defining a uniform scale for all images with `-s, --scale SCALE_FLOAT`

     ```
     usage: ./predict.py -i IMAGE_DIR -m FILE -s SCALE_FLOAT [--model_version MODEL_VERSION] [--output_dir OUTPUT_DIR] [--output OUTPUT] [--plot [none, dots, numbers]]
     ```

2. Using a *.txt / .tps* file as reference (option `-f, --input_file,` [Carabus_pronotum_pred.txt](example/Carabus_pronotum_pred.txt))

     ```
     usage: ./predict.py -i IMAGE_DIR -m FILE -f FILE [--model_version MODEL_VERSION] [--output_dir OUTPUT_DIR] [--output OUTPUT] [--plot [none, dots, numbers]]
     ```


**Input parameters**

* **`-i DIR`, `--input_dir DIR`,**
  
     &nbsp;&nbsp;&nbsp;&nbsp; Input directory containing the images for predicting. Required.

* **`-m FILE`, `--model FILE`**

     &nbsp;&nbsp;&nbsp;&nbsp; .dat file path of the LandmarkGen model. Required

Input options:
  
1. `-f FILE`, `--input_file FILE`

     &nbsp;&nbsp;&nbsp;&nbsp; .tps/.txt file with image names, scales and ID but no landmarks annotated. Required if scale is not defined.

2. `-s, --scale SCALE`

     &nbsp;&nbsp;&nbsp;&nbsp; Scale of all the images, all images must have the same scale. A .tps/.txt file will be generated using this scale and the input images.

**Output parameters**

* `--output_dir DIR`

    &nbsp;&nbsp;&nbsp;&nbsp;  Define working directory. By default it takes the current directory.

* `--output_file OUTPUT`

     &nbsp;&nbsp;&nbsp;&nbsp; Name of the output .tps/.txt file that will contain all predicted landmarks. By default it will take the model's name (*{model_name}_landmarks.txt*)
  
* `--plot [none, dots, numbers]`

     &nbsp;&nbsp;&nbsp;&nbsp; Plot landmarks on images with desired design. Original images will not be override, new images will be generated. 
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
