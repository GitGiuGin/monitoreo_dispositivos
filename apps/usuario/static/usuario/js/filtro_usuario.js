document.addEventListener("DOMContentLoaded", () => {
    const inputBusqueda = document.getElementById("busquedaUsuarios");
    const tabla = document.querySelector("table tbody");

    inputBusqueda.addEventListener("keyup", () => {
        const filtro = inputBusqueda.value.toLowerCase();
        const filas = tabla.querySelectorAll("tr");

        filas.forEach(fila => {
            const columnas = fila.querySelectorAll("td");
            if (columnas.length === 0) return; // ignora fila vacía
            const usuario = columnas[0].textContent.toLowerCase();
            const rol = columnas[1].textContent.toLowerCase();
            const estado = columnas[2].textContent.toLowerCase();

            if (usuario.includes(filtro) || rol.includes(filtro) || estado.includes(filtro)) {
                fila.style.display = "";
            } else {
                fila.style.display = "none";
            }
        });
    });
});