from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'estado', 'is_staff', 'is_active') 