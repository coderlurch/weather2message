import requests
from datetime import timedelta

class Weather:

    UNITS = {
        "cloud cover":"%",
        "dew point":"°C",
        "precipitation":"mm",
        "pressure":"hPa",
        "relative humidity":"%",
        "sunshine":"min",
        "temperature":"°C",
        "visibility":"m",
        "wind direction":"°",
        "wind speed":"km / h",
        "wind gust direction":"°",
        "wind gust speed":"km / h"
    }

    def __init__(self,coordinates, start_date, hours=1):
        self.coordinates = coordinates
        self.start_date = start_date
        self.hours = hours

    def build_url(self):
        self.lat = self.coordinates["lat"]
        self.lon = self.coordinates["lon"]
        start_date_iso = self.start_date.isoformat()
        last_date = self.start_date + timedelta(hours=self.hours)
        last_date_iso = last_date.isoformat()
        return f"https://api.brightsky.dev/weather?date={start_date_iso}&last_date={last_date_iso}" \
               f"&lat={self.lat}&lon={self.lon}"

    def get_data(self):
        response = requests.get(self.build_url())
        response.raise_for_status()
        json = response.json()
        return json

    def parse_data(self,hours):
        if hours >= self.hours:
            hours = self.hours
        data = self.get_data()
        weather_data = data["weather"][hours]
        hour_weather_data = {}
        hour_weather_data["timestamp"] = weather_data["timestamp"]
        hour_weather_data["precipitation"] = weather_data["precipitation"]
        hour_weather_data["sunshine"] = weather_data["sunshine"]
        hour_weather_data["temperature"] = weather_data["temperature"]
        hour_weather_data["wind_speed"] = weather_data["wind_speed"]
        hour_weather_data["cloud_cover"] = weather_data["cloud_cover"]
        hour_weather_data["condition"] = weather_data["condition"]
        hour_weather_data["icon"] = weather_data["icon"]
        return hour_weather_data

    def report(self,hours):
        "add written report of hourly weather"


