import csv
import ClassManager as cm
import datetime

# Load the data from the CSV file into a list of LoadData objects
data = []
weather_data_list = []


with open('raw_data/hourly_weather.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        dt = int(row['dt'])
        dt_iso = row['dt_iso']
        timezone = int(row['timezone'])
        city_name = row['city_name']
        lat = float(row['lat'])
        lon = float(row['lon'])
        temp = float(row['temp'])
        visibility = int(row['visibility']) if row['visibility'] != '' else 0
        dew_point = float(row['dew_point']) if row['dew_point'] != '' else 0
        feels_like = float(row['feels_like']) if row['feels_like'] != '' else 0
        temp_min = float(row['temp_min']) if row['temp_min'] != '' else 0
        temp_max = float(row['temp_max']) if row['temp_max'] != '' else 0
        pressure = float(row['pressure']) if row['pressure'] != '' else 0
        sea_level = float(row['sea_level']) if row['sea_level'] != '' else 0
        grnd_level = float(row['grnd_level']) if row['grnd_level'] != '' else 0
        humidity = int(row['humidity']) if row['humidity'] != '' else 0
        wind_speed = float(row['wind_speed'])
        wind_deg = int(row['wind_deg'])
        wind_gust = float(row['wind_gust']) if row['wind_gust'] != '' else 0
        rain_1h = float(row['rain_1h'])
        rain_3h = float(row['rain_3h']) if row['rain_3h'] != '' else 0
        snow_1h = float(row['snow_1h']) if row['snow_1h'] != '' else 0
        snow_3h = float(row['snow_3h']) if row['snow_3h'] != '' else 0
        clouds_all = int(row['clouds_all'])
        weather_id = int(row['weather_id'])
        weather_main = row['weather_main']
        weather_description = row['weather_description']
        weather_icon = row['weather_icon']

        # Create a new WeatherData object and append it to the list
        weather_data = cm.WeatherData(dt, dt_iso, timezone, city_name, lat, lon, temp, visibility, dew_point,
                                   feels_like, temp_min, temp_max, pressure, sea_level, grnd_level, humidity,
                                   wind_speed,
                                   wind_deg, wind_gust, rain_1h, rain_3h, snow_1h, snow_3h, clouds_all, weather_id,
                                   weather_main, weather_description, weather_icon)
        weather_data_list.append(weather_data)


filtered_weather_data_list = []

with open('raw_data/hourly_load.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    # Loop through each row in the CSV file
    for row in csv_reader:
        # Extract the values from the row
        date_str = row[0]
        hour = int(row[1])
        load = float(row[2])
        # Create a new LoadData object and append it to the list
        new_data = cm.LoadData(date_str, hour, load)
        data.append(new_data)


initial_time = data[0].epoch_timestamp

for item in weather_data_list:
    if item.dt > initial_time:
        filtered_data = {
            'dt': item.dt,
            'temp': item.temp,
            'dew_point': item.dew_point,
            'feels_like': item.feels_like,
            'humidity': item.humidity,
            'wind_speed': item.wind_speed,
            'rain_1h': item.rain_1h
        }
        filtered_weather_data_list.append(filtered_data)

weather_data_list = filtered_weather_data_list

final_array= []

for load_data in data:
    epoch_timestamp = load_data.epoch_timestamp
    for weather_data in weather_data_list:
        if (weather_data['dt']) == epoch_timestamp:
            sub_array= {
            'epoch': weather_data['dt'],
            'temp': weather_data['temp'],
            'dew_point': weather_data['dew_point'],
            'feels_like': weather_data['feels_like'],
            'humidity': weather_data['humidity'],
            'wind_speed': weather_data['wind_speed'],
            'rain_1h': weather_data['rain_1h'],
            'load':load_data.load,
            'date_string': load_data.date_str,
            'hour':load_data.hour
             }
            final_array.append(sub_array)
            break

# Write the combined data to a new CSV file
with open('final_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['epoch', 'temp', 'dew_point', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'load','date_string','hour'])
    for row in final_array:
        writer.writerow([row['epoch'], row['temp'], row['dew_point'], row['feels_like'], row['humidity'], row['wind_speed'], row['rain_1h'], row['load'], row['date_string'], row['hour']])