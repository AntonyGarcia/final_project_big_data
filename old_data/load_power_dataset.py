import csv
from datetime import datetime

# Define the start and end dates for the filter
start_date = datetime.strptime('2015-01-03', '%Y-%m-%d')
end_date = datetime.strptime('2020-06-27', '%Y-%m-%d')

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
