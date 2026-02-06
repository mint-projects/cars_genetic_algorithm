import numpy as np

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    # Odejmujemy max dla stabilności numerycznej
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

class Brain:
    def __init__(self):
        self.layer1 = np.random.rand(8, 6)
        self.layer2 = np.random.rand(6, 4)
    def predict(self, inputs):
        H1 = relu(np.dot(inputs, self.layer1))
        output = relu(np.dot(H1, self.layer2))
        probs = softmax(output)
        return probs
    
        