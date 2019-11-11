from django.db import models

# Create your models here.

class Info(models.Model):
    title = models.CharField(max_length=200)
    kitchen = models.CharField(max_length=200)
    review_count = models.IntegerField()
    average_delivery_time = models.CharField(max_length=200)
    delivery_cost = models.CharField(max_length=200)
    minimum_order = models.CharField(max_length=200)
    rating_number = models.FloatField(max_length=200)