import numpy as np
from sklearn.preprocessing import StandardScaler

class LinearRegression:

    def __init__(self, lr=0.0001, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.scaler = StandardScaler()

    def fit(self, X, y):
        # Scale the input features
        X_scaled = self.scaler.fit_transform(X)
        
        n_samples, n_features = X_scaled.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            y_pred = np.dot(X_scaled, self.weights) + self.bias

            dw = (1 / n_samples) * np.dot(X_scaled.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            self.weights = self.weights - self.lr * dw
            self.bias = self.bias - self.lr * db

    def predict(self, X):
        # Scale the test data using the same scaler
        X_scaled = self.scaler.transform(X)
        y_pred = np.dot(X_scaled, self.weights) + self.bias

        # Ensure y_pred matches the shape of y_test (2D if needed)
        if y_pred.ndim == 1:
            y_pred = y_pred.reshape(-1, 1)  # Reshape to (n_samples, 1)

        return y_pred
