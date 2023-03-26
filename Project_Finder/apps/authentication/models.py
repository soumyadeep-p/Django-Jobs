from django.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms


class Profile(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length = 200)
	

    def __str__(self):
        return self.name