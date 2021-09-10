import requests
from datetime import datetime, timedelta
import weather
import message
from personal_data import contact_data, motion_profile

tmrw = datetime.now() + timedelta(days=1)
is_weekday_tmrw = True#tmrw.weekday() in range(5)

if is_weekday_tmrw:
    for contact in contact_data.keys():
        weather_message = f"Hallo {contact}! \n"
        try:
            times = motion_profile[contact]["Weekday"]
        except AttributeError:
            times = motion_profile[contact][tmrw.weekday()]
        for time in times.keys():
            tmrw = tmrw.replace(hour=time, minute=0)
            location = times[time]
            weather_temp = weather.Weather(location, tmrw)
            weather_message = weather_message + weather_temp.report() + "\n"
        message.send_message(weather_message, contact_data[contact])