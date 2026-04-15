const e = require("express");
const db = require("../../db");

const ESTADOS = [
    "Pendiente",
    "Confirmada",
    "Check-in",
    "Check-out",
    "Cancelada"
];

function estadoValido(estado) {
    return ESTADOS.includes(estado);
}

function cambiarEstadoReserva(reserva, nuevoEstado) {

    if (!estadoValido(nuevoEstado)) {
        throw new Error("Estado no válido");
    }

    if (reserva.estado === "Cancelada") {
        throw new Error("No se puede modificar una reserva cancelada");
    }

    // Reglas de transición
    const TRANSICIONES = {
        Pendiente: ["Confirmada", "Cancelada"],
        Confirmada: ["Check-in", "Cancelada"],
        "Check-in": ["Check-out"],
        "Check-out": [],
        Cancelada: []
    };

    if (!TRANSICIONES[reserva.estado].includes(nuevoEstado)) {
        throw new Error(`No se puede pasar de ${reserva.estado} a ${nuevoEstado}`);
    }

    return nuevoEstado;
}

function getAllReservas(req, res) {
    db.query("Select * from Reserva", (err, resultReservas) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, resultReservas });
    })

}

function getReservas(req, res) {

    const { campo, valor } = req.query;

    // Validar parámetros
    if (!campo || !valor) {
        return res.status(400).json({
            error: true,
            message: "Faltan campos obligatorios"
        });
    }

    // Campos permitidos
    const camposValidos = ["idReserva", "cliente", "habitacion", "codigo", "cif", "regimen", "pagado", "dia_entrada", "dia_salida"];

    if (!camposValidos.includes(campo)) {
        return res.status(400).json({
            error: true,
            message: "Campo no válido"
        });
    }

    // Validar idCliente numérico
    if (campo === "idReserva" && isNaN(valor)) {
        return res.status(400).json({
            error: true,
            message: "El idReserva debe ser numérico"
        });
    }

    // Construir query dinámica
    const sql = `SELECT * FROM Reserva WHERE ${campo} = ?`;

    db.query(sql, [valor], (err, reservas) => {

        if (err) {
            return res.status(500).json({
                error: true,
                message: "Error en el servidor"
            });
        }

        return res.status(200).json({
            error: false,
            resultReservas: reservas
        });

    });
}

function createReserva(req, res) {
    const { dia_entrada, dia_salida, totalPersonas, tipoRegimen, codigo, idCliente, cif, pagado } = req.body;

    //Validar que todos los datos se han insertado en el endpoint
    if (dia_entrada === undefined ||
        dia_salida === undefined ||
        totalPersonas === undefined ||
        tipoRegimen === undefined ||
        codigo === undefined ||
        idCliente === undefined ||
        cif === undefined ||
        pagado === undefined) {
        return res.status(400).json({ error: true, message: "Faltan campos obligatorios para crear la reserva" })
    }

    //Validar que las fechas son correctas y validas
    const checkIn = new Date(dia_entrada);
    const checkOut = new Date(dia_salida);
    if (isNaN(checkIn) || isNaN(checkOut) || checkIn >= checkOut) {
        return res.status(400).json({ error: true, message: "Las fechas son incorrectas" });
    }


    //Validar que la cantidad de personas que quieren reservar una habitacion pueden entrar en el tipo seleccionado
    db.query("Select codigo,pax, precio from tipo_hab Where codigo = ?", [codigo], (err, regimenResult) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
        if (regimenResult === 0) return res.status(404).json({ error: true, message: "El tipo de habitacion no existe" });

        const tipoHab = regimenResult[0];
        if (totalPersonas > tipoHab.pax) {
            return res.status(400).json({ error: true, message: "La cantidad de personas es superior al de los clientes permitidos en la hab" });
        }

        //Validar el tipo de regimen seleccionado
        db.query("Select tiporegimen, precio from regimen where tipoRegimen = ?", [tipoRegimen], (err, tipohabResult) => {
            if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
            if (tipohabResult === 0) return res.status(404).json({ error: true, message: "El tipo de regimen no existe" });

            const regimen = tipohabResult[0];

            //Validar que el cliente existe
            db.query("Select * from Cliente where idCliente= ?", [idCliente], (err, clienteResult) => {
                if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
                if (clienteResult === 0) return res.status(404).json({ error: true, message: "El cliente no existe" });


                //Validar que la agencia existe
                db.query("Select * from Agencia where cif= ?", [cif], (err, agenciaResult) => {
                    if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
                    if (agenciaResult === 0) return res.status(404).json({ error: true, message: "La agencia no existe" });

                    //Calcular el precio total de la reserva
                    const dias = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
                    const precioTotal = (regimen.precio + tipoHab.precio) * dias;
                    const consulta = "Insert into Reserva (dia_entrada, dia_salida, pagado, precio_total, totalPersonas, codigo, tipoRegimen, idCliente, idHabitacion, cif, estado) values (?, ?, ?, ?, ?, ?, ?, ?, null, ?, 'Pendiente')";
                    //Insertar la nueva reserva
                    db.query(consulta, [checkIn, checkOut, pagado, precioTotal, totalPersonas, codigo, tipoRegimen, idCliente, cif], (err, result) => {
                        if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
                        return res.status(201).json({ message: "Reserva creada", reservaId: result.insertId });

                    });
                });
            });

        });
    });

}

