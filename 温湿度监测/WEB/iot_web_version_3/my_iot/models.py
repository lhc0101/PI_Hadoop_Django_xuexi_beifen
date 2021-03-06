from django.db import models

class HistoryValue(models.Model):
    temperature = models.CharField(max_length=32)
    humidity = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)
class Temperature(models.Model):
    temperature = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)

class Humidity(models.Model): 
    humidity = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)