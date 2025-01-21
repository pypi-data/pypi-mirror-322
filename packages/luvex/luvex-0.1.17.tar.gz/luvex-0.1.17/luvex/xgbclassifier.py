from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.class_weight import compute_sample_weight
import numpy as np
from luvex.xgbclasstree import XGBClass_Tree

class XGBClass(BaseEstimator, ClassifierMixin):
    def __init__(self, max_depth=3, reg_lambda=1.0, prune_gamma=0.1, n_estimators=100, learning_rate=0.1):
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.prune_gamma = prune_gamma
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate

    def fit(self, X, y):
        X = np.array(X)  # Keep default dtype to avoid mismatch
        y = np.array(y)
        n_samples = X.shape[0]

        # Compute class weights
        sample_weight = compute_sample_weight(class_weight='balanced', y=y)

        self.models = []
        self.prev_yhat = np.full(n_samples, 0.5)  # Initialize with probability 0.5

        for _ in range(self.n_estimators):
            # Gradient and Hessian for binary cross-entropy
            residual = y - self.prev_yhat
            hessian = self.prev_yhat * (1 - self.prev_yhat)

            tree = XGBClass_Tree(self.max_depth, self.reg_lambda, self.prune_gamma)
            tree.fit(X, residual, hessian)
            self.models.append(tree)

            # Update predictions with weighted loss function
            self.prev_yhat += self.learning_rate * tree.predict(X) * sample_weight  # Adjust predictions based on class weights

    def predict(self, X):
        preds = np.zeros(X.shape[0])
        for tree in self.models:
            preds += self.learning_rate * tree.predict(X)
        # Convert probabilities to binary predictions
        return (preds >= 0.5).astype(int)

    def score(self, X, y):
        """
        This method calculates the accuracy of the classifier.
        """
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return accuracy

    def get_params(self, deep=True):
        """
        This method returns the hyperparameters of the model as a dictionary.
        """
        return {
            "max_depth": self.max_depth,
            "reg_lambda": self.reg_lambda,
            "prune_gamma": self.prune_gamma,
            "n_estimators": self.n_estimators,
            "learning_rate": self.learning_rate
        }
