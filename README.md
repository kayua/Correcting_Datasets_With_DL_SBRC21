# Correct Torrent Trace - Machine Learning

Algorithm for correcting sessions of users of large-scale peer-to-peer systems based on deep learning.
These scripts contain a complete framework that allows you to simulate, correct and evaluate session failures.
We made some initial experiments available with this repository.

## Free parameters:
    Parameters

        1 - Number of neurons per layers
        2 - Training optimization algorithm
        3 - Number epochs
        4 - Number neural layers
        5 - Dropout probability
        6 - Threshold of correction



## Input parameters:


                Correction of monitoring data - Machine learning 

    Optional Parameters

        --models                |  Define a template file saved as the current model.
        --original_swarm_file   |  Original input file.
        --training_swarm_file   |  File of training samples.
        --path_file_results     |  Path file results.
        --size_window_left      |  Size window left.
        --size_window_right     |  Size window right.
        --num_sample_training   |  Numbers samples to training.
        --corrected_swarm_file  |  File corrected.
        --failed_swarm          |  File failed swarm.
        --lstm_mode             |  Active LSTM mode.        
        --num_epochs            |  Number of training epochs.

        --------------------------------------------------------------

    Required Parameters

        Training         | This command allow training your model.
        Correct          | This command allow correct session.
        Predict          | This command is reserved for developers.
        Evaluation       | This command allow evaluation your model.
        help             | This command show this message.

## Requirements:

`matplotlib 3.4.1`
`tensorflow 2.4.1`
`tqdm 4.60.0`
`numpy 1.18.5`

`keras 2.4.3`
`setuptools 45.2.0`
`h5py 2.10.0`

