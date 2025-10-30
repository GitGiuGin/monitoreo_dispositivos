from django.db.models.signals import post_migrate
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils import timezone
from .models import Usuario

@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    if not Usuario.objects.filter(usuario='monitoreo').exists():
        Usuario.objects.create_superuser(
            usuario='monitoreo',
            contraseña='b3d3p3.1',
        )
        
@receiver(user_logged_in)
def cerrar_sesiones_anteriores(sender, request, user, **kwargs):
    sesiones = Session.objects.filter(expire_date__gte=timezone.now())
    for s in sesiones:
        data = s.get_decoded()
        if data.get('_auth_user_id') == str(user.id):
            if s.session_key != request.session.session_key:
                s.delete()