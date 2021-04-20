# Correcting Datasets - Deep Learning (SBRC21)

Algorithm for correcting sessions of users of large-scale peer-to-peer systems based on deep learning.



## Input parameters:

Torrent Trace Correct - Machine Learning


    Arguments(run_SBRC21.py):
        
        -h, --help              |   Show this help message and exit
        --output                |   Full name of the output file with analysis results (default=sbrc21.txt)
        --append                |   Append output logging file with analysis results (default=False)
        --trials                |   Number of trials (default=1)
        --start_trials          |   Start trials (default=0)
        --skip_train            |   Skip training of the machine learning model training?
        --campaign              |   Campaign [demo, sbrc21] (default=demo)
        --verbosity             |   Verbosity logging level (INFO=20 DEBUG=10)

    --------------------------------------------------------------
   
    Arguments(main.py):

        -h,--help                 |   Show this help message and exit
        --original_swarm_file     |   File of ground truth.
        --training_swarm_file     |   File of training samples
        --corrected_swarm_file    |   File of correction
        --failed_swarm_file       |   File of failed swarm
        --analyse_file            |   Analyse results with statistics
        --analyse_file_mode       |   Open mode (e.g. 'w' or 'a')
        --model_architecture_file |   Full model architecture file
        --model_weights_file      |   Full model weights file
        --num_epochs              |   Number of epochs
        --threshold               |   i.e. alpha (e.g. 0.5 - 0.95)
        --dense_layers            |   Number of dense layers (e.g. 1, 2, 3)
        --pif PIF                 |   pif (only for statistics)
        --dataset DATASET         |   Dataset (only for statistics)
        --seed SEED               |   Seed (only for statistics)
        --skip_train, -t          |   Skip training of the machine learning model training?
        --skip_correct, -c        |   Skip correcting of the dataset?
        --skip_analyse, -a        |   Skip analyzing of the results?
        --verbosity VERBOSITY, -v |   Verbosity logging level (INFO=20 DEBUG=10)


        --------------------------------------------------------------

#  Run:
`Python2 run_sbrc21.py -c sbrc`


## Requirements:

`matplotlib 3.4.1`
`tensorflow 2.4.1`
`tqdm 4.60.0`
`numpy 1.18.5`

`keras 2.4.3`
`setuptools 45.2.0`
`h5py 2.10.0`

