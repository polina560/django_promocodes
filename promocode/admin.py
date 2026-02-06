from ckeditor.fields import RichTextFormField, RichTextField
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models
from django.forms import TextInput, NumberInput

from django.contrib.admin import SimpleListFilter

from promocode.models import TestModel, MainModel, Promocode, ListModel


# Register your models here.

class ActiveFilter(SimpleListFilter):
    title = "status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [("active", "Active"), ("inactive", "Inactive")]

    def queryset(self, request, qs):
        if self.value() == "active":
            return qs.filter(active=True)
        if self.value() == "inactive":
            return qs.filter(active=False)
        return qs

class TestModelInline(admin.StackedInline):
    list_display = ("text", "number", "image", "is_active")
    model = TestModel

@admin.register(ListModel)
class ListModelAdmin(admin.ModelAdmin):
    search_fields = ["title"]


@admin.register(MainModel)
class MainModelAdmin(admin.ModelAdmin):
    inlines = [TestModelInline]

    search_fields = ["title"]
    list_filter = ("title", "created_at", ActiveFilter)
    list_display = ("title", "system", "created_at", "active")

    # пагинация
    # list_per_page = 3
    # preserve_filters = True
    # save_on_top = True

    # редактор текста на тектсовых полях
    # formfield_overrides = {
    #     models.CharField: {"widget": CKEditorWidget(attrs={"size": 60})},
    # }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Применяем CKEditor только к полю 'title'
        form.base_fields['title'].widget = CKEditorWidget()
        return form


    #  поиск по выпадающему списку
    autocomplete_fields = ["list"]

    # def list_title(self, obj):
    #     return obj.list.title
    #
    # list_title.admin_order_field = "list_name"
    # list_title.short_description = "List"



@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    # поиск по полю
    search_fields = ["promocode"]
    search_help_text = "Search by promocode"

    # поля в таблице
    list_display = ("promocode", "description")

    # массовое редактирование
    list_editable = ("description",)
    list_display_links = ("promocode",)
