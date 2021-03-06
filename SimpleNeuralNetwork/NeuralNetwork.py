from SimpleNeuralNetwork.NeuralNetworkLayer import NeuralNetworkLayer


class NeuralNetwork:
    """
    Used to generate a neural network.
    """

    def __init__(self, neuron_counts, learning_factor=0.01, bias=1):
        """
        Creates the neural network.
        :param neuron_counts: a list of the neuron count of each layer;
        len(neuron_counts) equals the count of layers
        :param learning_factor: the factor, how much a single result should change the network
        (a huge learning_factor results in a faster change; earlier results will be overridden more for that)
        :param bias: the added base for each network layer (should be 1)
        """
        self.learning_factor = learning_factor
        self.default_bias = bias
        # create layers:
        last_layer = None
        self.layers = []
        for neuron_count in neuron_counts:
            last_layer = NeuralNetworkLayer(neuron_count, last_layer, self.default_bias)
            self.layers.append(last_layer)
        self.layers[-1].to_output_layer()
        self.network_error = 0

    def __iter__(self):
        """
        Iterates over the layers as default.
        :return: an iterator including the layers
        """
        return iter(self.layers)

    @classmethod
    def loss(cls, a, b):
        """
        Evaluates the difference of a and b and doubles it.
        :param a: the first number (minuend)
        :param b: the second number (subtrahend)
        :return: the double of the difference
        """
        return (a - b) * 2

    def think(self, input_values):
        """
        Starts the neural network with the passed input values.
        :param input_values: the input values for the first layer
        :return: a list of the output of the neural network
        """
        self.layers[0].set_input(input_values)
        for layer in self:
            layer.think()
        return list(map(lambda neuron: neuron.get_output(), self.layers[-1]))

    def train(self, input_values, output_values, iterations=10_000):
        """
        Trains the network with specified input and output values.
        :param input_values: a list of the input values for the network
        :param output_values: a list of the output values for the network
        :param iterations: count of the repetitions of the
        :return: the last error
        """
        for _ in range(iterations):
            for (nn_inputs, nn_outputs) in zip(input_values, output_values):
                network_output = self.think(nn_inputs)
                network_error = list(map(lambda network_value, desired_value:
                                         NeuralNetwork.loss(network_value, desired_value) * self.learning_factor,
                                         network_output, nn_outputs))
                self.layers[-1].adjust(network_error)
        return [self.think(nn_inputs) for nn_inputs in input_values]

    def get_error(self):
        """
        Returns the error of the network.
        :return: the error
        """
        return self.network_error

    def print_results(self, input_values, output_values, label=None, decimal_places=10):
        """
        Prints (formatted) the passed input, output and predictions of the neural network.
        :param input_values: the input values for the neural network to test
        :param output_values: the (correct) output values
        :param label: an information text, printed before the data is printed
        :param decimal_places: count of decimal places to round the prediction
        """
        if label is not None:
            print(label)
        for (inputs, outputs) in zip(input_values, output_values):
            print("Input:", inputs, "   Output:", outputs, "   Prediction:",
                  [round(x, decimal_places) for x in self.think(inputs)])
