import pandas as pd
import joblib

# Load CSV file into a pandas DataFrame
df = pd.read_csv('raw_data/future_dataset.csv')

# Load the trained regressor using joblib
regressor = joblib.load('trained_regressor/trained_regressor.joblib')

# Make predictions on the data
predictions = regressor.predict(df[['hour_of_day', 'day_of_week', 'month_of_year', 'year', 'is_holiday', 'temperature']])

# Add the predicted values as an extra column to the DataFrame
df['predicted_load'] = predictions

# Write the updated DataFrame to a new CSV file
df.to_csv('file_with_predictions.csv', index=False)
