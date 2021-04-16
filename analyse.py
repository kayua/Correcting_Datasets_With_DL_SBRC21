from tqdm import tqdm
import datetime
DEFAULT_PATH_ANALYSES = 'analyses/'
DEFAULT_PATH_LOG = 'logs/'


class Analyse:

    def __init__(self, original_file_swarm, corrected_file_swarm, failed_file_swarm, analyse_file, analyse_file_mode,
                 dense_layers, threshold, pif, dataset, seed):

        self.original_file_swarm = []

        self.original_file_swarm = []
        self.corrected_file_swarm = []
        self.failed_file_swarm = []

        self.trace_found_in_original_and_corrected = 0
        self.trace_found_in_original_and_failed = 0
        self.trace_found_in_original_and_failed_and_corrected = 0

        self.original_file_swarm_location = original_file_swarm
        self.corrected_file_swarm_location = corrected_file_swarm
        self.failed_file_swarm_location = failed_file_swarm

        self.size_list_corrected = 0
        self.size_list_original = 0
        self.size_list_failed = 0
        self.number_fills = 0

        self.analyse_file = analyse_file
        self.analyse_file_mode = analyse_file_mode

        self.dense_layers = dense_layers
        self.threshold = threshold
        self.pif = pif
        self.dataset = dataset
        self.seed = seed

    def load_original_swarm(self):

        file_swarm_original = open(self.original_file_swarm_location, 'r')

        for i, j in enumerate(file_swarm_original):

            if i != 0:

                keys = j.split(' ')
                self.original_file_swarm.append([int(keys[0]), int(keys[3])])

        self.size_list_original = len(self.original_file_swarm)

    def load_corrected_swarm(self):

        file_swarm_original = open(self.corrected_file_swarm_location, 'r')
        self.load_number_predictions()

        for i, j in enumerate(file_swarm_original):

            if i != 0:

                keys = j.split(' ')
                self.corrected_file_swarm.append([int(keys[0]), int(keys[1])])

        self.size_list_corrected = len(self.corrected_file_swarm)
        self.corrected_file_swarm = sorted(self.corrected_file_swarm, key=lambda x: x[0])

    def load_failed_swarm(self):

        file_swarm_original = open(self.failed_file_swarm_location, 'r')

        for i, j in enumerate(file_swarm_original):

            if i != 0:

                keys = j.split(' ')

                self.failed_file_swarm.append([int(keys[0]), int(keys[3])])

        self.size_list_failed = len(self.failed_file_swarm)

    def search_corrected(self, key_1, key_2):

        for i, j in enumerate(self.corrected_file_swarm):

            if j[0] == key_1:

                if j[1] == key_2:

                    del self.corrected_file_swarm[i]
                    return True

        return False

    def search_failed(self, key_1, key_2):

        for i, j in enumerate(self.failed_file_swarm):

            if j[0] == key_1:

                if j[1] == key_2:

                    del self.failed_file_swarm[i]
                    return True

        return False

    def run_analise(self):

        self.load_corrected_swarm()
        self.load_failed_swarm()
        self.load_original_swarm()

        for i in tqdm(range(len(self.original_file_swarm)), desc='Analyzing'):

            key_1, key_2 = self.original_file_swarm[i]

            swarm_failed = self.search_failed(key_1, key_2)
            swarm_corrected = self.search_corrected(key_1, key_2)

            if swarm_failed:

                self.trace_found_in_original_and_failed += 1

            if swarm_corrected:

                self.trace_found_in_original_and_corrected += 1

            if swarm_corrected and swarm_failed:

                self.trace_found_in_original_and_failed_and_corrected += 1


    def load_number_predictions(self):
        number_fills = open(DEFAULT_PATH_LOG + 'number_fills.log', 'r')
        self.number_fills = int(number_fills.read())

    def write_results_analyse(self):

        analyse_results = open(self.analyse_file, self.analyse_file_mode)
        topology = "["
        for i in range(self.dense_layers):
            topology += "20, "
        topology += "1]"

        analyse_results.write('\nBEGIN ############################################\n\n')
        analyse_results.write(' RESULTS \n')
        analyse_results.write("  Now      : {}\n".format(datetime.datetime.now()))
        analyse_results.write("  Topology : {}\n".format(topology))
        analyse_results.write("  Threshold: {}\n".format(self.threshold))
        analyse_results.write("  PIF      : {}%\n".format(int(self.pif * 100)))
        analyse_results.write("  Dataset  : {}\n".format(self.dataset))
        analyse_results.write("  Seed     : {}\n\n".format(self.seed))

        analyse_results.write('  Size files:           \n')
        analyse_results.write('-----------------------------\n')
        analyse_results.write('  Total Traces original file         : {}\n'.format(self.size_list_original))
        analyse_results.write('  Total Traces failed file           : {}\n'.format(self.size_list_failed))
        analyse_results.write('  Total Traces corrected file        : {}\n'.format(self.size_list_corrected))

        falhas = self.size_list_original - self.size_list_failed
        analyse_results.write('  Fails (Original-failed)            : {}\n'.format(falhas))

        modificacoes = self.size_list_corrected - self.size_list_failed
        analyse_results.write('  Modifications (Original-corrected) : {}\n'.format(modificacoes))

        analyse_results.write('------------------------------\n')
        analyse_results.write('            Analyse:          \n')
        analyse_results.write('------------------------------\n')
        analyse_results.write('  Found in [Original, Corrected, Failed]: {}\n'.format(self.trace_found_in_original_and_failed_and_corrected))
        analyse_results.write('  Found in [Original, Corrected]        : {}\n'.format(self.trace_found_in_original_and_corrected))
        analyse_results.write('  Found in [Original, Failed]           : {}\n'.format(self.trace_found_in_original_and_failed))
        analyse_results.write('------------------------------\n')
        analyse_results.write('            Scores:           \n')
        analyse_results.write('------------------------------\n')
        tp = self.trace_found_in_original_and_corrected-self.trace_found_in_original_and_failed
        analyse_results.write('  True positive  (TP): {}\n'.format(tp))
        fp = self.size_list_corrected-self.trace_found_in_original_and_corrected
        analyse_results.write('  False positive (FP): {}\n'.format(fp))
        fn = self.size_list_original-self.trace_found_in_original_and_corrected
        analyse_results.write('  False negative (FN): {}\n'.format(fn))

        tn = self.size_list_original -tp -(fp+fn)
        analyse_results.write('  True negative  (TN): {}\n'.format(tn))

        # falhas = tp + fn
        # modificacoes = tp + fp

        # [20, 20, 1]			.75	10%	S1d	0.75	1	10488	671	7531	112886

        linha = "#SUMMARY#"
        linha += ";{}".format(topology)
        linha += ";{}".format(self.size_list_original)
        linha += ";{}".format(falhas)
        linha += ";{}".format(self.threshold)
        linha += ";{}%".format(int(self.pif*100))
        linha += ";{}".format(self.dataset)
        linha += ";{}".format(self.threshold)
        linha += ";{}".format(self.seed)
        linha += ";{}".format(tp)
        linha += ";{}".format(fp)
        linha += ";{}".format(fn)
        linha += ";{}".format(tn)
        linha += "\n"
        print(linha)

        linha = "#SUMNEW#"
        linha += ";{}".format(topology)
        linha += ";{}".format(self.threshold)

        linha += ";{}%".format(int(self.pif * 100))
        linha += ";{}".format(self.dataset)
        linha += ";{}".format(self.seed)

        linha += ";{}".format(self.size_list_original)
        linha += ";{}".format(falhas)
        linha += ";{}".format(modificacoes)

        linha += ";{}".format(tp)
        linha += ";{}".format(fp)
        linha += ";{}".format(fn)
        linha += ";{}".format(tn)
        linha += "\n"
        print(linha)
        analyse_results.write(linha)

        analyse_results.write('\nEND ############################################\n\n')
        analyse_results.write('\n\n\n')
        analyse_results.close()


    def load_original_swarm(self):

        file_swarm_original = open(self.original_file_swarm_location, 'r')

        for i, j in enumerate(file_swarm_original):

            if i != 0:

                keys = j.split(' ')
                self.original_file_swarm.append([int(keys[0]), int(keys[3])])

        self.size_list_original = len(self.original_file_swarm)

    def load_corrected_swarm(self):

        file_swarm_original = open(self.corrected_file_swarm_location, 'r')
        self.load_number_predictions()

        for i, j in enumerate(file_swarm_original):

            if i != 0:

                keys = j.split(' ')
                self.corrected_file_swarm.append([int(keys[0]), int(keys[1])])

        self.size_list_corrected = len(self.corrected_file_swarm)
        self.corrected_file_swarm = sorted(self.corrected_file_swarm, key=lambda x: x[0])

    def load_failed_swarm(self):

        file_swarm_original = open(self.failed_file_swarm_location, 'r')

        for i, j in enumerate(file_swarm_original):

            if i != 0:

                keys = j.split(' ')

                self.failed_file_swarm.append([int(keys[0]), int(keys[3])])

        self.size_list_failed = len(self.failed_file_swarm)

    def search_corrected(self, key_1, key_2):

        for i, j in enumerate(self.corrected_file_swarm):

            if j[0] == key_1:

                if j[1] == key_2:

                    del self.corrected_file_swarm[i]
                    return True

        return False

    def search_failed(self, key_1, key_2):

        for i, j in enumerate(self.failed_file_swarm):

            if j[0] == key_1:

                if j[1] == key_2:

                    del self.failed_file_swarm[i]
                    return True

        return False

    def run_analise(self):

        self.load_corrected_swarm()
        self.load_failed_swarm()
        self.load_original_swarm()

        for i in tqdm(range(len(self.original_file_swarm)), desc='Analyzing'):

            key_1, key_2 = self.original_file_swarm[i]

            swarm_failed = self.search_failed(key_1, key_2)
            swarm_corrected = self.search_corrected(key_1, key_2)

            if swarm_failed:

                self.trace_found_in_original_and_failed += 1

            if swarm_corrected:

                self.trace_found_in_original_and_corrected += 1

            if swarm_corrected and swarm_failed:

                self.trace_found_in_original_and_failed_and_corrected += 1


    def load_number_predictions(self):

        #number_fills = open(DEFAULT_PATH_LOG + 'number_fills.log', 'r')
        #self.number_fills = int(number_fills.read())
        print('')

    # def write_results_analyse(self):
    #
    #     analyse_results = open(self.analyse_file, self.analyse_file_mode)
    #
    #     analyse_results.write('          RESULTS \n')
    #     analyse_results.write('            Size files:           ')
    #     analyse_results.write('-----------------------------')
    #     analyse_results.write(str(' Total Traces original file: ' + str(self.size_list_original)))
    #     analyse_results.write(str(' Total Traces failed file: ' + str(self.size_list_failed)))
    #     # falhas = self.size_list_original - self.size_list_failed
    #     analyse_results.write(str(' Total Traces corrected file: ' + str(self.size_list_corrected)))
    #     # modificacoes = self.size_list_original - self.size_list_corrected
    #
    #     analyse_results.write('------------------------------\n')
    #     analyse_results.write('            Analyse:            ')
    #     analyse_results.write('------------------------------\n')
    #     analyse_results.write('Found in [Original, Corrected, Failed]: ' + str(self.trace_found_in_original_and_failed_and_corrected))
    #     analyse_results.write('Found in [Original, Corrected]: ' + str(self.trace_found_in_original_and_corrected))
    #     analyse_results.write('Found in [Original, Failed]: ' + str(self.trace_found_in_original_and_failed))
    #     analyse_results.write('------------------------------\n\n')
    #     analyse_results.write('            Scores:            ')
    #     analyse_results.write('------------------------------\n\n')
    #     tp = self.trace_found_in_original_and_corrected-self.trace_found_in_original_and_failed
    #     analyse_results.write('True positive(TP): ' + str(tp))
    #     fp = self.size_list_corrected-self.trace_found_in_original_and_corrected
    #     analyse_results.write('False positive(FP): ' + str(fp))
    #     fn = self.size_list_original-self.trace_found_in_original_and_corrected
    #     analyse_results.write('False negative(FN): ' + str(fn))
    #
    #     tn = self.size_list_original -tp -(fp+fn)
    #     analyse_results.write('True negative(TN): ' + str(tn))
    #     analyse_results.write('\n############################################\n\n')
    #     # falhas = tp + fn
    #     # modificacoes = tp + fp
    #
    #     analyse_results.write('\n\n\n')


