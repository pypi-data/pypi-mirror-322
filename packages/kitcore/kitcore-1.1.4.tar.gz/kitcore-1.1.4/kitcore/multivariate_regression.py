import numpy as np
from sklearn.preprocessing import StandardScaler

class Multivariate_Regression:
    def __init__(self, learning_rate=0.01, convergence_tol=1e-5, clip_threshold=1.0):
        self.learning_rate = learning_rate
        self.convergence_tol = convergence_tol
        self.clip_threshold = clip_threshold  # Gradient clipping threshold
        self.W = None  # Weights (one for each feature)
        self.b = None  # Bias term (scalar)
        self.scaler = StandardScaler()  # For feature scaling

    def initialize_parameters(self, n_features):
        # Initialize weights and bias to small values
        self.W = np.random.randn(n_features) * 0.01
        self.b = 0

    def forward(self, X):
        # Compute predictions using the linear model
        return np.dot(X, self.W) + self.b

    def compute_cost(self, predictions, y):
        # Compute Mean Squared Error (MSE) cost
        m = len(y)
        cost = np.sum(np.square(predictions - y)) / (2 * m)
        return cost

    def backward(self, predictions, X, y):
        # Compute gradients for weights and bias
        m = len(y)
        dW = np.dot(X.T, (predictions - y)) / m
        db = np.sum(predictions - y) / m

        # Clip gradients to avoid overflow
        dW = np.clip(dW, -self.clip_threshold, self.clip_threshold)
        db = np.clip(db, -self.clip_threshold, self.clip_threshold)
        return dW, db

    def fit(self, X, y, iterations=1000):
        # Train the model using Gradient Descent
        # Scale features
        X = self.scaler.fit_transform(X)

        # Initialize parameters
        n_features = X.shape[1]
        self.initialize_parameters(n_features)

        for i in range(iterations):
            # Forward pass
            predictions = self.forward(X)

            # Compute cost (optional for tracking but not used here)
            cost = self.compute_cost(predictions, y)

            # Backward pass (gradient computation)
            dW, db = self.backward(predictions, X, y)

            # Update parameters
            self.W -= self.learning_rate * dW
            self.b -= self.learning_rate * db

            # Print progress every 100 iterations
            if i % 100 == 0:
                print(f"Iteration {i}, Cost: {cost:.6f}")

        # Compute R² score after training
        r2 = self.calculate_r2(y, predictions)
        return r2

    def predict(self, X):
        # Predict outputs for the given input data
        X = self.scaler.transform(X)  # Scale features
        return self.forward(X)

    def calculate_r2(self, y_true, y_pred):
        # Compute R² score
        ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        r2 = 1 - (ss_residual / ss_total)
        return r2
