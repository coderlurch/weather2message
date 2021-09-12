from datetime import datetime, timedelta
import weather
import message
from personal_data import contact_data, motion_profile

tmrw = datetime.now() + timedelta(days=1)
is_weekday_tmrw = tmrw.weekday() in range(5)

if is_weekday_tmrw:
    for contact in contact_data.keys():
        personal_motion_data = motion_profile[contact]
        try:
            if tmrw.date().isocalendar()[1]%2 == 0:
                valid_motion_data = personal_motion_data["even"]
            else:
                valid_motion_data = personal_motion_data["odd"]
        except KeyError:
            valid_motion_data = personal_motion_data["general"]
        weather_message = f"\n\nHallo {contact}! \n\n"
        try:
            times = valid_motion_data["Weekday"]
        except KeyError:
            times = valid_motion_data[tmrw.weekday()]
        for time in times.keys():
            tmrw = tmrw.replace(hour=time-1, minute=0)
            location = times[time]
            weather_temp = weather.Weather(location, tmrw)
            weather_message = weather_message + weather_temp.report()
        print(weather_message)
        #message.send_message(weather_message, contact_data[contact])