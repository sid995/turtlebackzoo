from django.db import models


# Create your models here.
class Employee(models.Model):
    id = models.IntegerField().primary_key
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
