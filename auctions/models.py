from django.contrib.auth.models import AbstractUser
from django.db import models
import os


class User(AbstractUser):
    pass

class listings(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=120)
    listed_date = models.DateTimeField(auto_now=True)
    picture = models.URLField(max_length=200, null=True)
    seller = models.CharField(max_length=64)
    category = models.CharField(max_length=120)

class closedlistings(models.Model): 
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=120)
    closed_date = models.DateTimeField(auto_now=True)
    picture = models.URLField(max_length=200, null=True)
    listingid = models.IntegerField()
    seller = models.CharField(max_length=64)
    buyer = models.CharField(max_length=64)
    category = models.CharField(max_length=120)

class bidmodel(models.Model):
    name = models.CharField(max_length=64)
    listingid = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)


class comments(models.Model):
    name = models.CharField(max_length=80)
    body = models.TextField()
    listingid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class WatchList(models.Model): 
    name =  models.CharField(max_length=80)
    listingid = models.IntegerField()



    