const db = require("../../db");

function getAllAgencias(req, res) {
    db.query("Select * from Agencia", (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, result });
    })
}

function getNombreAgencia(req, res) {
    const { cif } = req.query;

    db.query("Select * from Agencia where cif = ?", [cif], (err, res) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, result });
    })
}

function inicioSesionAgencia(req, res) {

    const { email, contrasena, cif } = req.query;
    //Validar que los parametros del url si estan todos y si son validos
    if (!email || !contrasena || !cif) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Se realiza la consulta para obtener el id del cliente
    db.query("Select * from agencia where email = ? and contrasena= ? and cif=?", [email, contrasena, cif], (err, agencia) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        return res.status(200).json({ error: false, agencia });
    });

}

function crearAgencia() {
    const { nombreAgencia, url, cif, email, numTelefono, contrasena } = req.body;

    if (!nombreAgencia || !url || !numTelefono || cif === undefined || !email || !contrasena) {
        return res.status(400).json({
            error: true,
            message: "Faltan campos obligatorios"
        });
    }

    //Comprobar si el email ya existe
    db.query("SELECT * FROM agencia WHERE email = ?", [email], (err, results) => {
        if (err) {
            return res.status(500).json({
                error: true,
                message: "Error al comprobar el email"
            });
        }

        if (results.length > 0) {
            return res.status(400).json({
                error: true,
                message: "El email ya está registrado"
            });
        }

        //Insertar cliente si no existe
        db.query(
            "INSERT INTO agencia (nombreAgencia, url, cif, email, numTelefono, contrasena) VALUES (?,?,?,?,?,?)",
            [nombreAgencia, url, cif, email, numTelefono],
            (err, result) => {
                if (err) {
                    return res.status(500).json({
                        error: true,
                        message: "Error con el servidor"
                    });
                }

                return res.status(201).json({
                    error: false,
                    agenciaCIF: result.insertId
                });
            }
        );
    });
}

function getReservasAgenciaEnFechas(req, res) {
    const { dia_1, dia_2, cif } = req.query;

    //Validar que todos los datos se han insertado en el endpoint
    if (!dia_1 || !dia_2 || !cif) return res.status(400).json({ error: true, message: "Faltan campos obligatorios buscar las reservas" });

    //Parsean los datos en fechas y se confirman que estan bien parseados
    const primerDia = new Date(dia_1);
    const segundoDia = new Date(dia_2);
    if (isNaN(primerDia.getTime()) ||
        isNaN(segundoDia.getTime()) ||
        primerDia >= segundoDia) return res.status(400).json({ error: true, message: "Las fechas son incorrectas" });

    //Se hace la consulta a la base de datos y se muestran todas las reserva que haya entre las fechas indicadas
    db.query("SELECT * FROM reserva where reserva.dia_entrada >= ? AND reserva.dia_salida <= ? and cif=?;", [primerDia, segundoDia, cif], (err, reservasAgencia) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el sistema cliente" });
        return res.status(200).json({ error: false, totalReservas: reservasAgencia.length, reservasAgencia })
    })


}

function createReserva(req, res) {
    const { dia_entrada, dia_salida, totalPersonas, tipoRegimen, codigo, precioTotal, idCliente, cif, estado } = req.body;

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

                    const consulta = "Insert into Reserva (dia_entrada, dia_salida, pagado, precio_total, totalPersonas, codigo, tipoRegimen, idCliente, idHabitacion, cif, estado) values (?, ?, 0, ?, ?, ?, ?, ?, ?, ?)";
                    //Insertar la nueva reserva
                    db.query(consulta, [checkIn, checkOut, precioTotal, totalPersonas, codigo, tipoRegimen, idCliente, cif], (err, result) => {
                        if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
                        return res.status(201).json({ message: "Reserva creada", reservaId: result.insertId });

                    });
                });
            });

        });
    });

}

function infoReservasFecha(req, res) {
    const { fecha, cif } = req.query;
    if (!fecha || cif === null) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });
    const sql = `SELECT
    -- Reservas activas en esa fecha
    (
        SELECT COUNT(*)
        FROM reserva r
        WHERE r.cif = ?
        AND r.estado NOT IN ('Cancelada')
        AND ? BETWEEN r.dia_entrada AND r.dia_salida
    ) AS reservas,

    -- Check-ins del día
    (
        SELECT COUNT(*)
        FROM reserva r
        WHERE r.cif = ?
        AND DATE(r.dia_entrada) = ?
    ) AS checkins,

    -- Check-outs del día
    (
        SELECT COUNT(*)
        FROM reserva r
        WHERE r.cif = ?
        AND DATE(r.dia_salida) = ?
    ) AS checkouts,

    -- Total clientes
    (
        SELECT COUNT(*)
        FROM cliente c
    ) AS clientes,

    -- Ocupación Individual
    (
        SELECT COUNT(*)
        FROM reserva r
        INNER JOIN tipo_hab th 
            ON r.codigo = th.codigo
        WHERE r.cif = ?
        AND ? BETWEEN r.dia_entrada AND r.dia_salida
        AND th.denominacion LIKE '%Individual%'
    ) AS individual,

    -- Ocupación Doble
    (
        SELECT COUNT(*)
        FROM reserva r
        INNER JOIN tipo_hab th 
            ON r.codigo = th.codigo
        WHERE r.cif = ?
        AND ? BETWEEN r.dia_entrada AND r.dia_salida
        AND th.denominacion LIKE '%Doble%'
    ) AS dobles,

    -- Ocupación Triple
    (
        SELECT COUNT(*)
        FROM reserva r
        INNER JOIN tipo_hab th 
            ON r.codigo = th.codigo
        WHERE r.cif = ?
        AND ? BETWEEN r.dia_entrada AND r.dia_salida
        AND th.denominacion LIKE '%Triple%'
    ) AS triples,

    -- Ocupación Cuádruple
    (
        SELECT COUNT(*)
        FROM reserva r
        INNER JOIN tipo_hab th 
            ON r.codigo = th.codigo
        WHERE r.cif = ?
        AND ? BETWEEN r.dia_entrada AND r.dia_salida
        AND th.denominacion LIKE '%Cuadruple%'
    ) AS cuadruples,

    -- Ingresos estimados
    (
        SELECT COALESCE(SUM(r.precio_total), 0)
        FROM reserva r
        WHERE r.dia_entrada = ?
        AND r.cif = ?
    ) AS ingreso;`;
    const valores = [
        cif, fecha,
        cif, fecha,
        cif, fecha,
        cif, fecha,
        cif, fecha,
        cif, fecha,
        cif, fecha,
        fecha, cif
    ];
    db.query(sql, valores, (err, result) =>{
        if (err) return res.status(500).json({ error: true, message: "Error en el sistema" });
        return res.status(200).json({error: false, result});
    })

}


module.exports = { getAllAgencias, getNombreAgencia, inicioSesionAgencia, crearAgencia, getReservasAgenciaEnFechas, createReserva, infoReservasFecha };