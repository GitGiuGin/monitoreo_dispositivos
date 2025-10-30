document.addEventListener("DOMContentLoaded", function() {
    // Selecciona todos los alert dentro del form
    const alerts = document.querySelectorAll('form .alert');
    alerts.forEach(function(alert) {
        // Esperar segundos
        setTimeout(() => {
            // Agrega la clase fade y quita show para animar el cierre
            alert.classList.remove('show');
            alert.classList.add('hide');
            // Opcional: después de 0.5s eliminar del DOM
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});