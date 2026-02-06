from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Promocode(models.Model):
    promocode = models.CharField( verbose_name =_('Promocode'), max_length=100)
    description = models.CharField(verbose_name =_('Description'))

    class Meta:
        verbose_name = _('Promocode')  # Название в единственном числе
        verbose_name_plural = _('Promocodes')  # Название во множественном числе


    def __str__(self):
        return f'{self.promocode}'

class ListModel(models.Model):
    title = models.CharField( verbose_name =_('Title'), max_length=100)

    def __str__(self):
        return f'{self.title}'

class MainModel(models.Model):
    title = models.CharField(verbose_name =_('Name'),  max_length=100)
    system = models.CharField(max_length=100)

    created_at = models.DateField(verbose_name =_('Created at'), null=True, blank=True)
    updated_at = models.DateField(verbose_name =_('Updated at'), null=True, blank=True)

    active = models.BooleanField(verbose_name =_('Active'), default=True)

    list = models.ForeignKey(ListModel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('Main Model')  # Название в единственном числе
        verbose_name_plural = _('Main Model')  # Название во множественном числе

    def __str__(self):
        return f'{self.title}'

class TestModel (models.Model):
    text = RichTextField(verbose_name =_('Text'))
    number = models.IntegerField(verbose_name =_('Number'))
    date = models.DateField(verbose_name =_('Date'), null=True, blank=True)
    image = models.ImageField(verbose_name =_('Image'), null=True, blank=True)
    file = models.FileField(verbose_name =_('File'), null=True, blank=True)

    is_active = models.BooleanField(verbose_name =_('Active'), default=True)


    main = models.ForeignKey(MainModel, on_delete=models.CASCADE, null=True, related_name='tests')

    class Meta:
        verbose_name = _('Test Model')  # Название в единственном числе
        verbose_name_plural = _('Test Model')  # Название во множественном числе

    def __str__(self):
        return f'{self.text}'



