from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import apps.pdu.dashboard as dash

@login_required
def dashboard(request):
    if request.user.cambiar_password:
        messages.warning(request, "Debes actualizar tu contraseña antes de continuar.", extra_tags="info")
        mostrar_modal = True
    else:
        mostrar_modal = False

    regionales, datasets_regional = dash.por_regional()
    
    context = {
        'mostrar_modal': mostrar_modal,
        'por_tipo': list(dash.por_tipo()),
        'por_ciudad': list(dash.por_ciudad()),
        'adm_data': dash.dispositivos_administrables(),
        'adm_por_regional': dash.dispositivos_adm_por_regional(),
        'adm_ip_chart': dash.dispositivos_con_ip(),
        'regionales': regionales,
        'datasets_regional': datasets_regional,
    }
    return render(request, 'dashboard.html', context)