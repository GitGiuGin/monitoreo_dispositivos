from django.contrib import admin

from .models import Marca

@admin.register(Marca)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)