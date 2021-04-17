import datetime
import matplotlib.pyplot
from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.models import model_from_json
import tensorflow as tf

tf.get_logger().setLevel('INFO')


class Neural:

    def __init__(self, size_window_left, size_window_right, number_samples, threshold, number_epochs,
                      learning_patterns_per_id, optimizer_function, loss_function, dense_layers,
                      output_evolution_error_figures):

        self.size_windows_left = size_window_left
        self.size_window_right = size_window_right
        self.number_samples = number_samples
        self.threshold = threshold
        self.number_epochs = number_epochs
        self.learning_patterns_per_id = learning_patterns_per_id
        self.optimizer_function = optimizer_function
        self.loss_function = loss_function
        self.output_evolution_error_figures = output_evolution_error_figures
        self.neural_network = None
        self.dense_layers = dense_layers

    def create_neural_network(self):

        input_size = Input(shape=(self.size_windows_left + self.size_window_right + 1,))
        # Please do not change this layer
        self.neural_network = Dense(20, )(input_size)
        self.neural_network = Dropout(0.2)(self.neural_network)

        for i in range(self.dense_layers - 1):

            self.neural_network = Dense(20)(self.neural_network)
            self.neural_network = Dropout(0.5)(self.neural_network)

        # Please do not change this layer
        self.neural_network = Dense(1, activation='sigmoid')(self.neural_network)
        self.neural_network = Model(input_size, self.neural_network)
        self.neural_network.summary()
        self.neural_network.compile(optimizer=self.optimizer_function, loss=self.loss_function,
                                    metrics=['mean_squared_error'])

    def fit(self, x, y, x_validation, y_validation):

        first_test_training = self.neural_network.evaluate(x, y)
        first_test_validation = self.neural_network.evaluate(x_validation, y_validation)
        history = self.neural_network.fit(x, y, epochs=self.number_epochs,
                                          validation_data=(x_validation, y_validation), )
        self.plotter_error_evaluate(history.history['mean_squared_error'], history.history['val_mean_squared_error'],
                                    first_test_training, first_test_validation)

    def plotter_error_evaluate(self, mean_square_error_training, mean_square_error_evaluate, first_error_training,
                               first_error_evaluate):

        mean_square_error_training.insert(0, first_error_training[1])
        mean_square_error_evaluate.insert(0, first_error_evaluate[1])
        matplotlib.pyplot.plot(mean_square_error_training, 'b', marker='^', label="Treinamento")
        matplotlib.pyplot.plot(mean_square_error_evaluate, 'g', marker='o', label="Validação")
        matplotlib.pyplot.legend(loc="upper right")
        matplotlib.pyplot.xlabel('Quantidade de épocas')
        matplotlib.pyplot.ylabel('Erro Médio')
        matplotlib.pyplot.savefig(
            self.output_evolution_error_figures + "fig_Mean_square_error_" + str(datetime.datetime.now()) + ".pdf")

    def predict_values(self, x):

        return self.neural_network.predict(x)

    def save_models(self, model_architecture_file, model_weights_file):

        model_json = self.neural_network.to_json()

        with open(model_architecture_file, "w") as json_file:

            json_file.write(model_json)

        self.neural_network.save_weights(model_weights_file)
        print("Saved model {} {}".format(model_architecture_file, model_weights_file))

    def load_models(self, model_architecture_file, model_weights_file):

        json_file = open(model_architecture_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.neural_network = model_from_json(loaded_model_json)
        self.neural_network.load_weights(model_weights_file)
        print("Loaded model {} {}".format(model_architecture_file, model_weights_file))

    @staticmethod
    def get_samples_vectorized(sample):

        sample_vectorized = []

        for i in range(len(sample)):

            sample_vectorized.append(float(sample[i][2]))

        return sample_vectorized, sample[5][2]

    def predict(self, x):

        x_axis = []
        y_axis = []
        results_predicted = []

        for i in range(len(x)):

            x_temp, y_temp = self.get_samples_vectorized(x[i])
            x_axis.append(x_temp)
            y_axis.append(y_temp)

        predicted = self.neural_network.predict(x_axis)

        for i in range(len(predicted)):

            if predicted[i] > self.threshold or y_axis[i] > 0.8:

                results_predicted.append(x[i][5])

        return results_predicted
