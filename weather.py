import requests
from datetime import datetime, timedelta
import numpy as np


class Weather:

    def __init__(self, city, start_date, hours=1):
        self.city = city
        self.coordinates = self.get_geo_data(city)
        self.lat = self.coordinates["lat"]
        self.lon = self.coordinates["lon"]
        self.start_date = start_date
        self.hours = hours

        self.UNITS = {
            "cloud_cover": "%",
            "dew_point": "°C",
            "precipitation": "mm",
            "pressure": "hPa",
            "relative_humidity": "%",
            "sunshine": "min/h",
            "temperature": "°C",
            "visibility": "m",
            "wind_direction": "°",
            "wind_speed": "km/h",
            "wind_gust direction": "°",
            "wind_gust speed": "km/h"
        }

        self.CATEGORIES = {
            "precipitation": [0.1, 0.5, 4, 10, np.inf],
            "sunshine": [0, 15, 30, 45, 60],
            "cloud_cover": [0, 25, 50, 75, 100],
            "wind_speed": [0, 19, 61, 117, np.inf]
        }

        self.SCALES = {0: "○○○○", 1: "●○○○", 2: "●●○○", 3: "●●●○", 4: "●●●●"}

    def get_geo_data(self, city):
        """
        get lat lon info from city name
        :param city:
        :return:
        """
        response = requests.get(f"https://nominatim.openstreetmap.org/search?city={city}&format=json")
        response.raise_for_status()
        json = response.json()
        return {"lat": json[0]["lat"], "lon": json[0]["lon"]}

    def get_data(self):
        """
        get json weather data
        :return:
        """
        start_date_iso = self.start_date.isoformat()
        last_date = self.start_date + timedelta(hours=self.hours)
        last_date_iso = last_date.isoformat()
        response = requests.get(f"https://api.brightsky.dev/weather?date={start_date_iso}&last_date={last_date_iso}"
                                f"&lat={self.lat}&lon={self.lon}")
        response.raise_for_status()
        json = response.json()
        return json

    def get_scale(self, type, value):
        index = np.argwhere(np.array(self.CATEGORIES[type]) >= value).ravel()[0]
        return self.SCALES[index]

    def parse_data(self, hours=0):
        """
        reduce large weather data dict and add scale
        :param hours:
        :return:
        """
        if hours >= self.hours:
            hours = self.hours
        data = self.get_data()
        weather_data = data["weather"][hours]
        hour_weather_data = {"timestamp": weather_data["timestamp"],
                             "precipitation": [weather_data["precipitation"],
                                               self.get_scale("precipitation", weather_data["precipitation"])],
                             "sunshine": [weather_data["sunshine"],
                                          self.get_scale("sunshine", weather_data["sunshine"])],
                             "temperature": weather_data["temperature"],
                             "wind_speed": [weather_data["wind_speed"],
                                            self.get_scale("wind_speed", weather_data["wind_speed"])],
                             "cloud_cover": [weather_data["cloud_cover"],
                                             self.get_scale("cloud_cover", weather_data["cloud_cover"])],
                             "condition": weather_data["condition"],
                             "icon": weather_data["icon"]
                             }
        return hour_weather_data

    def report(self, hours=0):
        """
        create written report
        :param hours:
        :return:
        """
        translate_condition = {"clear-day": "klar",
                               "clear-night": "klar",
                               "partly-cloudy-day": "teilweise bewölkt",
                               "partly-cloudy-night": "teilweise bewölkt",
                               "cloudy": "bewölkt",
                               "fog": "neblig",
                               "rain": "regnerisch",
                               "sleet": "Schneeregen geben",
                               "snow": "schneien",
                               "hail": "hageln",
                               "thunderstorm": "gewittrig"
                               }
        hwd = self.parse_data(hours)
        timestamp_dt = datetime.fromisoformat(hwd['timestamp'])
        report = f"Am {timestamp_dt.date().strftime('%d. %B %Y')} um {timestamp_dt.time()} Uhr" \
                 f" wird es in {self.city} {translate_condition[hwd['icon']]}: \n" \
                 f"Temperatur: {hwd['temperature']} {self.UNITS['temperature']} \n" \
                 f"Niederschlag: {hwd['precipitation'][1]} ({hwd['precipitation'][0]} {self.UNITS['precipitation']}) \n" \
                 f"Sonnenschein: {hwd['sunshine'][1]} ({hwd['sunshine'][0]} {self.UNITS['sunshine']}) \n" \
                 f"Wind: {hwd['wind_speed'][1]} ({hwd['wind_speed'][0]} {self.UNITS['wind_speed']}) \n" \
                 f"Wolken: {hwd['cloud_cover'][1]} ({hwd['cloud_cover'][0]} {self.UNITS['cloud_cover']}) \n\n"

        return report
