import csv
from datetime import datetime

starting_period = '2015-01-03'
ending_period = '2020-06-27'

# Define the start and end dates for the filter
start_date = datetime.strptime(starting_period, '%Y-%m-%d')
end_date = datetime.strptime(ending_period, '%Y-%m-%d')

# Open the input and output CSV files
with open('raw_data/raw_load_dataset.csv') as infile, open('filtered_power.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile, delimiter=',')
    writer = csv.writer(outfile, delimiter=';')

    # Write the header row to the output file
    header = next(reader)
    keep_cols = [0, 1, 14, 15, 16]
    header = [header[i] for i in keep_cols]
    header[0] = 'epoch_time'
    header[1] = 'nat_demand'
    writer.writerow(header)

    # Loop through each row in the input file and write it to the output file if it's within the date range
    for row in reader:
        # Convert the datetime column to epoch format
        dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        epoch_time = int(dt.timestamp())

        # Check if the datetime is within the specified range
        if start_date <= dt < end_date:
            # Format the nat_demand column to two decimal places
            nat_demand = '{:.2f}'.format(float(row[1]))

            # Replace the datetime and nat_demand columns with the epoch format and formatted value
            row[0] = epoch_time
            row[1] = nat_demand

            # Write the filtered row to the output file
            filtered_row = [row[i] for i in keep_cols]
            writer.writerow(filtered_row)



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

with open('filtered_power.csv') as power_file, open('filtered_weather.csv') as weather_file:
    power_reader = csv.reader(power_file, delimiter=';')
    weather_reader = csv.reader(weather_file, delimiter=';')

    # Skip the header row in the input files
    next(power_reader)
    next(weather_reader)

    # Create a dictionary to store the weather data, with the timestamp as the key
    weather_data = {}
    for row in weather_reader:
        dt = datetime.fromtimestamp(int(row[0]))
        if start_date <= dt < end_date:
            weather_data[int(row[0])] = row[1:]

    # Open the output CSV file
    with open('final_dataset.csv', 'w', newline='') as merged_file:
        writer = csv.writer(merged_file, delimiter=';')

        # Write the header row to the output file
        writer.writerow(['epoch_time', 'nat_demand', 'Holiday_ID', 'holiday', 'school', 'temp', 'dew_point', 'feels_like', 'humidity', 'wind_speed', 'wind_deg'])

        # Loop through each row in the power data and add the corresponding weather data
        for row in power_reader:
            dt = datetime.fromtimestamp(int(row[0]))
            if start_date <= dt < end_date:
                timestamp = int(row[0])
                nat_demand = float(row[1])
                holiday_id = int(row[2])
                holiday = int(row[3])
                school = int(row[4])

                # If there is weather data for this timestamp, add it to the row
                if timestamp in weather_data:
                    weather_row = weather_data[timestamp]
                    temp = float(weather_row[0])
                    dew_point = float(weather_row[1])
                    feels_like = float(weather_row[2])
                    humidity = float(weather_row[3])
                    wind_speed = float(weather_row[4])
                    wind_deg = float(weather_row[5])
                else:
                    temp = None
                    dew_point = None
                    feels_like = None
                    humidity = None
                    wind_speed = None
                    wind_deg = None

                # Write the merged row to the output file
                merged_row = [timestamp, nat_demand, holiday_id, holiday, school, temp, dew_point, feels_like, humidity, wind_speed, wind_deg]
                writer.writerow(merged_row)