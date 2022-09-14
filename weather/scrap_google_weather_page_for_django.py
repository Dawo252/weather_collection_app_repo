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


# def gather_weather_interia_better_solution(url: str) -> List:
#     r = requests.get(url)
#     site_content = BeautifulSoup(r.text, 'html.parser')
#     print(type(site_content))
#     weather_divs_interia = site_content.findAll('span', attrs={'class': re.compile('^(weather-forecast-hbh-day-label|hour|temp-info|forecast-phrase)')})
#     weather_divs_temperature_interia = []
#     lista = []
#
#     for each_temp_div in weather_divs_interia:
#         try:
#             if each_temp_div['class'] == ['weather-forecast-hbh-day-labelRight'] and len(lista) > 0:
#                 weather_divs_temperature_interia.append(lista)
#                 lista = []
#                 lista.append(each_temp_div.text)
#             elif each_temp_div['class'] == ['temp-info']:
#                 lista.append(each_temp_div.span.text)
#             else:
#                 if len(each_temp_div.text) == 1 or len(each_temp_div.text) == 2:
#                     lista.append(each_temp_div.text+":00")
#                 else:
#                     lista.append(each_temp_div.text)
#         except AttributeError:
#             continue
#     return weather_divs_temperature_interia[:3]


""" need to rename variables """


def gather_weather_interia_better_solution(url: str) -> List:
    r = requests.get(url)
    site_content = BeautifulSoup(r.text, 'html.parser')
    print(type(site_content))
    weather_divs_interia = site_content.findAll('span', attrs={'class': re.compile('^(weather-forecast-hbh-day-label|hour|temp-info|forecast-phrase)')})
    weather_data_dictionary_interia = {}
    lista = []

    for each_temp_div in weather_divs_interia:
        try:
            if each_temp_div['class'] == ['weather-forecast-hbh-day-labelRight']:
                lista = []
                weather_data_dictionary_interia[each_temp_div.text] = lista
            elif each_temp_div['class'] == ['temp-info']:
                lista.append(each_temp_div.span.text)
            else:
                if len(each_temp_div.text) == 1 or len(each_temp_div.text) == 2:
                    lista.append(each_temp_div.text+":00")
                else:
                    lista.append(each_temp_div.text)
        except AttributeError:
            continue
    return weather_data_dictionary_interia

# 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 - my token

def gather_weather_data_google_better_solution(url: str) -> Dict[str, List]:
    r = requests.get(url)
    weather_data_for_a_day = []
    google_weather_site_content = BeautifulSoup(r.text, 'html.parser')
    google_weather_site_content.select(".HourlyForecast--DisclosureList--3CdxR")
    for weather_div in google_weather_site_content.select(".HourlyForecast--DisclosureList--3CdxR"):
        day = weather_div.select('.HourlyForecast--longDate--1tdaJ')
        day2 = weather_div.select('.DetailsSummary--DetailsSummary--2HluQ')

    weather_data_dictionary_google = {}

    i = 0
    for each in day2:
        fahrenheit_to_delicious = str(round((int(each.div.span.text.strip('°')) - 32) * 5 / 9))
        if each.h3.text != '12 am' and day2.index(each) != len(day2) - 1:
            weather_data_for_a_day.append(each.h3.text)
            weather_data_for_a_day.append(fahrenheit_to_delicious+'°C')
            weather_data_for_a_day.append(each.div.find_next('div').span.text)
        else:
            weather_data_dictionary_google[day[i].text] = weather_data_for_a_day
            weather_data_for_a_day = [each.h3.text, fahrenheit_to_delicious+'°C', each.div.find_next('div').span.text]
            i += 1
    return weather_data_dictionary_google


print(gather_weather_interia_better_solution(url_interia))
