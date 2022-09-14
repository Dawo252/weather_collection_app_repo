from django.shortcuts import render
from .scrap_google_weather_page_for_django import gather_weather_interia_better_solution, gather_weather_data_google_better_solution
from django.http import HttpResponse

# Create your views here.


def index(request):
    weather_data_list_interia = gather_weather_interia_better_solution('https://pogoda.interia.pl/prognoza-szczegolowa-barczewo,cId,662')
    weather_data_list_google = gather_weather_data_google_better_solution('https://weather.com/weather/hourbyhour/l/8e27d7d0e411d0e7b84d1464a5e5e3404d16f22d6fdbf7b1cd9a910912978804')
    return render(request, 'weather/index.html', context={'weather_data_list_interia': weather_data_list_interia, 'weather_data_list_google': weather_data_list_google})


