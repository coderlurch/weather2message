from datetime import datetime, timedelta
import socket
from weather import Weather
import message
from personal_data import contact_data, motion_profile

tmrw = datetime.now() + timedelta(days=1)
is_weekday_tmrw = tmrw.weekday() in range(5)

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
            weather_temp = Weather(location, tomorrow)
            weather_message = weather_message + weather_temp.report()

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
