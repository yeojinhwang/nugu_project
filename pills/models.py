from django.db import models

# Create your models here.

class Pill(models.Model):
    name = models.TextField()