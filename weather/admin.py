from django.contrib import admin

from .models import WeatherTable, WeatherProvider

admin.site.register(WeatherTable)
admin.site.register(WeatherProvider)