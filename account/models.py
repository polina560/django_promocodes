from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # bio = models.TextField(blank=True, verbose_name='О себе')
    promocode = models.ForeignKey('promocode.Promocode', on_delete=models.SET_NULL, blank=True, null=True)
    is_used_promocode = models.BooleanField(default=False)

    def __str__(self):
        return f'Профиль {self.user.username}'