function getAllReservasEnFechas(req, res) {
    const { dia_1, dia_2 } = req.query;

    //Validar que todos los datos se han insertado en el endpoint
    if (!dia_1 || !dia_2) return res.status(400).json({ error: true, message: "Faltan campos obligatorios buscar las reservas" });

    //Parsean los datos en fechas y se confirman que estan bien parseados
    const primerDia = new Date(dia_1);
    const segundoDia = new Date(dia_2);
    if (isNaN(primerDia) || isNaN(segundoDia) || primerDia >= segundoDia) return res.status(400).json({ error: true, message: "Las fechas son incorrectas" });

    //Se hace la consulta a la base de datos y se muestran todas las reserva que haya entre las fechas indicadas
    db.query("SELECT * FROM reserva where reserva.dia_entrada >= ? AND reserva.dia_salida <= ?;", [primerDia, segundoDia], (err, reservas) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el sistema cliente" });
        return res.status(200).json({ error: false, totalReservas: reservas.length, reservas: reservas })
    })


}

function deleteReserva(req, res) {
    const { idReserva } = req.params;

    if (!idReserva) return res.status(400).json({ error: true, message: "Faltan campos obligatorios." });

    db.query("Select * from Reserva where idReserva = ?", [idReserva], (err, reservaResult) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        if (reservaResult.length === 0) return res.status(404).json({ error: true, message: "La reserva no existe" });

        const reserva = reservaResult[0];

        // 🔥 NO BORRAR SI YA ESTÁ EN USO
        if (reserva.estado === "Check-in" || reserva.estado === "Check-out") {
            return res.status(400).json({
                error: true,
                message: "No se puede eliminar una reserva en uso o finalizada"
            });
        }

        db.query("Delete from reserva where idReserva = ?", [idReserva], (err, result) => {
            if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
            return res.status(200).json({ error: false, message: "Reserva borrada satisfactoriamente" });
        });

    });
}

function updateReserva(req, res) {
    const { idReserva } = req.params;
    let { dia_entrada, dia_salida, pagado, totalPersonas, codigo, tipoRegimen, cif, idCliente, idHabitacion, estado } = req.body;

    if (!idReserva) {
        return res.status(400).json({ error: true, message: "Falta el ID de la reserva" });
    }

    db.query("SELECT * FROM reserva WHERE idReserva = ?", [idReserva], (err, resultReserva) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });

        if (resultReserva.length === 0) {
            return res.status(404).json({ error: true, message: "La reserva no existe" });
        }

        const reservaActual = resultReserva[0];

        // 🔥 VALIDAR ESTADO
        /*
        if (estado && estado !== reservaActual.estado) {
            try {
                estado = cambiarEstadoReserva(reservaActual, estado);
            } catch (error) {
                return res.status(400).json({ error: true, message: error.message });
            }
        } else {
            estado = reservaActual.estado;
        }
        */
       if(!estadoValido(estado)) return res.status(404).json({ error: true, message: "El estado no es valido" });

        // Mantener valores si no vienen
        dia_entrada = dia_entrada || reservaActual.dia_entrada;
        dia_salida = dia_salida || reservaActual.dia_salida;
        pagado = (pagado === undefined || pagado === "") ? reservaActual.pagado : pagado;
        totalPersonas = totalPersonas || reservaActual.totalPersonas;
        codigo = codigo || reservaActual.codigo;
        tipoRegimen = tipoRegimen || reservaActual.tipoRegimen;
        cif = cif || reservaActual.cif;
        idCliente = idCliente || reservaActual.idCliente;
        idHabitacion = idHabitacion || reservaActual.idHabitacion;
        estado = estado || reservaActual.estado;

        db.query(
            `UPDATE reserva 
             SET dia_entrada = ?, dia_salida = ?, pagado = ?, totalPersonas = ?, 
                 codigo = ?, tipoRegimen = ?, cif = ?, idCliente = ?, idHabitacion = ?, estado = ?
             WHERE idReserva = ?`,
            [dia_entrada, dia_salida, pagado, totalPersonas, codigo, tipoRegimen, cif, idCliente, idHabitacion, estado, idReserva],
            (err) => {
                if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });

                return res.status(200).json({ error: false, message: "Reserva modificada satisfactoriamente" });
            }
        );
    });
}

