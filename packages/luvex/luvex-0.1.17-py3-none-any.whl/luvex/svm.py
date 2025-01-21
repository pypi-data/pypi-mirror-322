from sklearn.base import BaseEstimator
import numpy as np
class SVM(BaseEstimator):
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)

        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]

        return self  # Required by scikit-learn to return the fitted model

    def predict(self, X):
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)  # Return predictions as -1 or 1

    def score(self, X, y):
        predictions = self.predict(X)
        return np.mean(predictions == y)  # Accuracy score

    def get_params(self, deep=True):
        """
        Returns the hyperparameters of the SVM model as a dictionary.

        Parameters:
        deep : bool, default=True
            If True, it will return the hyperparameters of subcomponents recursively.
        
        Returns:
        params : dict
            A dictionary with hyperparameters as key-value pairs.
        """
        return {
            "learning_rate": self.lr,
            "lambda_param": self.lambda_param,
            "n_iters": self.n_iters
        }
