document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('select[name="admin"]').forEach(function(selectAdmin) {

        const modal = selectAdmin.closest('.modal');
        if (!modal) return;

        const dependientes = modal.querySelectorAll(
            'select[name="modelo"], input[name="nfb"], input[name="serie"], input[name="ip"], input[name="usuario"], input[name="clave"]'
        );

        let valoresOriginales = {}; // Guardamos los valores originales

        // Función que habilita/deshabilita campos según Adm
        function actualizarCampos() {
            const habilitar = selectAdmin.value === "True";
            dependientes.forEach(campo => {
                campo.disabled = !habilitar;
            });
        }

        // Guardar los valores originales al abrir el modal
        modal.addEventListener('show.bs.modal', function() {
            valoresOriginales['admin'] = selectAdmin.value;
            dependientes.forEach(campo => {
                valoresOriginales[campo.name] = campo.value;
            });
        });

        // Restaurar los valores al cerrar el modal
        modal.addEventListener('hidden.bs.modal', function() {
            selectAdmin.value = valoresOriginales['admin'];
            dependientes.forEach(campo => {
                campo.value = valoresOriginales[campo.name];
            });

            // Bloquear campos si Adm = False
            actualizarCampos();
        });

        // Ejecutar al cambiar Adm en tiempo real
        selectAdmin.addEventListener('change', actualizarCampos);

        // Inicializa estado al cargar el DOM
        actualizarCampos();
    });
});
