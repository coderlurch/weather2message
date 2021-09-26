from datetime import datetime, timedelta
import socket
import emoji
import weather
import message
from personal_data import contact_data, motion_profile

from flask import Flask
app = Flask(__name__)

tmrw = datetime.now() + timedelta(days=3)
is_weekday_tmrw = tmrw.weekday() in range(5)


def setup_text_from_weather_object(weather_object,hours=0):
    """

    :param hours:
    :return:
    """
    translate_condition = {"clear-day":"klar",
                           "clear-night":"klar",
                           "partly-cloudy-day":"teilweise bewölkt",
                           "partly-cloudy-night":"teilweise bewölkt",
                           "cloudy":"bewölkt",
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
             f" ist es in {weather_object.city} {translate_condition[hwd['icon']]}: <br>" \
             f" <ul> <li> Es ist {hwd['temperature']} {weather_object.UNITS['temperature']} warm </li>" \
             f" <li> und es gibt {hwd['precipitation']} {weather_object.UNITS['precipitation']} Niederschlag. </li> " \
             f" <li> Die Sonne scheint {hwd['sunshine']} {weather_object.UNITS['sunshine']} pro Stunde. </li> " \
             f" <li> Der Wind weht mit {hwd['wind_speed']} {weather_object.UNITS['wind speed']} </li> " \
             f" <li> und es ist zu {hwd['cloud_cover']} {weather_object.UNITS['cloud cover']} bewölkt. </li> </ul> " \

    return report

def get_weather_messages(tomorrow):
    weather_messages_dict = {}
    for contact in contact_data.keys():
        personal_motion_data = motion_profile[contact]
        try:
            if tomorrow.date().isocalendar()[1]%2 == 0:
                valid_motion_data = personal_motion_data["even"]
            else:
                valid_motion_data = personal_motion_data["odd"]
        except KeyError:
            valid_motion_data = personal_motion_data["general"]
        weather_message = f'<h1> Hallo {contact}! </h1>'
        try:
            times = valid_motion_data["Weekday"]
        except KeyError:
            times = valid_motion_data[tomorrow.weekday()]
        for time in times.keys():
            tomorrow = tomorrow.replace(hour=time-1, minute=0)
            location = times[time]
            weather_temp = weather.Weather(location, tomorrow)
            weather_message = weather_message + "<body>" + setup_text_from_weather_object(weather_temp)+ "</body>"

        weather_messages_dict[contact] = weather_message
    return weather_messages_dict

@app.route('/<name>')
def post_weather_message(name):
    if is_weekday_tmrw:
        content = get_weather_messages(tomorrow=tmrw)
        return content[name]
    else:
        return "enjoy your weekend!"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def notify():
    for contact in contact_data.keys():
        message.send_message(f"Hi {contact}! Dein Wetter für morgen ist online: "
              f"http://{get_ip()}:5000/{contact}",contact_data[contact])

if __name__ == "__main__":
    app.run(host='0.0.0.0')




