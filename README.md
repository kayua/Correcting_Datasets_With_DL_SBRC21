# Correct Torrent Trace - Machine Learning

Algorithm for correcting sessions of users of large-scale peer-to-peer systems based on deep learning.
These scripts contain a complete framework that allows you to simulate, correct and evaluate session failures.
We made some initial experiments available with this repository.

## Free parameters:




## Input parameters:

                    Torrent Trace Correct - Machine Learning


    Optional Parameters(Main)

        --original_swarm_file     |  File of ground truth.
        --training_swarm_file     |  File of training samples.
        --corrected_swarm_file    |  File of correction
        --failed_swarm_file       |
        --analyse_file            |  Analyse results with statistics
        --analyse_file_mode       |  Open mode (e.g. 'w' or 'a')
        --model_architecture_file |  Full model architecture file
        --model_weights_file      |  Full model weights file
        --size_window_left        |
        --size_window_right       |
        --num_sample_training     |
        --num_epochs              |
        --threshold               |
        --dense_layers            |
        --pif                     |
        --dataset                 |
        --seed                    |
        --num_lstm_windows        |
        --lstm_mode               |
        --skip_train              |  Skip training of the machine learning model training
        --skip_correct            |  Skip correcting of the dataset
        --skip_analyse            |  Skip analyzing of the results
        --verbosity               |  Verbosity logging level 

        --------------------------------------------------------------

    Free Parameters

        1 - Number of neurons per layers
        2 - Training optimization algorithm
        3 - Number epochs
        4 - Number neural layers
        5 - Dropout probability
        6 - Threshold of correction

## Requirements:

`matplotlib 3.4.1`
`tensorflow 2.4.1`
`tqdm 4.60.0`
`numpy 1.18.5`

`keras 2.4.3`
`setuptools 45.2.0`
`h5py 2.10.0`

