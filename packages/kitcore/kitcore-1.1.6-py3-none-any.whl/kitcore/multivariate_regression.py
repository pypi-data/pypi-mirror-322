import numpy as np
from sklearn.preprocessing import StandardScaler

class Multivariate_Regression:

    def __init__(self, lr=0.01, n_iters=10000, regularization=False, lambda_reg=0.1):
        self.lr = lr
        self.n_iters = n_iters
        self.regularization = regularization  # Whether to apply regularization
        self.lambda_reg = lambda_reg  # Regularization strength
        self.weights = None
        self.bias = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()

    def fit(self, X, y):
        # Scale input features and target
        X_scaled = self.scaler_X.fit_transform(X)
        y_scaled = self.scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

        n_samples, n_features = X_scaled.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            # Predict values
            y_pred = np.dot(X_scaled, self.weights) + self.bias

            # Compute gradients
            dw = (1 / n_samples) * np.dot(X_scaled.T, (y_pred - y_scaled))
            db = (1 / n_samples) * np.sum(y_pred - y_scaled)

            # If regularization is enabled add the regularization term to the gradient of weights
            if self.regularization:
                dw += (self.lambda_reg / n_samples) * self.weights

            # Update weights and bias
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        # Scale the test data using the same scaler
        X_scaled = self.scaler_X.transform(X)
        y_pred_scaled = np.dot(X_scaled, self.weights) + self.bias
        # Rescale predictions back to original scale
        y_pred = self.scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
        return y_pred
