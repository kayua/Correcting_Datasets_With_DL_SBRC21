from tqdm import tqdm


class Dataset:

    def __init__(self, size_window_left, size_window_right, number_samples, file_results):

        self.header = []
        self.list_swarm_loaded = []
        self.list_swarm_per_peer = []
        self.output_file = None
        self.size_window_left = size_window_left
        self.size_window_right = size_window_right
        self.number_samples = number_samples
        self.file_results = file_results
        self.number_fills = 0

    def load_samples(self, swarm_file):

        file_swarm_loaded = open(swarm_file, 'r')
        file_swarm_lines = file_swarm_loaded.readlines()

        for line in tqdm(range(len(file_swarm_lines)), desc='Loading swarm'):

            if line == 0:

                self.header = file_swarm_lines[line]

            else:

                line_swarm = file_swarm_lines[line].split(' ')
                line_swarm = [int(line_swarm[0]), int(line_swarm[3]), 1]

                self.list_swarm_loaded.append(line_swarm)

    def create_list_peer(self, swarm):

        try:

            _ = self.list_swarm_per_peer[int(swarm[1])]
            self.list_swarm_per_peer[int(swarm[1])].append(swarm)

        except IndexError:

            while True:

                self.list_swarm_per_peer.append([])

                try:

                    _ = self.list_swarm_per_peer[int(swarm[1])]
                    self.list_swarm_per_peer[int(swarm[1])].append(swarm)
                    break

                except IndexError:

                    pass

    def create_list_per_peer(self):

        for i in tqdm(range(len(self.list_swarm_loaded)), desc='Creating list peers'):

            self.create_list_peer(self.list_swarm_loaded[i])

    def clear_samples(self):

        for i in range(len(self.list_swarm_per_peer)):

            try:

                if len(self.list_swarm_per_peer[i]) == 0:

                    del self.list_swarm_per_peer[i]

            except IndexError:

                pass

    def fill_gaps_per_peer(self, id_peer):

        try:

            iterator = int(self.list_swarm_per_peer[id_peer][0][0])

        except IndexError:

            return 0

        temporary_swarm = []
        iterator_list_swarm = 0

        while iterator < int(self.list_swarm_per_peer[id_peer][-1][0]):

            if int(self.list_swarm_per_peer[id_peer][iterator_list_swarm][0]) != iterator:

                temporary_swarm.append([int(iterator), int(id_peer), 0])
                self.number_fills += 1

            else:

                temporary_swarm.append(self.list_swarm_per_peer[id_peer][iterator_list_swarm])
                iterator_list_swarm += 1

            iterator += 1

        temporary_swarm.append(self.list_swarm_per_peer[id_peer][-1])
        self.list_swarm_per_peer[id_peer] = temporary_swarm

        return 0

    def fill_gaps(self):

        for i in tqdm(range(len(self.list_swarm_per_peer)), desc='filling gaps'):

            self.fill_gaps_per_peer(i)

        return self.number_fills

    def fill_borders(self):

        for i in range(len(self.list_swarm_per_peer)):

            self.filling_borders(i)

    def filling_borders(self, id_peer):

        list_swarm_borders = []

        for i in range(self.size_window_left):

            list_swarm_borders.append([-1, id_peer + 1, 0])

        self.list_swarm_per_peer[id_peer] = list_swarm_borders + self.list_swarm_per_peer[id_peer]
        list_swarm_borders = []

        for i in range(self.size_window_right + 1):

            list_swarm_borders.append([-1, id_peer + 1, 0])

        self.list_swarm_per_peer[id_peer] = self.list_swarm_per_peer[id_peer] + list_swarm_borders

    def create_windows_per_peer(self, peer_id):

        windows_list_x = []
        windows_list_y = []

        for i in range((len(self.list_swarm_per_peer[peer_id]) - (self.size_window_right + self.size_window_left))):

            windows_list_x.append(
                self.list_swarm_per_peer[peer_id][i:(i + (self.size_window_right + self.size_window_left) + 1)])
            windows_list_y.append(self.list_swarm_per_peer[peer_id][i + self.size_window_right + 1][2])

        return windows_list_x, windows_list_y

    @staticmethod
    def get_samples_vectorized(sample):

        sample_vectorized = []

        for i in range(len(sample)):

            sample_vectorized.append(float(sample[i][2]))

        return sample_vectorized, sample[5][2]

    def create_sample_to_training(self):

        list_windows_to_predict_x = []
        list_windows_to_predict_y = []

        for i in range(self.number_samples):

            list_windows_x, list_windows_y = self.create_windows_per_peer(i)

            for j in range(len(list_windows_x)):

                x, y = self.get_samples_vectorized(list_windows_x[j])
                list_windows_to_predict_x.append(x)
                list_windows_to_predict_y.append(float(y))

        return list_windows_to_predict_x, list_windows_to_predict_y

    def get_training_samples(self):

        x, y = self.create_sample_to_training()

        for i in tqdm(range(len(x)), desc='Creating Samples'):

            if (x[i][4] < 0.5 and x[i][6] < 0.5) or ((x[i][4] > 0.5 > x[i][6]) and (0.5 > x[i][7]) and (0.5 > x[i][8])) or ((x[i][3] < 0.5) and (x[i][4] < 0.5) and (x[i][4] < 0.5 < x[i][6])):
                y[i] = float(0)

            x[i][5] = float(0)

        return x, y

    def create_file_results(self):

        self.output_file = open(self.file_results, 'w')
        self.output_file.write(str(self.header))

    def write_swarm(self, values):

        for i in values:

            output_result_format = str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
            self.output_file.write(str(output_result_format))

    def get_number_peers(self):

        return len(self.list_swarm_per_peer)
