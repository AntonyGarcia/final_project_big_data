import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.utils import all_estimators


# Define a function to load the dataset
def loadDataset(fileName):
    data = pd.read_csv(fileName)
    y = np.array(data['load'])
    x = np.array(data[['hour_of_day', 'day_of_week', 'month_of_year', 'year', 'is_holiday', 'temperature']])
    return x, y


# Load the dataset
dataset_x, dataset_y = loadDataset('raw_data/final_dataset.csv')

# Split the dataset into training and testing sets
train_x, test_x, train_y, test_y = train_test_split(dataset_x, dataset_y, test_size=0.1)

# Get a list of all regression models in scikit-learn, excluding GammaRegressor and GaussianProcessRegressor
exclude_regressors = ['GammaRegressor','StackingRegressor', 'GaussianProcessRegressor','KernelRidge','MultiOutputRegressor','MLPRegressor','MultiTaskElasticNet','MultiTaskElasticNetCV','MultiTaskLasso','MultiTaskLassoCV','NuSVR','QuantileRegressor','OrthogonalMatchingPursuitCV','RadiusNeighborsRegressor','SVR']
estimators = [est for est in all_estimators(type_filter='regressor') if est[0] not in exclude_regressors]

# Loop over all regression models and print their names
best_model = None
best_rmse = float('inf')
for name, RegressorClass in estimators:
    print('Trying model:', name)

    try:
        # Create an instance of the model
        model = RegressorClass()

        # Train the model
        model.fit(train_x, train_y)

        # Make predictions on the test data
        pred_y = model.predict(test_x)

        # Evaluate the model
        rmse = np.sqrt(mean_squared_error(test_y, pred_y))

        # Update the best model and its accuracy
        if rmse < best_rmse:
            best_model = model
            best_rmse = rmse

        print('Model: {}, RMSE: {}'.format(name, rmse))

    except Exception as e:
        # Some models may raise exceptions, so we catch them and print an error message
        print('Error with model {}: {}'.format(name, e))

# Print the best model and its accuracy
print('\nBest model: {}, RMSE: {}'.format(type(best_model).__name__, best_rmse))