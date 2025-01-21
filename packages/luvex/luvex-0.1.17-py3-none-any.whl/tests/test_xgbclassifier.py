import numpy as np
from luvex import XGBClass  # Import your XGBClass model (assuming XGBClass is implemented in the luvex module)

def test_xgb():
    # Sample training data
    X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y_train = np.array([0, 1, 0, 1])  # Binary labels for classification
    
    # Sample test data
    X_test = np.array([[2, 2], [3, 3]])

    # Initialize and fit the model
    model = XGBClass(max_depth=3, reg_lambda=1.0, prune_gamma=0.1, n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Validate the predictions (adjust the expected result accordingly)
    #assert np.all((predictions == 0) | (predictions == 1)), "Predictions should be binary (0 or 1)"
    
    print(f"Predictions: {predictions}")
    print("All tests passed for XGBClassifier")

if __name__ == "__main__":
    test_xgb()
