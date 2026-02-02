from django.db import models

# Create your models here.

class Promocode(models.Model):
    promocode = models.CharField()
    description = models.CharField()

    def __str__(self):
        return f'{self.promocode}'