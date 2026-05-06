document.addEventListener("DOMContentLoaded", function () {

    cargarClientes();

    document.getElementById("btnBuscar").addEventListener("click", async function () {

        const texto = document.getElementById("inputBuscar").value.trim();

        if (!texto) {
            cargarClientes();
            return;
        }

        try {
            const url = `http://localhost:3000/api/clientes/buscarValor?valor=${texto}`;

            const res = await fetch(url);
            const data = await res.json();

            if (data.error) {
                alert("Error en la búsqueda");
                return;
            }

            listarClientes(data.resultClientes);

        } catch (error) {
            console.error("Error buscando clientes:", error);
            alert("Error de conexión");
        }
    });

     document.getElementById("btnLimpiar").addEventListener("click", function () {

        // 🧠 limpiar buscador
        document.getElementById("inputBuscar").value = "";

        // 🧠 reset cliente actual
        clienteActualId = null;

        // 🧠 limpiar formulario derecho
        document.getElementById("nombreCliente").value = "";
        document.getElementById("apellido").value = "";
        document.getElementById("dni").value = "";
        document.getElementById("email").value = "";
        document.getElementById("telefono").value = "";

        // 🧠 limpiar reservas
        document.querySelector("#listaReservas tbody").innerHTML = "";

        // 🧠 recargar todos los clientes
        cargarClientes();
    });


});

let clienteActualId = null;

document.addEventListener("click", function (e) {

    if (e.target.classList.contains("btn-ver")) {

        const id = e.target.dataset.id;

        clienteActualId = id; // 👈 GUARDAS EL ID


        // 🔍 Buscar el cliente en memoria o volver a pedirlo al backend
        cargarDetalleCliente(id);
        listarReservasCliente(id);
    }
    if (e.target.classList.contains("btn-borrar")) {

        const id = e.target.dataset.id;

        // 🔍 Buscar el cliente en memoria o volver a pedirlo al backend
        borrarCliente(id, e.target);
    }

});

async function cargarClientes() {
    try {
        const cif = localStorage.getItem("agenciaCIF");

        const url = `http://localhost:3000/api/clientes/buscar?campo=cif&valor=${cif}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.error) {
            alert("Error al cargar clientes");
            return;
        }

        listarClientes(data.resultCliente);

    } catch (error) {
        console.error("Error cargando clientes:", error);
        alert("Error de conexión con el servidor");
    }
}

function listarClientes(clientes) {
    const tbody = document.querySelector("#listaClientes tbody");
    tbody.innerHTML = "";

    if (clientes.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3">No se encontraron clientes</td></tr>`;
        return;
    }

    clientes.forEach(cliente => {
        const fila = document.createElement("tr");

        fila.setAttribute("data-id", cliente.idCliente);

        fila.innerHTML = `
            <td>${cliente.nombre} ${cliente.apellido}</td>
            <td>${cliente.email}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-primary btn-ver" data-id="${cliente.idCliente}">
                    Ver
                </button>
                <button class="btn btn-sm btn-outline-danger btn-borrar" data-id="${cliente.idCliente}">
                    Borrar
                </button>
            </td>
        `;

        tbody.appendChild(fila);
    });
}

async function cargarDetalleCliente(idCliente) {
    try {
        const url = `http://localhost:3000/api/clientes/buscar?campo=idCliente&valor=${idCliente}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.error) {
            alert("Cliente no encontrado");
            return;
        }

        const cliente = data.resultCliente[0];

        // 🧠 Rellenar formulario derecha
        document.getElementById("nombreCliente").value = cliente.nombre;
        document.getElementById("apellido").value = cliente.apellido;
        document.getElementById("dni").value = cliente.dni;
        document.getElementById("email").value = cliente.email;
        document.getElementById("telefono").value = cliente.numTelefono;


    } catch (error) {
        console.error("Error cargando detalle:", error);
        alert("Error al cargar cliente");

    }
}

async function listarReservasCliente(idCliente) {
    const tabla = document.getElementById("listaReservas");
    const tbody = tabla.querySelector("tbody");;
    try {
        const url = `http://localhost:3000/api/clientes/reservasCliente?idCliente=${idCliente}`

        const res = await fetch(url);
        const data = await res.json();

        const reservasCliente = data.resultReservas;

        tbody.innerHTML = "";

        reservasCliente.forEach(reservaCliente => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${reservaCliente.codigo}</td>
                <td>${reservaCliente.tipoRegimen}</td>
                <td>${reservaCliente.dia_entrada}</td>
                <td>${reservaCliente.dia_salida}</td>
                <td>${renderEstado(reservaCliente.estado)}</td>
                <td>${reservaCliente.precio_total}</td>

            `;
            tbody.appendChild(fila);

        })

    } catch (error) {
    console.error("Error cargando reservas:", error);
    alert("Error cargando reservas");
    }

}

function renderEstado(estado) {
    switch (estado) {
        case "Pendiente":
            return `<span class="badge bg-warning text-dark">Pendiente</span>`;

        case "Confirmada":
            return `<span class="badge bg-success">Confirmada</span>`;

        case "Check-in":
            return `<span class="badge bg-primary">Check-in</span>`;

        case "Check-out":
            return `<span class="badge bg-info text-dark">Check-out</span>`;

        case "Cancelada":
            return `<span class="badge bg-danger">Cancelada</span>`;

        default:
            return `<span class="badge bg-secondary">Desconocido</span>`;
    }
}

function actualizarFilaCliente(id, nombre, apellido, email) {

    const fila = document.querySelector(`tr[data-id="${id}"]`);

    if (!fila) return;

    fila.innerHTML = `
        <td>${nombre} ${apellido}</td>
        <td>${email}</td>
        <td class="text-end">
            <button class="btn btn-sm btn-outline-primary btn-ver" data-id="${id}">
                Ver
            </button>
            <button class="btn btn-sm btn-outline-danger btn-borrar" data-id="${id}">
                Borrar
            </button>
        </td>
    `;
}

async function borrarCliente(idCliente, boton) {
    const confirmar = confirm("¿Seguro que quieres eliminar este cliente?");
    if (!confirmar) return;
    try {
        const url = `http://localhost:3000/api/clientes/delete/${idCliente}`;

        const res = await fetch(url, {
            method: "DELETE"
        })

        const data = await res.json();

        if (data.error) {
            alert("Error al eliminar cliente");
            return;
        }

        // 🧹 Eliminar fila de la tabla (sin recargar)
        const fila = boton.closest("tr");
        fila.remove();

        alert("Cliente eliminado correctamente");

    } catch (error) {
        console.error("Error eliminando cliente:", error);
        alert("Error de conexión con el servidor");

    }

}
document.getElementById("detalleCliente").addEventListener("submit", async function (e) {
    e.preventDefault();

    const nombre = document.getElementById("nombreCliente").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const dni = document.getElementById("dni").value.trim();
    const email = document.getElementById("email").value.trim();
    const numTelefono = document.getElementById("telefono").value.trim();
    const contrasena = "";

    try {
        const url = `http://localhost:3000/api/clientes/update/${clienteActualId}`;

        const body = { nombre, apellido, dni, email, numTelefono, contrasena };

        const res = await fetch(url, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();

        if (data.error) {
            alert("Error al modificar el cliente");
            return;
        }

        alert("Cliente modificado correctamente");

        // 🔁 refrescar vista
        cargarDetalleCliente(clienteActualId);

        actualizarFilaCliente(
            clienteActualId,
            nombre,
            apellido,
            email
        );

    } catch (error) {
        console.error(error);
        alert("Error de conexión");
    }
});