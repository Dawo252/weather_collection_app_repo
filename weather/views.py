import datetime

from django.shortcuts import render
from .scrap_google_weather_page_for_django import gather_weather_data_interia_better_solution, \
    gather_weather_data_google_better_solution, gather_weather_data_onet
from django.http import HttpResponse
from .models import WeatherProvider, WeatherTable, WeatherImages
from django.db.models import F


# Create your views here.


# def index(request):
#
#     weather_data_list_interia = gather_weather_data_interia_better_solution(
#         'https://pogoda.interia.pl/prognoza-szczegolowa-barczewo,cId,662')
#     weather_data_list_google = gather_weather_data_google_better_solution(
#         'https://weather.com/weather/hourbyhour/l/8e27d7d0e411d0e7b84d1464a5e5e3404d16f22d6fdbf7b1cd9a910912978804')
#     weather_data_list_onet = gather_weather_data_onet('https://pogoda.onet.pl/prognoza-pogody/barczewo-268262')
#     return render(request, 'weather/index.html', context={'weather_data_list_interia': weather_data_list_interia,
#                                                           'weather_data_list_google': weather_data_list_google,
#                                                           'weather_data_list_onet': weather_data_list_onet})

def index(request):
    weather_data_list_interia = gather_weather_data_interia_better_solution(
        'https://pogoda.interia.pl/prognoza-szczegolowa-barczewo,cId,662')
    weather_data_list_google = gather_weather_data_google_better_solution(
        'https://weather.com/weather/hourbyhour/l/8e27d7d0e411d0e7b84d1464a5e5e3404d16f22d6fdbf7b1cd9a910912978804')
    weather_data_list_onet = gather_weather_data_onet('https://pogoda.onet.pl/prognoza-pogody/barczewo-268262')

    weather_dict_list = [weather_data_list_interia, weather_data_list_google, weather_data_list_onet]

    interia = WeatherProvider.objects.get(provider_name='interia')
    google = WeatherProvider.objects.get(provider_name='google')
    onet = WeatherProvider.objects.get(provider_name='onet')
    # wea = WeatherTable.objects.filter(weather_provider=interia)
    weather_temp_list = []
    weather_tables = WeatherProvider.objects.filter(provider_name='interia').annotate(
        temp=F('weathertable__temperature'))
    for weather_table in weather_tables:
        weather_temp_list.append(weather_table.temp)
    for each in weather_dict_list:
        for key, i in each[1].items():
            for i_i in i:
                if each[0] == 'interia':
                    WeatherTable.objects.update_or_create(weather_provider=interia, date=key, hour=i_i[0],
                                                          defaults={'temperature': i_i[1],
                                                                    'weather_description': i_i[2]})
                elif each[0] == 'google':
                    WeatherTable.objects.update_or_create(weather_provider=google, date=key, hour=i_i[0],
                                                          defaults={'temperature': i_i[1],
                                                                    'weather_description': i_i[2]})
                elif each[0] == 'onet':
                    WeatherTable.objects.update_or_create(weather_provider=onet, date=key, hour=i_i[0],
                                                          defaults={'temperature': i_i[1],
                                                                    'weather_description': i_i[2]})

    # WeatherTable.objects.create(date=datetime.date(1990, 10, 12), hour='1', temperature='1', weather_description='1')
    return HttpResponse(weather_temp_list)
