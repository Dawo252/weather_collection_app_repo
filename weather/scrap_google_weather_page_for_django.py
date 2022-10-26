from typing import Dict, List, Tuple
import requests
from bs4 import BeautifulSoup
import datetime

ignore_missing_imports = True

""" funkcja wyciągająca divy z pogodą na dzis z linku """
""" pomysl nad wyciagnieciem tego z jednej dzuej listy zamiast 3 oddzielnych """

url_interia = 'https://pogoda.interia.pl/prognoza-szczegolowa-barczewo,cId,662'
url_google = 'https://weather.com/weather/hourbyhour/l/8e27d7d0e411d0e7b84d1464a5e5e3404d16f22d6fdbf7b1cd9a910912978804'
url_onet = 'https://pogoda.onet.pl/prognoza-pogody/barczewo-268262'
datetime_now = datetime.datetime.now()
""" need to rename variables """


def gather_weather_data_interia_better_solution(url: str) -> Tuple[str, Dict[str, List]]:
    r = requests.get(url)
    site_content = BeautifulSoup(r.text, 'html.parser')
    hour_span = site_content.select('.hour')
    temp_span = site_content.select('.forecast-temp')
    forecast_span = site_content.select('.forecast-phrase')
    weather_data_dictionary_interia = {}
    weather_list = []
    i = 0
    j = 0
    for each_hour in hour_span:
        try:
            temp_int = int(temp_span[j].text.strip('°C'))
            if each_hour.text != '0':
                weather_list.append(each_hour.text + ':00')
                weather_list.append(temp_int)
                weather_list.append(forecast_span[j].text)
                j += 1
            else:
                date = datetime_now + datetime.timedelta(days=i)
                weather_data_dictionary_interia[date.strftime("%Y-%m-%d")] = [
                    weather_list[x:x + 3] for x in
                    range(0, len(weather_list), 3)]
                weather_list = [each_hour.text + ':00', temp_int, forecast_span[j].text]
                i += 1
                j += 1
        except IndexError:
            break
    return 'interia', weather_data_dictionary_interia


# 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 - my token


def gather_weather_data_google_better_solution(url: str) -> Tuple[str, Dict[str, List]]:
    r = requests.get(url)
    weather_data_for_a_day = []
    google_weather_site_content = BeautifulSoup(r.text, 'html.parser')
    big_google_div = google_weather_site_content.select(".HourlyForecast--DisclosureList--3CdxR")

    for weather_div in big_google_div:
        hourly_weather_data_divs = weather_div.select('.DetailsSummary--DetailsSummary--2HluQ')

    weather_data_dictionary_google = {}

    i = 0

    for each in hourly_weather_data_divs:
        hour = each.h3.text
        if hour == '12 am':
            hour = '0:00'
        elif 'am' in hour or hour == '12 pm':
            hour = f'{int(hour[:-2])}:00'
        elif 'pm' in hour:
            hour = f'{int(hour[:-2]) + 12}:00'

        fahrenheit_to_celicious = round((int(each.div.span.text.strip('°')) - 32) * 5 / 9)
        if hour != '0:00' and hourly_weather_data_divs.index(each) != len(hourly_weather_data_divs) - 1:
            weather_data_for_a_day.append(hour)
            weather_data_for_a_day.append(fahrenheit_to_celicious)
            weather_data_for_a_day.append(each.div.find_next('div').span.text)
        else:
            date = datetime_now + datetime.timedelta(days=i)
            weather_data_dictionary_google[date.strftime("%Y-%m-%d")] = [
                weather_data_for_a_day[x:x + 3] for x in
                range(0, len(weather_data_for_a_day), 3)]
            weather_data_for_a_day = [hour, fahrenheit_to_celicious, each.div.find_next('div').span.text]
            i += 1
    return 'google', weather_data_dictionary_google


def gather_weather_data_onet(url: str) -> Tuple[str, Dict[str, List]]:
    r = requests.get(url)
    onet_weather_site_content = BeautifulSoup(r.text, 'html.parser')
    temp = onet_weather_site_content.select('.temperature')
    forecast_phrases = onet_weather_site_content.select('.forecastIconHolder')
    weather_divs = onet_weather_site_content.select('.mainParams')
    weather_list_onet = []
    weather_data_dictionary_onet = {}
    i = 0
    j = 0
    for each in weather_divs:
        # needed, as text from the div had shitload of /t and /n (getting just the center)
        #  ^           ^          ^          ^         ^          ^            ^        ^
        hour = each.div.text[int(len(each.div.text) / 2) - 2:int(len(each.div.text) / 2) + 3]
        if hour.endswith(':00') and hour != '00:00':
            try:
                weather_list_onet.append(hour)
                weather_list_onet.append(int(temp[j + 1].text[-5:-2].strip('\t')))
                weather_list_onet.append(forecast_phrases[j].img['alt'])
                j += 1
            except IndexError:
                break
        elif hour == '00:00' or j == 45:
            date = datetime_now + datetime.timedelta(days=i)
            weather_data_dictionary_onet[date.strftime("%Y-%m-%d")] = [
                weather_list_onet[x:x + 3] for x in
                range(0, len(weather_list_onet), 3)]

            weather_list_onet = [hour, int(temp[j + 1].text[-5:-2].strip('\t')), forecast_phrases[j].img['alt']]
            i += 1
            j += 1

    return 'onet', weather_data_dictionary_onet

#
# print(gather_weather_data_interia_better_solution(url_interia))
# print(gather_weather_data_google_better_solution(url_google))
# print(gather_weather_data_onet(url_onet))
