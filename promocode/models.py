from django.db import models

# Create your models here.

class Promocode(models.Model):
    promocode = models.CharField()
    description = models.CharField()

    def __str__(self):
        return f'{self.promocode}'

class MainModel(models.Model):
    title = models.CharField()
    system = models.CharField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f'{self.title}'

class TestModel (models.Model):
    text = models.TextField()
    number = models.IntegerField()
    date = models.DateField()
    image = models.ImageField()
    file = models.FileField()

    main = models.ForeignKey(MainModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.text}'
