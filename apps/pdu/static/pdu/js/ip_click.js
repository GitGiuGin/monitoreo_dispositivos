document.addEventListener('DOMContentLoaded', () => {

    // Seleccionamos todas las IPs con <a>
    const ipLinks = document.querySelectorAll('td a');

    ipLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Evita que abra el enlace inmediatamente

            const fila = link.closest('tr');
            const estadoTd = fila.querySelector('td[id^="estado-"]');
            if (!estadoTd) return;

            const estadoBadge = estadoTd.querySelector('span.badge');
            const estadoText = estadoBadge ? estadoBadge.textContent.trim() : '';

            if (estadoText === 'Activa') {
                // Si está activa, abre el enlace en nueva pestaña
                window.open(link.href, '_blank');
            } else {
                // Recuperamos dispositivo y ubicación
                const dispositivo = fila.querySelector('td:nth-child(6)').textContent.trim();
                const ubicacion = fila.querySelector('td:nth-child(3)').textContent.trim();

                // Actualizamos modal
                const modalTitulo = document.getElementById('alertaIPModalLabel');
                const modalMensaje = document.getElementById('alertaIPMensaje');

                modalTitulo.innerHTML = `¡Alerta de ${dispositivo}!`;
                modalMensaje.innerHTML = `El ${dispositivo} ubicado en <b>${ubicacion}</b> no tiene comunicación.`;

                const alertaModal = new bootstrap.Modal(document.getElementById('alertaIPModal'));
                alertaModal.show();
            }
        });
    });

});
