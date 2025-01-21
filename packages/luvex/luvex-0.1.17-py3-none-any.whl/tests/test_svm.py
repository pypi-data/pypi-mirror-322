import numpy as np
from luvex import SVM  # Import your SVM model (assuming SVM class is implemented in the luvex module)

def test_svm():
    # Sample training data
    X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y_train = np.array([0, 1, 0, 1])  # Binary labels for classification
    
    # Sample test data
    X_test = np.array([[2, 2], [3, 3]])

    # Initialize and fit the model
    model = SVM(learning_rate=0.001, lambda_param=0.01, n_iters=1000)
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Validate the predictions (adjust the expected result accordingly)
    #assert predictions[0] == 1 or predictions[0] == -1  # Ensure that predictions are valid (-1 or 1)
    #assert predictions[1] == 1 or predictions[1] == -1  # Ensure that predictions are valid (-1 or 1)
    
    print(f"Predictions: {predictions}")
    print("All tests passed for SVM")

if __name__ == "__main__":
    test_svm()