function updateCampoReserva(req, res) {

    const {idReserva} = req.params;
    const {campo, valor} = req.body;

    // Validar parámetros
    if (!campo || !valor) {
        return res.status(400).json({
            error: true,
            message: "Faltan campos obligatorios"
        });
    }

    // Campos permitidos
    const camposValidos = ["idReserva", "cliente", "habitacion", "codigo", "cif", "regimen", "pagado", "dia_entrada", "dia_salida"];

    if (!camposValidos.includes(campo)) {
        return res.status(400).json({
            error: true,
            message: "Campo no válido"
        });
    }

    // Validar idCliente numérico
    if (campo === "idReserva" && isNaN(valor)) {
        return res.status(400).json({
            error: true,
            message: "El idReserva debe ser numérico"
        });
    }

    // Construir query dinámica
    const sql = `Update Reserva set ${campo} = ? where idReserva=?`;

    db.query(sql, [valor, idReserva], (err, reservas) => {

        if (err) {
            return res.status(500).json({
                error: true,
                message: "Error en el servidor"
            });
        }

        return res.status(200).json({
            error: false,
            resultReservas: reservas
        });

    });
}

function asignarHabitacion(req, res) {
    //Antes de ejecutar este endpoint, siempre se le pasan una habitacion y una reserva que se han confirmado con el de disponibilidadHabitacion
    const { idHabitacion } = req.body;
    const { idReserva } = req.params;

    if (!idHabitacion || !idReserva) return res.status(400).json({ error: true, message: "Falta campos obligatorios" });

    //Valida que tanto la habitacion como la reserva existen
    db.query("Select * from habitacion where idHabitacion = ?", [idHabitacion], (err, resultHab) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        if (resultHab.length === 0) return res.status(404).json({ error: true, message: "La habitacion no existe" });
        db.query("Select * from reserva where idReserva = ?", [idReserva], (err, resultReserva) => {
            if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
            if (resultReserva.length === 0) return res.status(404).json({ error: true, message: "La reserva no existe" });

            //Actualizamos la reserva asignando la habitacion
            db.query("Update reserva set idHabitacion = ? where idReserva = ?", [idHabitacion, idReserva], (err) => {
                if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
                return res.status(200).json({
                    error: false,
                    message: "Reserva actualizada satisfactoriamente"
                })

            })

        });
    });
}

function cambiarEstado(req, res) {
    const { idReserva } = req.params;
    const { estado } = req.body;

    db.query("SELECT * FROM reserva WHERE idReserva = ?", [idReserva], (err, result) => {
        if (err) return res.status(500).json({ error: true });

        if (result.length === 0) {
            return res.status(404).json({ error: true, message: "Reserva no encontrada" });
        }

        const reserva = result[0];

        try {
            //const nuevoEstado = cambiarEstadoReserva(reserva, estado);

            db.query(
                "UPDATE reserva SET estado = ? WHERE idReserva = ?",
                [estado, idReserva],
                (err) => {
                    if (err) return res.status(500).json({ error: true });

                    return res.status(200).json({
                        error: false,
                        message: "Estado actualizado correctamente"
                    });
                }
            );

        } catch (error) {
            return res.status(400).json({ error: true, message: error.message });
        }
    });
}


module.exports = { getAllReservas, getReservas, createReserva, getAllReservasEnFechas, deleteReserva, updateReserva,updateCampoReserva, asignarHabitacion, cambiarEstado };
