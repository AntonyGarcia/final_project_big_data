import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

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

# Define the best hyperparameters
best_params = {
    'n_estimators': 200,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'max_features': 'sqrt',
    'max_depth': 30
}

# Create an instance of the best model
model = RandomForestRegressor(**best_params)

# Train the model on the training dataset
model.fit(train_x, train_y)

# Make predictions on the test data
pred_y = model.predict(test_x)

# Evaluate the model on the test data
rmse = np.sqrt(np.mean((pred_y - test_y) ** 2))
print('RMSE:', rmse)

# Save the trained model
joblib.dump(model, 'trained_regressor/trained_regressor.joblib')
