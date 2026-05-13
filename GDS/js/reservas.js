document.addEventListener("DOMContentLoaded", function () {

    cargarClientesSelect();
    cargarRegimenes();

    // 🔄 cambiar habitaciones según personas
    document.getElementById("personas")
        .addEventListener("change", function () {

            const personas = this.value;

            cargarHabitaciones(personas);
        });

});

async function cargarClientesSelect() {

    try {

        const cif = localStorage.getItem("agenciaCIF");

        const url = `http://localhost:3000/api/clientes/buscar?campo=cif&valor=${cif}`;

        const res = await fetch(url);

        const data = await res.json();

        if (data.error) return;

        const select = document.getElementById("cliente");

        select.innerHTML = `
            <option value="">Seleccionar cliente</option>
        `;

        data.resultCliente.forEach(cliente => {

            select.innerHTML += `
                <option value="${cliente.idCliente}">
                    ${cliente.nombre} ${cliente.apellido}
                </option>
            `;
        });

    } catch (error) {

        console.error("Error cargando clientes:", error);

    }
}


async function cargarRegimenes() {
    try {
        const url = `http://localhost:3000/api/regimen`

        const res = await fetch(url);
        const data = await res.json();

        if (data.error) {
            alert(data.message);
            return
        }

        const regimenes = data.resultRegimen;

        const select = document.getElementById("regimen");
        select.innerHTML = '<option value="">Seleccion régimen</option>';

        regimenes.forEach(regimen => {
            select.innerHTML += `<option value="${regimen.tipoRegimen}">${regimen.descripcion}</option>`;
                            

        });
    } catch (error) {
        console.error("Error cargando regimenes:", error);
        alert("Error cargando regimenes");
    }


}

async function cargarHabitaciones(personas) {
    try {
        const url = `http://localhost:3000/api/tipo_habitacion/porPax/${personas}`

        const res = await fetch(url);
        const data = await res.json();

        if(data.error){
            alert(data.message);
            return
        }

        const tipoHabitaciones = data.resultTipoHab;
        
        const select = document.getElementById("habitacion");
        select.innerHTML = `<option value="">Seleccionar habitación</option>`

        tipoHabitaciones.forEach(tipoHab => {
            select.innerHTML += `<option value="${tipoHab.codigo}">${tipoHab.denominacion}</option>`;

        });

    } catch (error) {
        console.error("Error cargando habitaciones:", error);
        alert("Error cargando habitaciones");
    }

}

async function cargarReservas() {

    const dia_1 = document.getElementById("fechaInicio").value.trim();
    const dia_2 = document.getElementById("fechaFinal").value.trim();
    const cif = localStorage.getItem("agenciaCIF");

    if (!dia_1 || !dia_2) {
        alert("Selecciona ambas fechas");
        return;
    }

    try {

        const url = `http://localhost:3000/api/agencia/reservasFechas?dia_1=${dia_1}&dia_2=${dia_2}&cif=${cif}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.error) {
            alert(data.message);
            return;
        }

        const reservasAgencia = data.reservasAgencia;

        listarReservas(reservasAgencia);

    } catch (error) {

        console.error("Error cargando reservas:", error);
        alert("Error cargando reservas");

    }

}

// 🔘 FILTRAR
document.getElementById("filtrarReservas").addEventListener("click", async function (e) {

    e.preventDefault();

    cargarReservas();

});



// 📋 LISTAR RESERVAS
function listarReservas(reservasAgencia) {

    const tbody = document.querySelector("#reservas tbody");

    tbody.innerHTML = "";

    reservasAgencia.forEach(reserva => {

        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${reserva.idReserva}</td>
            <td>${reserva.idCliente}</td>
            <td>${reserva.dia_entrada}</td>
            <td>${reserva.dia_salida}</td>
            <td>${reserva.codigo}</td>
            <td>${reserva.tipoRegimen}</td>
            <td>${renderEstado(reserva.estado)}</td>
            <td>${reserva.precio_total} €</td>
            <td>${reserva.pagado ? "Sí" : "No"}</td>
            <td>
                <button 
                    class="btn btn-sm btn-primary btn-ver"
                    data-id="${reserva.idReserva}">
                    Ver
                </button>

                <button 
                    class="btn btn-sm btn-danger btn-cancelar"
                    data-id="${reserva.idReserva}">
                    Cancelar
                </button>
            </td>
        `;

        tbody.appendChild(fila);

    });

}

let reservaActual = null;


// 🎨 ESTADOS
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


// 🖱 EVENTOS TABLA
document.addEventListener("click", function (e) {

    // 👁 VER
    if (e.target.classList.contains("btn-ver")) {

        const id = e.target.dataset.id;

        reservaActual = id;

        console.log("Reserva seleccionada:", id);

    }

    // ❌ CANCELAR
    if (e.target.classList.contains("btn-cancelar")) {

        const id = e.target.dataset.id;

        cancelarReserva(id);

    }

    if (e.target.classList.contains("btn-pendiente")) {
        const estado = "Pendiente";
        crearReserva(estado);

    }

    if (e.target.classList.contains("btn-confirmar")) {
        const estado = "Confirmada"
        crearReserva(estado);

    }

});

async function crearReserva(estado) {
    const idCliente = document.getElementById("cliente").value.trim();
    const totalPersonas = document.getElementById("personas").value.trim();
    const codigo = document.getElementById("habitacion").value.trim();
    const tipoRegimen = document.getElementById("regimen").value.trim();
    const dia_entrada = document.getElementById("entrada").value.trim();
    const dia_salida = document.getElementById("salida").value.trim();
    const precioTotal = document.getElementById("precio").value.trim();
    const cif = localStorage.getItem("agenciaCIF")

    try {
        const url = `http://localhost:3000/api/agencia/createReserva`;
        const body = { dia_entrada, dia_salida, totalPersonas, tipoRegimen, codigo, precioTotal, idCliente, cif, estado };

        const res = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
        const data = await res.json();

        if (data.error) {
            alert(data.message);
            return
        }



    } catch (error) {
        console.error("Error cancelando reserva:", error);

        alert("Error de conexión con el servidor");
    }

}


// ❌ CANCELAR RESERVA
async function cancelarReserva(idReserva) {

    const confirmar = confirm("¿Seguro que quieres cancelar esta reserva?");

    if (!confirmar) return;

    try {

        const url = `http://localhost:3000/api/reservas/cambiarEstado/${idReserva}`;

        const body = {
            estado: "Cancelada"
        };

        const res = await fetch(url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();

        if (data.error) {
            alert(data.message);
            return;
        }

        alert("Reserva cancelada correctamente");

        // 🔄 VOLVER A CARGAR RESERVAS
        cargarReservas();

    } catch (error) {

        console.error("Error cancelando reserva:", error);

        alert("Error de conexión con el servidor");

    }

}