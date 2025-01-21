import numpy as np
from sklearn.preprocessing import StandardScaler

class LinearRegression:

    def __init__(self, lr=0.01, n_iters=10000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()

    def fit(self, X, y):
        # Scale the input features and target
        X_scaled = self.scaler_X.fit_transform(X)
        y_scaled = self.scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

        n_samples, n_features = X_scaled.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            y_pred = np.dot(X_scaled, self.weights) + self.bias

            dw = (1 / n_samples) * np.dot(X_scaled.T, (y_pred - y_scaled))
            db = (1 / n_samples) * np.sum(y_pred - y_scaled)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            # Uncomment to debug
            # loss = (1 / n_samples) * np.sum((y_pred - y_scaled)**2)
            # print(f"Iteration {_}: Loss = {loss}")

    def predict(self, X):
        # Scale the test data using the same scaler
        X_scaled = self.scaler_X.transform(X)
        y_pred_scaled = np.dot(X_scaled, self.weights) + self.bias
        # Rescale predictions back to original scale
        y_pred = self.scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
        return y_pred
