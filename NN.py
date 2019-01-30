import numpy as np
import random


class NeuralNetwork:

	# INPUTS = integer defining the number of inputs
	# HIDDEN = list with the size of all of the hidden layers. Ex. [2,3,2]
	# OUTPUTS = integer defining the number of outputs
	def __init__(self,inputs,hidden,outputs):

		self.layers = []
		for i in range(0,len(hidden)):
			layer = []
			for j in range(0,hidden[i]):
				if i == 0:
					layer.append(Node(inputs,"relu"))
				else:
					layer.append(Node(hidden[i-1],"relu"))
			self.layers.append(layer)


		self.outputs = []
		for i in range(0,outputs):
			self.outputs.append(Node(hidden[-1],"sigmoid"))


	# INPUTS = Array with the inputs to predict
	def predict(self, inputs):
		# In case inputs its not a numpy array convert
		if type(inputs) == list:
			inputs = np.array(inputs)

		for i in range(0,len(self.layers)):
			A = []
			for j in range(0,len(self.layers[i])):
				a = self.layers[i][j].forward(inputs)			
				A.append(a)
			inputs = np.array(A)

		output = []
		for i in range(0,len(self.outputs)):
			a = self.outputs[i].forward(inputs)
			output.append(a)

		return output

	# Function to mutate the wheights and biases
	# M_PROB = Probability to mutate th current parameter
	# SD = Standar deviation for the mutation range
	def mutate(self, m_prob=0.3, sd=0.5):
		for i in range(0,len(self.layers)):
			for j in range(0,len(self.layers[i])):
				rand = random.uniform(0, 1)
				if rand < m_prob:
					self.layers[i][j].bias = self.layers[i][j].bias + random.gauss(0, .5)
				for t in range(0,len(self.layers[i][j].weights)):
					rand = random.uniform(0, 1)
					if rand < m_prob:
						self.layers[i][j].weights[t] = self.layers[i][j].weights[t] + random.gauss(0, .5)


class Node:

	def __init__(self,inputs, activation):
		self.bias = random.uniform(-1, 1)

		self.weights = np.zeros([inputs])
		for i in range(0,len(self.weights)):
			self.weights[i] = random.uniform(-1, 1)

		self.a = 0

		self.activation = activation

	def forward(self, inputs):
		z = np.dot(inputs, self.weights) + self.bias

		# RELU ACTIVATION
		if self.activation == "relu":
			self.a = max(0,z)
		if self.activation == "sigmoid":
			self.a = 1/(1+np.exp(-z))

		return self.a