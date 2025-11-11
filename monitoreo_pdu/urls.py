from django.urls import include, path
from apps.usuario import views
from .views import dashboard

urlpatterns = [
    path('', views.vista_login, name='login'),
    path('logout/', views.desconectar, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('pdu/', include('apps.pdu.urls')),
    path('usuario/', include('apps.usuario.urls')),
    path('ciudad/', include('apps.ciudad.urls')),
    path('marca/', include('apps.marca.urls')),
    path('modelo/', include('apps.modelo.urls')),
    path('regional/', include('apps.regional.urls')),
    path('ubicacion/', include('apps.ubicacion.urls')),
]
