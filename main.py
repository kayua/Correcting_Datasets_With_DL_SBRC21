#!/usr/bin/python3
# -*- coding: utf-8 -*-

from analyse import Analyse
from dataset import Dataset
from models.models import Neural

try:

    import sys
    from tqdm import tqdm
    import argparse
    import logging

except ImportError as error:

    print(error)
    print()
    print("1. (optional) Setup a virtual environment: ")
    print("  python3 - m venv ~/Python3env/mltraces ")
    print("  source ~/Python3env/mltraces/bin/activate ")
    print()
    print("2. Install requirements:")
    print("  pip3 install --upgrade pip")
    print("  pip3 install -r requirements.txt ")
    print()
    sys.exit(-1)

DEFAULT_ORIGINAL_SWARM_FILE = 'swarm/original/S1d.sort_u_1n_3n'
DEFAULT_TRAINING_SWARM_FILE = 'swarm/training/S2_25.sort_u_1n_3n'
DEFAULT_CORRECTED_SWARM_FILE = 'swarm/results/swarm.corrected'
DEFAULT_FAILED_SWARM_FILE = "swarm/failed/S1d.sort_u_1n_3n.fail10_seed1"
DEFAULT_VALIDATION_SWARM_FILE = "swarm/validation/S1_25.sort_u_1n_3n"
DEFAULT_OUTPUT_EVOLUTION_ERROR_FIGURES = "evolution/"
DEFAULT_MODEL_ARCHITECTURE_FILE = "models_saved/model_architecture.json"
DEFAULT_MODEL_WEIGHTS_FILE = "models_saved/model_weights.h5"

DEFAULT_OPTIMIZER = 'adam'
DEFAULT_FUNCTION_LOSS = 'mean_squared_error'

DEFAULT_SIZE_WINDOW_LEFT = 5
DEFAULT_SIZE_WINDOW_RIGHT = 5
DEFAULT_NUMBER_SAMPLES_TRAINING = 20000
DEFAULT_NUMBER_SAMPLES = 160
DEFAULT_NUMBER_EPOCHS = 15
DEFAULT_THRESHOLD = 0.75
DEFAULT_DENSE_LAYERS = 3
DEFAULT_LEARNING_PATTERNS_PER_ID = False
DEFAULT_VERBOSITY_LEVEL = logging.INFO
TIME_FORMAT = '%Y-%m-%d,%H:%M:%S'
DEFAULT_ANALYSE_FILE = "analyse.txt"
DEFAULT_ANALYSE_FILE_MODE = "a"


def analyse(args):

    analise_results = Analyse(args.original_swarm_file, args.corrected_swarm_file, args.failed_swarm_file,
                              args.analyse_file, args.analyse_file_mode,
                              args.dense_layers, args.threshold, args.pif, args.dataset, args.seed)

    analise_results.run_analise()
    analise_results.write_results_analyse()


def training_neural_network(args):

    neural_network = Neural(DEFAULT_SIZE_WINDOW_LEFT, DEFAULT_SIZE_WINDOW_RIGHT,
                            DEFAULT_NUMBER_SAMPLES, args.threshold, DEFAULT_NUMBER_EPOCHS,
                            DEFAULT_LEARNING_PATTERNS_PER_ID, DEFAULT_OPTIMIZER,
                            DEFAULT_FUNCTION_LOSS, args.dense_layers, DEFAULT_OUTPUT_EVOLUTION_ERROR_FIGURES)
    neural_network.create_neural_network()

    dataset_file = Dataset(DEFAULT_SIZE_WINDOW_LEFT, DEFAULT_SIZE_WINDOW_RIGHT, DEFAULT_NUMBER_SAMPLES,
                           args.corrected_swarm_file)

    dataset_file.load_samples(args.original_swarm_file)
    dataset_file.create_list_per_peer()
    dataset_file.clear_samples()
    dataset_file.fill_gaps()
    dataset_file.fill_borders()

    dataset_file_validation = Dataset(DEFAULT_SIZE_WINDOW_LEFT, DEFAULT_SIZE_WINDOW_RIGHT, DEFAULT_NUMBER_SAMPLES,
                                      DEFAULT_VALIDATION_SWARM_FILE)

    dataset_file_validation.load_samples(DEFAULT_VALIDATION_SWARM_FILE)
    dataset_file_validation.create_list_per_peer()
    dataset_file_validation.clear_samples()
    dataset_file_validation.fill_gaps()
    dataset_file_validation.fill_borders()

    x, y = dataset_file.get_training_samples()
    x_validation, y_validation = dataset_file_validation.get_training_samples()

    neural_network.fit(x, y, x_validation, y_validation)
    neural_network.save_models(args.model_architecture_file, args.model_weights_file)


