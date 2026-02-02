from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from account.models import UserProfile


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    # Опционально: добавить поля профиля в список отображения пользователей
    list_display = UserAdmin.list_display + ('get_avatar',)

    def get_avatar(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.avatar
        return None

    get_avatar.short_description = 'Аватар'


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)