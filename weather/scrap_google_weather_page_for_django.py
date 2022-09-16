import datetime
import re
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import simplejson as json
ignore_missing_imports = True

""" funkcja wyciągająca divy z pogodą na dzis z linku """
""" pomysl nad wyciagnieciem tego z jednej dzuej listy zamiast 3 oddzielnych """

url_interia = 'https://pogoda.interia.pl/prognoza-szczegolowa-olsztyn,cId,24210'
url_google = 'https://weather.com/weather/hourbyhour/l/8e27d7d0e411d0e7b84d1464a5e5e3404d16f22d6fdbf7b1cd9a910912978804'


""" need to rename variables """


def gather_weather_data_interia_better_solution(url: str) -> Dict[str, List]:
    r = requests.get(url)
    site_content = BeautifulSoup(r.text, 'html.parser')
    # weather_divs_interia = site_content.findAll('span', attrs={'class': re.compile('^(weather-forecast-hbh-day-labelRight|hour|temp-info|forecast-phrase)')}) -> fajne, krotkie, ale beznadziejne w obróbce
    day_span = site_content.select('.weather-forecast-hbh-day-labelRight')
    hour_span = site_content.select('.hour')
    temp_span = site_content.select('.forecast-temp')
    forecast_span = site_content.select('.forecast-phrase')
    weather_data_dictionary_interia = {}
    weather_list = []

    i = 0
    for each_hour in hour_span:
        index = hour_span.index(each_hour)
        if each_hour.text != '0':
            weather_list.append(each_hour.text + ':00')
            weather_list.append(temp_span[index].text)
            weather_list.append(forecast_span[index].text)
        else:
            weather_data_dictionary_interia[day_span[i].text] = [weather_list[x:x+3] for x in range(0, len(weather_list), 3)]
            weather_list = [each_hour.text + ':00', each_hour.text, each_hour.text]
            i += 1
    return weather_data_dictionary_interia

# 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 - my token


def gather_weather_data_google_better_solution(url: str) -> Dict[str, List]:
    r = requests.get(url)
    weather_data_for_a_day = []
    google_weather_site_content = BeautifulSoup(r.text, 'html.parser')
    google_weather_site_content.select(".HourlyForecast--DisclosureList--3CdxR")
    for weather_div in google_weather_site_content.select(".HourlyForecast--DisclosureList--3CdxR"):
        coming_days_list = weather_div.select('.HourlyForecast--longDate--1tdaJ')
        hourly_weather_data_divs = weather_div.select('.DetailsSummary--DetailsSummary--2HluQ')

    weather_data_dictionary_google = {}

    i = 0
    for each in hourly_weather_data_divs:
        fahrenheit_to_delicious = str(round((int(each.div.span.text.strip('°')) - 32) * 5 / 9))
        if each.h3.text != '12 am' and hourly_weather_data_divs.index(each) != len(hourly_weather_data_divs) - 1:
            weather_data_for_a_day.append(each.h3.text)
            weather_data_for_a_day.append(fahrenheit_to_delicious+'°C')
            weather_data_for_a_day.append(each.div.find_next('div').span.text)
        else:
            weather_data_dictionary_google[coming_days_list[i].text] = [weather_data_for_a_day[x:x+3] for x in range(0, len(weather_data_for_a_day), 3)]
            weather_data_for_a_day = [each.h3.text, fahrenheit_to_delicious+'°C', each.div.find_next('div').span.text]
            i += 1
    return weather_data_dictionary_google

#
# print(gather_weather_data_interia_better_solution(url_interia))
# print(gather_weather_data_google_better_solution(url_google))
