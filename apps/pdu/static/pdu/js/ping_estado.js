document.addEventListener('DOMContentLoaded', () => {

    let primeraCarga = true; // indica si es la primera vez

    function actualizarEstadoPDUs() {
        const celdas = document.querySelectorAll('td[id^="estado-"]');

        celdas.forEach(td => {
            const fila = td.closest('tr');
            const ipLink = fila.querySelector('td a');

            if (ipLink) {
                const ip = ipLink.textContent.replace(/\s/g, '').trim();

                // Solo mostrar "Verificando..." la primera vez
                if (primeraCarga) {
                    td.innerHTML = '<span class="badge bg-secondary">Verificando...</span>';
                }

                if (!ip) {
                    td.innerHTML = '<span class="text-muted">Sin IP</span>';
                    return; // Salta a la siguiente celda
                }

                fetch(`/pdu/ping/${ip}/`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.activa) {
                            td.innerHTML = `<span class="badge bg-success">Activa</span>
                                            <small class="text-muted">(${data.tiempo_ms.toFixed(1)} ms)</small>`;
                        } else {
                            td.innerHTML = '<span class="badge bg-danger">Inactiva</span>';
                        }
                    })
                    .catch(() => {
                        td.innerHTML = '<span class="badge bg-danger">Error</span>';
                    });
            } else {
                td.innerHTML = '<span class="text-muted">Sin IP</span>';
            }
        });

        primeraCarga = false; // después de la primera ejecución ya no mostrar "Verificando..."
    }

    // Ejecuta al cargar la página
    actualizarEstadoPDUs();

    // Actualiza cada 3 segundos automáticamente
    // setInterval(actualizarEstadoPDUs, 10000);
    let intervaloPing = setInterval(actualizarEstadoPDUs, 10000);

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            clearInterval(intervaloPing);
        } else {
            actualizarEstadoPDUs();
            intervaloPing = setInterval(actualizarEstadoPDUs, 10000);
        }
    });
});
