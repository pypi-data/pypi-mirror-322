import numpy as np
from collections import Counter

def euclidean_distance(x1, x2):
    #Calculate the Euclidean distance between two points.
    return np.sqrt(np.sum((x1 - x2) ** 2))

class KNN:
    def __init__(self, k=3):
        #Initialize the K-Nearest Neighbors classifier.
        self.k = k

    def fit(self, X, y):
        #Fit the KNN model.
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        #Predict the class labels for the given samples.
        return [self._predict(x) for x in X]

    def _predict(self, x):
        #Predict the class label for a single sample.
        distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

__all__ = ["KNN"]
