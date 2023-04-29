import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# Define the start and end dates for the filter
starting_period = '2015-01-03'
ending_period = '2020-06-27'

start_date = datetime.strptime(starting_period, '%Y-%m-%d')
end_date = datetime.strptime(ending_period, '%Y-%m-%d')

# Open the CSV file and read the data
with open('final_dataset.csv') as infile:
    reader = csv.reader(infile, delimiter=';')

    # Skip the header row in the input file
    next(reader)

    # Create lists to store the data
    timestamps = []
    nat_demands = []
    for row in reader:
        # Convert the timestamp to a datetime object and add it to the list
        dt = datetime.fromtimestamp(int(row[0]))
        if start_date <= dt < end_date:
            timestamps.append(dt)

            # Add the nat_demand to the list
            nat_demands.append(float(row[1]))

# Plot the data
fig, ax = plt.subplots()
ax.plot(timestamps, nat_demands)

# Format the x-axis with a date format
date_fmt = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(date_fmt)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

# Add a grid with secondary divisions every 6 months
ax.grid(which='major', axis='both', linestyle='--', linewidth=0.5)
ax.grid(which='minor', axis='both', linestyle='--', linewidth=0.2)
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

# Add axis labels and a title
ax.set_xlabel('Time')
ax.set_ylabel('National Power Demand in Panama (MW)')
ax.set_title('National Power Demand in Panama over Time')

# Show the plot
plt.show()

