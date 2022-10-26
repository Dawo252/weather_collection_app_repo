import datetime

from django.db import models

# Create your models here.


class WeatherImages(models.Model):
    image = models.FileField()


class WeatherProvider(models.Model):
    provider_name = models.CharField(default='cooos', max_length=30)


class WeatherTable(models.Model):
    weather_provider = models.ForeignKey(WeatherProvider, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now())
    hour = models.CharField(max_length=6)
    temperature = models.IntegerField(default=1000)
    weather_description = models.CharField(max_length=30)
