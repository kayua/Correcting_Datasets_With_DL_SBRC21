# Correcting Datasets - Deep Learning (SBRC21)

Algorithm for correcting sessions of users of large-scale peer-to-peer systems based on deep learning.
These scripts contain a complete framework that allows you to simulate, correct and evaluate session failures.
We made some initial experiments available with this repository.

## Free parameters:




## Input parameters:

                    Correcting Datasets - Machine Learning


    Parameters
        
        --original_swarm_file     |  File of ground truth
        --training_swarm_file     |  File of training samples
        --corrected_swarm_file    |  File of correction
        --failed_swarm_file       |  File of failed swarm
        --analyse_file            |  Analyse results with statistics
        --analyse_file_mode       |  Open mode (e.g. 'w' or 'a')
        --model_architecture_file |  Full model architecture file
        --model_weights_file      |  Full model weights file
        --size_window_left        |  Size window left
        --size_window_right       |  Size window right
        --num_sample_training     |  Number of samples training
        --num_epochs              |  Number of epochs training
        --threshold               |  Thresould of correction
        --dense_layers            |  Number of dense layers
        --pif                     |  pif (only for statistics)
        --dataset                 |  Dataset (only for statistics)
        --seed                    |  Seed (only for statistics)
        --skip_train              |  Skip training
        --skip_correct            |  Skip correcting of the dataset
        --skip_analyse            |  Skip analyzing of the results
        --verbosity               |  Verbosity logging level 

        --------------------------------------------------------------


## Requirements:

`matplotlib 3.4.1`
`tensorflow 2.4.1`
`tqdm 4.60.0`
`numpy 1.18.5`

`keras 2.4.3`
`setuptools 45.2.0`
`h5py 2.10.0`

