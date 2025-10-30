from django.urls import path
from . import views

urlpatterns = [
    path('agregar/', views.agregar_modelo, name='modelo_agregar'),
    path('delete/<int:modelo_id>/', views.eliminar_modelo, name='modelo_eliminar'),
    path('edit/<int:modelo_id>/', views.editar_modelo, name='modelo_editar'),

]