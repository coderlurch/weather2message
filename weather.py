import requests
from datetime import datetime, timedelta

class Weather:

    def __init__(self,city, start_date, hours=1):
        self.city = city
        self.coordinates = self.city_to_OSM_data(city)
        self.lat = self.coordinates["lat"]
        self.lon = self.coordinates["lon"]
        self.start_date = start_date
        self.hours = hours

        self.UNITS = {
            "cloud cover": "%",
            "dew point": "°C",
            "precipitation": "mm",
            "pressure": "hPa",
            "relative humidity": "%",
            "sunshine": "min",
            "temperature": "°C",
            "visibility": "m",
            "wind direction": "°",
            "wind speed": "km / h",
            "wind gust direction": "°",
            "wind gust speed": "km / h"
        }

    def city_to_OSM_data(self,city):
        response = requests.get(f"https://nominatim.openstreetmap.org/search?city={city}&format=json")
        response.raise_for_status()
        json = response.json()
        return {"lat": json[0]["lat"], "lon": json[0]["lon"]}

    def build_url(self):
        """

        :return:
        """
        start_date_iso = self.start_date.isoformat()
        last_date = self.start_date + timedelta(hours=self.hours)
        last_date_iso = last_date.isoformat()
        return f"https://api.brightsky.dev/weather?date={start_date_iso}&last_date={last_date_iso}" \
               f"&lat={self.lat}&lon={self.lon}"

    def get_data(self):
        """

        :return:
        """
        response = requests.get(self.build_url())
        response.raise_for_status()
        json = response.json()
        return json

    def parse_data(self,hours=0):
        """

        :param hours:
        :return:
        """
        if hours >= self.hours:
            hours = self.hours
        data = self.get_data()
        weather_data = data["weather"][hours]
        hour_weather_data = {"timestamp": weather_data["timestamp"],
                             "precipitation": weather_data["precipitation"],
                             "sunshine": weather_data["sunshine"],
                             "temperature": weather_data["temperature"],
                             "wind_speed": weather_data["wind_speed"],
                             "cloud_cover": weather_data["cloud_cover"],
                             "condition": weather_data["condition"],
                             "icon": weather_data["icon"]
                             }
        return hour_weather_data

    def report(self,hours=0):
        """

        :param hours:
        :return:
        """
        translate_condition = {"dry":"trocken",
                               "fog":"neblig",
                               "rain":"regnerisch",
                               "sleet":"Schneeregen geben",
                               "snow":"schneien",
                               "hail":"hageln",
                               "thunderstorm":"gewittrig"
                               }
        hwd = self.parse_data(hours)
        timestamp_dt = datetime.fromisoformat(hwd['timestamp'])
        report = f"Am {timestamp_dt.date().strftime('%d. %B %Y')} um {timestamp_dt.time()} Uhr"\
                 f" wird es in {self.city} {translate_condition[hwd['condition']]} werden."\
                 f" Es wird {hwd['temperature']} {self.UNITS['temperature']} warm werden"\
                 f" und {hwd['precipitation']} {self.UNITS['precipitation']} Niederschlag geben."\
                 f" Die Sonne wird {hwd['sunshine']} {self.UNITS['sunshine']} pro Stunde scheinen."\
                 f" Es wird {hwd['wind_speed']} {self.UNITS['wind speed']} Wind geben"\
                 f" und zu {hwd['cloud_cover']} {self.UNITS['cloud cover']} bewölkt sein. \n\n"\

        return report

