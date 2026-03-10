const db = require("../../db");

function getAllServiciosReserva(){


}

function createServicioReserva(req, res) {
    let { idReserva, idServiciosExtra, cantidad } = req.body;

    if (!idReserva || !idServiciosExtra) {
        return res.status(400).json({
            error: true,
            message: "Faltan campos obligatorios"
        });
    }

    if (!cantidad) cantidad = 1;

    // Obtener fechas de la reserva
    db.query(
        "SELECT dia_entrada, dia_salida FROM reserva WHERE idReserva = ?",
        [idReserva],
        (err, reservaResult) => {
            if (err || reservaResult.length === 0) {
                return res.status(500).json({ error: true, message: "Reserva no encontrada" });
            }

            const diaEntrada = new Date(reservaResult[0].dia_entrada);
            const diaSalida = new Date(reservaResult[0].dia_salida);

            // Obtener servicio extra
            db.query(
                "SELECT precio, porDia FROM servicios_extras WHERE idServiciosExtras = ?",
                [idServiciosExtra],
                (err, servicioResult) => {
                    if (err || servicioResult.length === 0) {
                        return res.status(500).json({ error: true, message: "Servicio no encontrado" });
                    }

                    const { precio, porDia } = servicioResult[0];
                    let precioTotal;

                    if (porDia) {
                        const dias =
                            Math.ceil((diaSalida - diaEntrada) / (1000 * 60 * 60 * 24));
                        precioTotal = precio * dias;
                    } else {
                        precioTotal = precio;
                    }

                    // Insertar servicio en la reserva
                    db.query(
                        `INSERT INTO servicios_reserva 
                        (idReserva, idServiciosExtras, cantidad, precioTotal)
                        VALUES (?, ?, ?, ?)`,
                        [idReserva, idServiciosExtra, cantidad, precioTotal],
                        (err, resultInsert) => {
                            if (err) {
                                return res.status(500).json({ error: true, message: "Error al insertar servicio" });
                            }

                            return res.status(201).json({
                                message: "Servicio añadido a la reserva",
                                servicioReservaId: resultInsert.insertId
                            });
                        }
                    );
                }
            );
        }
    );
}

module.exports = {getAllServiciosReserva, createServicioReserva}