import numpy as np

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

class Brain:
    def __init__(self, weights=None):
        if weights == None:
            self.layer1 = np.random.rand(7, 6)
            self.layer2 = np.random.rand(6, 4)
        else:
            self.layer1 = np.copy(weights[0])
            self.layer2 = np.copy(weights[1])
    def predict(self, inputs):
        H1 = relu(np.dot(inputs, self.layer1))
        output = relu(np.dot(H1, self.layer2))
        probs = softmax(output)
        return probs
    def mutate(self, rate=0.1, scale=0.2):
        """
        rate: szansa na zmianę konkretnej wagi (0.1 = 10% wag się zmieni)
        scale: jak duża może być zmiana (od -scale do +scale)
        """
        print("MUTUJE")
        mask1 = np.random.rand(*self.layer1.shape) < rate
        self.layer1 += mask1 * np.random.uniform(-scale, scale, self.layer1.shape)
        
        # Mutujemy drugą warstwę
        mask2 = np.random.rand(*self.layer2.shape) < rate
        self.layer2 += mask2 * np.random.uniform(-scale, scale, self.layer2.shape )
    def get_weights(self):
        return self.layer1, self.layer2
    
    
        