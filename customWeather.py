import requests
import datetime  # for unix UTC conversion


# COMPLEX WEATHER
def fullData():
    # GET URL AND ENTER KEYS
    key = input('Enter your API key: ')
    location = input('Enter the location to search: ')
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + key

    # LOAD DATA
    r = requests.get(url)
    response_dict = r.json()
    location = response_dict['name']
    country = response_dict['sys']['country']
    latitude = response_dict['coord']['lat']
    longitude = response_dict['coord']['lon']

    weather = response_dict['weather'][0]['main']
    weatherDesc = response_dict['weather'][0]['description']

    temperature = response_dict['main']['temp']-273.16  # convert to Celcsius
    maximum = response_dict['main']['temp_max']-273.16
    minimum = response_dict['main']['temp_min']-273.16
    humidity = response_dict['main']['humidity']
    pressure = response_dict['main']['pressure']

    cloudCover = response_dict['clouds']['all']  # in percentage
    windspeed = response_dict['wind']['speed']   # in m/s
    try:
        windDir = response_dict['wind']['deg']       # in degrees
    except KeyError:
        windDir = 'no data'

    sunrise = response_dict['sys']['sunrise']  # both of these in unix UTC
    sunset = response_dict['sys']['sunset']

    # DISPLAY DATA
    print(location + ', ' + country)
    print('Lat:', latitude)
    print('Lon:', longitude)

    print('\n' + weather + ', ' + weatherDesc)
    print('Temp: %.2f' % temperature + '°C')
    print('Max: %.2f' % maximum + '°C')
    print('Min: %.2f' % minimum + '°C')

    print('\nHumidity: %.2f' % humidity + '%')
    print('Pressure: %.2f' % pressure + 'hPa')
    print('Clouds: %.1f' % cloudCover + ' % cover')

    print('Wind blowing %.2f ' % windspeed + 'm/s at bearing ' + str(windDir))

    print('\nSunrise')
    print(datetime.datetime.fromtimestamp(int(sunrise)).strftime('%H:%M:%S:%A'))
    print('Sunset')
    print(datetime.datetime.fromtimestamp(int(sunset)).strftime('%H:%M:%S:%A'))

def forcastDays():
    key = input('Enter your API key: ')
    location = input('Enter the location to search: ')

    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + location + '&cnt=5&mode=json&appid=' + key
    days = int(input('How many days to forcast? (max. 16): '))

    # LOAD DATA
    r = requests.get(url)
    response_dict = r.json()
    # GET NUMBER OF DAYS
    print(str(days) + '-day forcast for ' + response_dict['city']['name'] + ', ' + response_dict['city']['country'])

    # RUN FOR LOOP BASED ON GIVEN DAYS
    for i in range(days):
        today = response_dict['list'][i]
        # GET THE DAY BASED ON UNIX TIMESTAMP
        print('\n' + datetime.datetime.fromtimestamp(today['dt']).strftime('%A'))
        print(today['weather'][0]['main'] + ', ' + today['weather'][0]['description'])
        print('Humidity: ' + str(today['humidity']) + '%')
        print('Cloud Cover: ' + str(today['clouds']) + '%')
        print('The wind is blowing at ' + str(today['speed']) + 'm/s at bearing ' + str(today['deg']))
        print('Max: %.2f' % (float((today['temp']['max'])-273.16)) + '°C')
        print('Min: %2.f' % (float((today['temp']['min'])-273.16)) + '°C')


# USER CHOICE
print('Would you like weather or a forcast?')
userChoice = int(input('1: Weather   2: Forcast   \n>> '))
if userChoice == 1:
    fullData()

elif userChoice == 2:
    forcastDays()
else:
    print('Invalid input!')
