from datetime import datetime, timedelta
import socket
import weather
import message
from personal_data import contact_data, motion_profile

tmrw = datetime.now() + timedelta(days=1)
is_weekday_tmrw = tmrw.weekday() in range(5)


def setup_text_from_weather_object(weather_object, hours=0):
    """

    :param hours:
    :return:
    """
    translate_condition = {"clear-day": "klar",
                           # TODO: add 5 point scale for all weather and local images for condition
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
    hwd = weather_object.parse_data(hours)
    timestamp_dt = datetime.fromisoformat(hwd['timestamp'])
    report = f"Am {timestamp_dt.date().strftime('%d. %B %Y')} um {timestamp_dt.time()} Uhr" \
             f" ist es in {weather_object.city} {translate_condition[hwd['icon']]}: \n" \
             f"Es ist {hwd['temperature']} {weather_object.UNITS['temperature']} warm " \
             f"und es gibt {hwd['precipitation']} {weather_object.UNITS['precipitation']} Niederschlag. \n" \
             f"Die Sonne scheint {hwd['sunshine']} {weather_object.UNITS['sunshine']} pro Stunde. \n" \
             f"Der Wind weht mit {hwd['wind_speed']} {weather_object.UNITS['wind speed']} " \
             f"und es ist zu {hwd['cloud_cover']} {weather_object.UNITS['cloud cover']} bewölkt. \n\n"

    return report


def get_weather_messages(tomorrow):
    weather_messages_dict = {}
    for contact in contact_data.keys():
        personal_motion_data = motion_profile[contact]
        try:
            if tomorrow.date().isocalendar()[1] % 2 == 0:
                valid_motion_data = personal_motion_data["even"]
            else:
                valid_motion_data = personal_motion_data["odd"]
        except KeyError:
            valid_motion_data = personal_motion_data["general"]
        weather_message = f"Hallo {contact}!\n\n"
        try:
            times = valid_motion_data["Weekday"]
        except KeyError:
            times = valid_motion_data[tomorrow.weekday()]
        for time in times.keys():
            tomorrow = tomorrow.replace(hour=time - 1, minute=0)
            location = times[time]
            weather_temp = weather.Weather(location, tomorrow)
            weather_message = weather_message + setup_text_from_weather_object(weather_temp)

        weather_messages_dict[contact] = weather_message
    return weather_messages_dict


def notify():
    content = get_weather_messages(tomorrow=tmrw)
    for contact in contact_data.keys():
        message.send_message("Dein Mari-Wetter-Service",
                             content[contact],
                             contact_data[contact])

if __name__ == "__main__":
    notify()
