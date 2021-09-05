import weather
from datetime import datetime

MY_LAT = 51.214986 # Your latitude
MY_LONG = 6.804756 # Your longitude

test_coordinates = {"lat":MY_LAT,"lon":MY_LONG}
test_date = datetime.now()

test = weather.Weather(test_coordinates,test_date)
print(test.parse_data(hours=0))