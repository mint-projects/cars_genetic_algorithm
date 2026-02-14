# Autonomous Pathfinding via Neuroevolution: A Genetic Algorithm Approach
This project is about teaching 2D cars to drive to their final desination.

## Table of Contents
- [Technical overview](#technical-overview)
- [Installation and usage](#installationinusage)
- [Visual demonstration](#visualdemonstration)

## Technical overview

### 1. The brain of a car
Instead of using traditional gradient-based reinforcement learning, this project implements Neuroevolution.
- **Neural Network**: Each agent (car) is powered by a custom Feedforward Neural Network (Multi-Layer Perceptron).

| Layer | Type | Neurons | Activation |
| :--- | :--- | :--- | :--- |
| input | Data from sensors | 7 | Linear |
| hidden | Dense | 6 | ReLU |
| Input Neurons | Actions | 4 | Softmax |

- **Evolutionary Strategy**: I implemented a Genetic Algorithm (GA) to optimize the network's weights. The population of cars evolves over generations, where only the fittest individuals pass their weights to the next batch.

### 2. Perceptrion. Raycasting sensors
Each agent has its own set of sensors - straight lines coming out of the middle of each car.
- **Input**: Each ray tracks the distance from the neares obstacle (wall) in real-time
- **Processing**: Each distance is normalized and fed to into the brain of the car (neural network)
- **Output**: Neural network predicts the cars move in the next frame. It can accelerate, brake or turn left or right

### 3. Fitness evaluation and genetic operators
This project evolves the population using the strategies below
- **Fitness function**: Fitness of a car is calculated by a custom formula:

$$Fitness = \left( \frac{100}{1 + \mathrm{Distance}_{\mathrm{to\_target}}} \right) + \mathrm{Score}_{\mathrm{checkpoints}}$$

- **Elitism**: Car with best fitness in the previous generation is automatically passed to the next generation
- **Selection and mutation**: New agents are created by mixing the weights of top performers (Crossover) and applying random Gaussian noise (Mutation) to explore new driving strategies.

### 4. Key technical features
- **Custom Physics Engine**: Developed using Pygame, handling collision detection and momentum
- **Dynamic Camera System**: A smooth camera that automatically tracks the leader of the current generation
- **Performance Optimization**: Use of NumPy for fast matrix multiplication within the neural networks

