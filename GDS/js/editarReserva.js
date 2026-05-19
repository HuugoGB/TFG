document.addEventListener("DOMContentLoaded", async function () {

    const idReserva = localStorage.getItem("reservaEditarId");

    if (!idReserva) {
        alert("No hay reserva seleccionada");
        return;
    }

    // 🔥 cargar selects
    await cargarClientesSelect();
    cargarRegimenesSelect();

    // 🔥 cargar reserva
    await cargarDatosReserva(idReserva);

    // 🔥 cambio habitaciones según personas
    document.getElementById("personas")
        .addEventListener("change", async function () {

            const personas = this.value;

            await cargarHabitaciones(personas);
        });

    // 🔥 submit editar
    document.getElementById("editarReserva")
        .addEventListener("submit", editarReserva);

});
async function cargarDatosReserva(idReserva) {

    try {

        const url = `http://localhost:3000/api/reserva/buscar?campo=idReserva&valor=${idReserva}`;

        const res = await fetch(url);

        const data = await res.json();

        if (data.error) {
            alert(data.message);
            return;
        }

        const reserva = data.resultReservas[0];

        // 🔥 valores simples
        document.getElementById("personas").value = reserva.totalPersonas;
        document.getElementById("entrada").value = reserva.dia_entrada.split("T")[0];
        document.getElementById("salida").value = reserva.dia_salida.split("T")[0];
        document.getElementById("precio").value = reserva.precio_total;

        // 🔥 cargar habitaciones según personas
        await cargarHabitaciones(reserva.totalPersonas);

        // 🔥 seleccionar valores actuales
        document.getElementById("cliente").value = reserva.idCliente;
        document.getElementById("habitacion").value = reserva.codigo;
        document.getElementById("regimen").value = reserva.tipoRegimen;

    } catch (error) {

        console.error(error);

        alert("Error cargando reserva");

    }
}

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


async function cargarRegimenesSelect() {
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

        if (data.error) {
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