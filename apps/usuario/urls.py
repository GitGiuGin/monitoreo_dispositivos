from django.urls import path
from . import views

urlpatterns = [
    path('changePassword/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('user-management/', views.gestion_usuarios, name='gestion_usuario'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('formulario/<int:usuario_id>/', views.obtener_form_editar_usuario, name='form_editar_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuario/<int:usuario_id>/reset-password/', views.resert_password, name='resert_password'),
]