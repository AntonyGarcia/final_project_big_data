import csv
from datetime import datetime

# Define the start and end dates for the filter
start_date = datetime.strptime('2015-01-03', '%Y-%m-%d')
end_date = datetime.strptime('2020-06-27', '%Y-%m-%d')

# Open the input and output CSV files
with open('raw_data/weather_data.csv') as infile, open('filtered_weather.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Skip the header row in the input file
    header = next(reader)

    # Find the indices of the columns to keep
    keep_cols = [0, 6, 8, 9, 15, 16, 17]

    # Write the header row to the output file
    writer.writerow([header[i] for i in keep_cols])

    # Loop through each row in the input file and write it to the output file if it's within the date range
    for row in reader:
        # Convert the dt column to a datetime object
        dt = datetime.fromtimestamp(int(row[0]))

        # Check if the datetime is within the specified range
        if start_date <= dt < end_date:
            # Normalize the temperature, dew point, and feels like values to include a decimal point and trailing zero if necessary
            temp = row[6]
            if len(temp) == 3:
                temp = temp + '0'
            if len(temp) == 2:
                temp = temp + '00'
            temp = '{:.2f}'.format(float(temp) * 0.01)

            dew_point = row[8]
            if len(dew_point) == 3:
                dew_point = dew_point + '0'
            if len(dew_point) == 2:
                dew_point = dew_point + '00'
            dew_point = '{:.2f}'.format(float(dew_point) * 0.01)

            feels_like = row[9]
            if len(feels_like) == 3:
                feels_like = feels_like + '0'
            if len(feels_like) == 2:
                feels_like = feels_like + '00'
            feels_like = '{:.2f}'.format(float(feels_like) * 0.01)

            # Write the filtered row to the output file
            filtered_row = [row[i] for i in keep_cols]
            filtered_row[1] = temp  # Replace the temperature column with the normalized value
            filtered_row[2] = dew_point  # Replace the dew point column with the normalized value
            filtered_row[3] = feels_like  # Replace the feels like column with the normalized value
            writer.writerow(filtered_row)
