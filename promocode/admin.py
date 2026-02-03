from django.contrib import admin

from promocode.models import TestModel, MainModel


# Register your models here.

class TestModelInline(admin.StackedInline):
    # list_display = ('text',)
    model = TestModel

@admin.register(MainModel)
class MainModelAdmin(admin.ModelAdmin):
    inlines = [TestModelInline]