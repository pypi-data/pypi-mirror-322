import numpy as np
from sklearn.preprocessing import StandardScaler

class Multivariate_Regression:
    def __init__(self, learning_rate=0.001, convergence_tol=1e-5, clip_threshold=1.0, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.convergence_tol = convergence_tol
        self.clip_threshold = clip_threshold
        self.beta1 = beta1  # Adam hyperparameter for first moment estimate
        self.beta2 = beta2  # Adam hyperparameter for second moment estimate
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.W = None
        self.b = None
        self.scaler = StandardScaler()

        # Adam moment estimates
        self.m_W = None
        self.v_W = None
        self.m_b = None
        self.v_b = None

    def initialize_parameters(self, n_features):
        # Initialize weights and bias to small values (Xavier initialization)
        self.W = np.random.randn(n_features) * np.sqrt(2. / n_features)
        self.b = 0

        # Initialize Adam moment estimates
        self.m_W = np.zeros_like(self.W)
        self.v_W = np.zeros_like(self.W)
        self.m_b = 0
        self.v_b = 0

    def forward(self, X):
        return np.dot(X, self.W) + self.b

    def compute_cost(self, predictions, y):
        m = len(y)
        cost = np.sum(np.square(predictions - y)) / (2 * m)
        return cost

    def backward(self, predictions, X, y):
        m = len(y)
        dW = np.dot(X.T, (predictions - y)) / m
        db = np.sum(predictions - y) / m

        # Clip gradients
        dW = np.clip(dW, -self.clip_threshold, self.clip_threshold)
        db = np.clip(db, -self.clip_threshold, self.clip_threshold)

        return dW, db

    def fit(self, X, y, iterations=1000, early_stopping_rounds=50):
        X = self.scaler.fit_transform(X)

        n_features = X.shape[1]
        self.initialize_parameters(n_features)

        prev_cost = float('inf')
        no_improvement_count = 0

        for i in range(iterations):
            predictions = self.forward(X)
            cost = self.compute_cost(predictions, y)

            dW, db = self.backward(predictions, X, y)

            # Adam optimization update for weights and bias
            self.m_W = self.beta1 * self.m_W + (1 - self.beta1) * dW
            self.v_W = self.beta2 * self.v_W + (1 - self.beta2) * (dW ** 2)

            self.m_b = self.beta1 * self.m_b + (1 - self.beta1) * db
            self.v_b = self.beta2 * self.v_b + (1 - self.beta2) * (db ** 2)

            m_W_hat = self.m_W / (1 - self.beta1 ** (i + 1))
            v_W_hat = self.v_W / (1 - self.beta2 ** (i + 1))

            m_b_hat = self.m_b / (1 - self.beta1 ** (i + 1))
            v_b_hat = self.v_b / (1 - self.beta2 ** (i + 1))

            # Update parameters using Adam
            self.W -= self.learning_rate * m_W_hat / (np.sqrt(v_W_hat) + self.epsilon)
            self.b -= self.learning_rate * m_b_hat / (np.sqrt(v_b_hat) + self.epsilon)

            # Early stopping based on cost improvement
            if abs(prev_cost - cost) < self.convergence_tol:
                no_improvement_count += 1
                if no_improvement_count >= early_stopping_rounds:
                    break
            else:
                prev_cost = cost
                no_improvement_count = 0

        r2 = self.calculate_r2(y, predictions)
        return r2

    def predict(self, X):
        X = self.scaler.transform(X)
        return self.forward(X)

    def calculate_r2(self, y_true, y_pred):
        ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        r2 = 1 - (ss_residual / ss_total)
        return r2
