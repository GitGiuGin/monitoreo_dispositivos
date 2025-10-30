document.addEventListener("DOMContentLoaded", () => {
    const botonesEditar = document.querySelectorAll(".btn-editar");
    const detalle = document.getElementById("detalleUsuario");

    botonesEditar.forEach(boton => {
        boton.addEventListener("click", () => {
            const idUsuario = boton.getAttribute("data-id");

            fetch(`/usuario/formulario/${idUsuario}/`)
                .then(response => response.text())
                .then(html => {
                    detalle.innerHTML = html;
                })
                .catch(error => {
                    detalle.innerHTML = `<div class="alert alert-danger">Error al cargar datos.</div>`;
                    console.error(error);
                });
        });
    });
});