def predict_neural_network(args):

    neural_network = Neural(DEFAULT_SIZE_WINDOW_LEFT, DEFAULT_SIZE_WINDOW_RIGHT,
                            DEFAULT_NUMBER_SAMPLES, args.threshold, DEFAULT_NUMBER_EPOCHS,
                            DEFAULT_LEARNING_PATTERNS_PER_ID, DEFAULT_OPTIMIZER,
                            DEFAULT_FUNCTION_LOSS, args.dense_layers, DEFAULT_OUTPUT_EVOLUTION_ERROR_FIGURES)

    neural_network.load_models(args.model_architecture_file, args.model_weights_file)

    dataset_file = Dataset(DEFAULT_SIZE_WINDOW_LEFT, DEFAULT_SIZE_WINDOW_RIGHT, DEFAULT_NUMBER_SAMPLES,
                            args.corrected_swarm_file)
    dataset_file.load_samples(args.failed_swarm_file)
    dataset_file.create_list_per_peer()
    dataset_file.fill_gaps()
    dataset_file.fill_borders()
    dataset_file.create_file_results()

    for i in tqdm(range(dataset_file.get_number_peers()), desc='Predicting'):

        x, y = dataset_file.create_windows_per_peer(i)
        saida_x = neural_network.predict(x)
        dataset_file.write_swarm(saida_x)

    dataset_file.output_file.close()


def print_config(args):

    logging.info("Command:\n\t{0}\n".format(" ".join([x for x in sys.argv])))
    logging.info("Settings:")

    for k, v in sorted(vars(args).items()):

        logging.info("\t{0}: {1}".format(k, v))

    logging.info("")


def main():

    parser = argparse.ArgumentParser(description='Torrent Trace Correct - Machine Learning')

    help_msg = 'File of ground truth.'
    parser.add_argument("--original_swarm_file", type=str, help=help_msg, default=DEFAULT_ORIGINAL_SWARM_FILE)

    help_msg = ''
    parser.add_argument("--training_swarm_file", type=str, help=help_msg, default=DEFAULT_TRAINING_SWARM_FILE)

    help_msg = ''
    parser.add_argument("--corrected_swarm_file", type=str, help=help_msg, default=DEFAULT_CORRECTED_SWARM_FILE)

    help_msg = ''
    parser.add_argument("--failed_swarm_file", type=str, help=help_msg, default=DEFAULT_FAILED_SWARM_FILE)

    help_msg = 'analyse results with statistics'
    parser.add_argument("--analyse_file", type=str, help=help_msg, default=DEFAULT_ANALYSE_FILE)

    help_msg = "open mode (e.g. 'w' or 'a')"
    parser.add_argument("--analyse_file_mode", type=str, help=help_msg, default=DEFAULT_ANALYSE_FILE_MODE)

    help_msg = 'full model architecture file'
    parser.add_argument("--model_architecture_file", type=str, help=help_msg, default=DEFAULT_MODEL_ARCHITECTURE_FILE)

    help_msg = 'full model weights file'
    parser.add_argument("--model_weights_file", type=str, help=help_msg, default=DEFAULT_MODEL_WEIGHTS_FILE)

    help_msg = ''
    parser.add_argument("--size_window_left", type=int, help=help_msg, default=DEFAULT_SIZE_WINDOW_LEFT)

    help_msg = ''
    parser.add_argument("--size_window_right", type=int, help=help_msg, default=DEFAULT_SIZE_WINDOW_RIGHT)

    help_msg = ''
    parser.add_argument("--num_sample_training", type=int, help=help_msg, default=DEFAULT_NUMBER_SAMPLES_TRAINING)

    help_msg = ''
    parser.add_argument("--num_epochs", type=int, help=help_msg, default=DEFAULT_NUMBER_EPOCHS)

    help_msg = ' i.e. alpha (e.g. 0.5 - 0.95)'
    parser.add_argument("--threshold", type=float, help=help_msg, default=DEFAULT_THRESHOLD)

    help_msg = ' number of dense layers (e.g. 1, 2, 3)'
    parser.add_argument("--dense_layers", type=int, help=help_msg, default=DEFAULT_DENSE_LAYERS)

    help_msg = ' pif (only for statistics)'
    parser.add_argument("--pif", type=float, help=help_msg, default=0.10)

    help_msg = ' dataset (only for statistics)'
    parser.add_argument("--dataset", type=str, help=help_msg, default="Sxxx")

    help_msg = ' seed (only for statistics)'
    parser.add_argument("--seed", type=int, help=help_msg, default=1)

    help_msg = "Skip training of the machine learning model training?"
    parser.add_argument("--skip_train", "-t", default=False, help=help_msg, action='store_true')

    help_msg = "Skip correcting of the dataset?"
    parser.add_argument("--skip_correct", "-c", default=False, help=help_msg, action='store_true')

    help_msg = "Skip analyzing of the results?"
    parser.add_argument("--skip_analyse", "-a", default=False, help=help_msg, action='store_true')

    help_msg = "verbosity logging level (INFO=%d DEBUG=%d)" % (logging.INFO, logging.DEBUG)
    parser.add_argument("--verbosity", "-v", help=help_msg, default=DEFAULT_VERBOSITY_LEVEL, type=int)

    args = parser.parse_args()

    if args.verbosity == logging.DEBUG:

        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                            datefmt=TIME_FORMAT, level=args.verbosity)

    else:

        logging.basicConfig(format='%(message)s', datefmt=TIME_FORMAT, level=args.verbosity)

    print_config(args)

    if not args.skip_train:

        training_neural_network(args)

    if not args.skip_correct:

        predict_neural_network(args)

    if not args.skip_analyse:

        analyse(args)


if __name__ == '__main__':

    sys.exit(main())

