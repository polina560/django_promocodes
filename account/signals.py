import secrets

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_user_token(sender, instance, created, **kwargs):
    """
    Создает рандомный токен для нового пользователя
    """
    if created:
        instance.token = secrets.token_urlsafe(32)
        UserProfile.objects.filter(pk=instance.pk).update(token=instance.token)