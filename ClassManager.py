import datetime
import pytz

class WeatherData:
    def __init__(self, dt, dt_iso, timezone, city_name, lat, lon, temp, visibility, dew_point, feels_like, temp_min,
                 temp_max, pressure, sea_level, grnd_level, humidity, wind_speed, wind_deg, wind_gust, rain_1h, rain_3h,
                 snow_1h, snow_3h, clouds_all, weather_id, weather_main, weather_description, weather_icon):
        self.dt = dt
        self.dt_iso = dt_iso
        self.timezone = timezone
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.temp = temp
        self.visibility = visibility
        self.dew_point = dew_point
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.sea_level = sea_level
        self.grnd_level = grnd_level
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.wind_gust = wind_gust
        self.rain_1h = rain_1h
        self.rain_3h = rain_3h
        self.snow_1h = snow_1h
        self.snow_3h = snow_3h
        self.clouds_all = clouds_all
        self.weather_id = weather_id
        self.weather_main = weather_main
        self.weather_description = weather_description
        self.weather_icon = weather_icon

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, value):
        self._dt = value

    @property
    def dt_iso(self):
        return self._dt_iso

    @dt_iso.setter
    def dt_iso(self, value):
        self._dt_iso = value

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value

    @property
    def city_name(self):
        return self._city_name

    @city_name.setter
    def city_name(self, value):
        self._city_name = value

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, value):
        self._lon = value

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        self._temp = value

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = value

    @property
    def dew_point(self):
        return self._dew_point

    @dew_point.setter
    def dew_point(self, value):
        self._dew_point = value

    @property
    def feels_like(self):
        return self._feels_like

    @feels_like.setter
    def feels_like(self, value):
        self._feels_like = value

    @property
    def temp_min(self):
        return self._temp_min

    @temp_min.setter
    def temp_min(self, value):
        self._temp_min = value

    @property
    def temp_max(self):
        return self._temp_max

    @temp_max.setter
    def temp_max(self, value):
        self._temp_max = value

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        self._pressure = value

    @property
    def sea_level(self):
        return self._sea_level

    @sea_level.setter
    def sea_level(self, value):
        self._sea_level = value

    @property
    def grnd_level(self):
        return self._grnd_level

    @grnd_level.setter
    def grnd_level(self, value):
        self._grnd_level = value

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        self._humidity = value

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, value):
        self._wind_speed = value

    @property
    def wind_deg(self):
        return self._wind_deg

    @wind_deg.setter
    def wind_deg(self, value):
        self._wind_deg = value

    @property
    def wind_gust(self):
        return self._wind_gust

    @wind_gust.setter
    def wind_gust(self, value):
        self._wind_gust = value

    # Getters and Setters
    @property
    def rain_1h(self):
        return self._rain_1h

    @rain_1h.setter
    def rain_1h(self, value):
        self._rain_1h = value

    @property
    def rain_3h(self):
        return self._rain_3h

    @rain_3h.setter
    def rain_3h(self, value):
        self._rain_3h = value

    @property
    def snow_1h(self):
        return self._snow_1h

    @snow_1h.setter
    def snow_1h(self, value):
        self._snow_1h = value

    @property
    def snow_3h(self):
        return self._snow_3h

    @snow_3h.setter
    def snow_3h(self, value):
        self._snow_3h = value

    @property
    def clouds_all(self):
        return self._clouds_all

    @clouds_all.setter
    def clouds_all(self, value):
        self._clouds_all = value

    @property
    def weather_id(self):
        return self._weather_id

    @weather_id.setter
    def weather_id(self, value):
        self._weather_id = value

    @property
    def weather_main(self):
        return self._weather_main

    @weather_main.setter
    def weather_main(self, value):
        self._weather_main = value

    @property
    def weather_description(self):
        return self._weather_description

    @weather_description.setter
    def weather_description(self, value):
        self._weather_description = value

    @property
    def weather_icon(self):
        return self._weather_icon

    @weather_icon.setter
    def weather_icon(self, value):
        self._weather_icon = value


class LoadData:
    def __init__(self, date_str, hour, load):
        self.date_str = date_str
        self.hour = hour
        self.load = load
        self.date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        self.date_obj = pytz.timezone('UTC').localize(self.date_obj)
        self._epoch_timestamp = int(self.date_obj.timestamp()+(hour*3600))

    def __repr__(self):
        return f"Date: {self.date_str}, Hour: {self.hour}, Load: {self.load}"

    @property
    def date_str(self):
        return self._date_str

    @date_str.setter
    def date_str(self, value):
        self._date_str = value
        self.date_obj = datetime.datetime.strptime(value, "%m/%d/%Y")
        self.date_obj = pytz.timezone('UTC').localize(self.date_obj)
        self._epoch_timestamp = int(self.date_obj.timestamp())

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        self._hour = value

    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, value):
        self._load = value

    @property
    def epoch_timestamp(self):
        return self._epoch_timestamp

    @epoch_timestamp.setter
    def epoch_timestamp(self, value):
        self._epoch_timestamp = value