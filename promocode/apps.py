from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class PromocodeConfig(AppConfig):
    name = 'promocode'

    class Meta:
        verbose_name = _('Promocode')
        verbose_name_plural = _('Promocodes')
