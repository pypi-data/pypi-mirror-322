import numpy as np
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler

class MultipleLinear(BaseEstimator):
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations

    def fit(self, X, y):
        # Normalize input data
        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(X)
        self.y = y.reshape(-1, 1)  # Ensure y is a column vector

        # Check for NaN or infinite values
        self.X = np.nan_to_num(self.X, nan=np.nanmean(self.X), posinf=np.nanmean(self.X), neginf=np.nanmean(self.X))
        self.y = np.nan_to_num(self.y, nan=np.nanmean(self.y), posinf=np.nanmean(self.y), neginf=np.nanmean(self.y))

        m = self.y.shape[0]
        self.theta = np.random.randn(self.X.shape[1], 1) * self.learning_rate  # Initialize theta with small random values

        # Gradient descent
        for i in range(self.iterations):
            y_pred = np.dot(self.X, self.theta)  # Predictions
            d_theta = (2 / m) * np.dot(self.X.T, (y_pred - self.y))  # Gradient
            self.theta -= self.learning_rate * d_theta  # Update theta

        return self

    def predict(self, X):
        X = self.scaler.transform(X)  # Normalize input data
        predictions = np.dot(X, self.theta)
        return predictions  # Return predictions as a 2D array

    def score(self, X, y):
        y_pred = self.predict(X)
        mse = np.mean(np.square(y_pred - y.reshape(-1, 1)))  # Mean Squared Error
        return mse

    def get_params(self, deep=True):
        return {"learning_rate": self.learning_rate, "iterations": self.iterations}

    def set_params(self, **params):
        for param, value in params.items():
            setattr(self, param, value)
        return self
    
    def score(self, X, y):
        """
        Compute the R² score for the linear regression model.
        :param X: Features of the dataset.
        :param y: True target values.
        :return: R² score.
        """
        y_pred = self.predict(X)
        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_residual = np.sum((y - y_pred) ** 2)
        r2_score = 1 - (ss_residual / ss_total)
        return r2_score