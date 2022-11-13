from api_keys import API_Key
import requests, json

"""
Abby Mueller

https://www.tutorialspoint.com/\
    find-current-weather-of-any-city-using-openweathermap-api-in-python
#https://geekyhumans.com/get-weather-information-using-python/ 
"""


class WeatherCall():

    def __init__(self):
        self.key = API_Key().get_key()

    def query_city_for_weather(self,city, state=""):
        if state != "":
            state = ","+state
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        total_query = base_url + "q=" + city + state + "&APPID=" + self.key

        response = requests.get(total_query)

        if response.status_code == 200:
            resp = response.json()
            main_info = resp["main"]
            #temperature, in kelvin
            curr_temp = main_info["temp"]
            #convert to F
            #print(curr_temp)
            curr_temp = (9/5) * (curr_temp - 273) + 32
            #print(curr_temp)
            weather = resp["weather"][0]["main"]

            return [curr_temp, weather]

    def determine_weather_sentiment(self,temp_weather_list):
        temp = temp_weather_list[0]
        weather = temp_weather_list[0]

        #very "scientific" temperature to sentiment ranking
        if temp <= -20 :
            return -1
        elif -20 < temp <= -10:
            return -0.8
        elif -10 < temp <= 0:
            return -.6
        elif 0 < temp <= 10:
            return -.4
        elif 10 < temp <= 20:
            return -.2
        elif 20 < temp <= 30:
            return 0
        elif 30 < temp <= 40:
            return 0.4
        elif 40 < temp <= 50:
            return 0.6
        elif 50 <= temp <= 60:
            return 0.8
        elif 60 < temp <= 70:
            return 1
        elif 70 < temp <= 80:
            return 0.6
        elif 80 < temp <= 90:
            return -0.2
        elif 90 < temp <= 100:
            return -0.4
        elif 100 < temp <= 110:
            return -0.6
        else:
            return -1

        #weather to sentiment later (add weather to top,)

        

#weather options:
"""
thunderstorm
drizzle
rain
snow
clouds
mist
smoke
haze
dust
fog
sand
ash
squall
tornado
clear

extreme
"""