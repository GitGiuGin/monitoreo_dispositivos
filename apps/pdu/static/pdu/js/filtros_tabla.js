document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const tbody = document.querySelector("table tbody");
    const pagination = document.querySelector(".pagination");

    function actualizarTabla() {
        const params = new URLSearchParams(new FormData(form));
        fetch(`?${params}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(res => res.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");

                // Reemplaza el contenedor completo (tabla + modales)
                const nuevoContenedor = doc.querySelector("#tabla-container");
                if (nuevoContenedor) {
                    document.getElementById("tabla-container").innerHTML = nuevoContenedor.innerHTML;
                }
                // Actualiza mensaje "Mostrando X de Y"
                const mensaje = doc.querySelector("#mensaje-datos");
                if (mensaje) {
                    const total = mensaje.dataset.total;
                    const mostrados = doc.querySelectorAll("#tabla-container tbody tr").length;
                    document.getElementById("mensaje-datos").innerHTML =
                        `Mostrando ${mostrados} de ${total} dispositivos`;
                }

                actualizarPaginacion(); // mantiene la funcionalidad de paginación
            })
            .catch(err => console.error(err));
    }

    function actualizarPaginacion() {
        const page = form.querySelector("input[name='page']").value;
        const items = document.getElementById("items").value;
        const marca = form.querySelector("input[name='marca']").value;
        const nfb = form.querySelector("input[name='nfb']").value;
        const serie = form.querySelector("input[name='serie']").value;
        const admin = form.querySelector("select[name='admin']").value;

        // Actualiza todos los enlaces de paginación
        pagination.querySelectorAll("a").forEach(a => {
            const url = new URL(a.href);
            url.searchParams.set("page", a.textContent.trim()); // número de página o "Anterior"/"Siguiente"
            url.searchParams.set("items", items);
            url.searchParams.set("marca", marca);
            url.searchParams.set("nfb", nfb);
            url.searchParams.set("serie", serie);
            url.searchParams.set("admin", admin);
            a.href = url.toString();

            a.onclick = function(e) {
                e.preventDefault();
                let p = url.searchParams.get("page");
                if(a.textContent.trim() === "Anterior") p = parseInt(page) - 1;
                if(a.textContent.trim() === "Siguiente") p = parseInt(page) + 1;
                form.querySelector("input[name='page']").value = p;
                actualizarTabla();
            };
        });
    }

    // Inicializa listeners de filtros
    form.querySelectorAll("input, select").forEach(el => {
        el.addEventListener("input", () => {
            form.querySelector("input[name='page']").value = 1;
            actualizarTabla();
        });
        el.addEventListener("change", () => {
            form.querySelector("input[name='page']").value = 1;
            actualizarTabla();
        });
    });

    // Selector de items
    document.getElementById("items").addEventListener("change", () => {
        form.querySelector("input[name='page']").value = 1;
        actualizarTabla();
    });

    document.getElementById("items").addEventListener("change", () => {
        form.querySelector("input[name='page']").value = 1;
        actualizarTabla();
    });
});
