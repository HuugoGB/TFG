const db = require("../../db");

function getAllTipoHab(req, res) {
    db.query("Select * from tipo_hab", (err, resultTipoHab) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, resultTipoHab });
    })
}

function getTipoHabPorPax(req, res){
    const {pax} = req.params;

    if (!pax) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });


    db.query("Select * from tipo_hab where pax = ?",[pax], (err, resultTipoHab) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, resultTipoHab });
    })
}

function createTipoHab(req, res) {
    const { codigo, denominacion, precio, pax } = req.body;
    //Validar que estan todos los elementos de la tabla de tipo de habitacion
    if (!codigo || !denominacion || !precio || !pax) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Consultamos que el tipo de habitacion no exista
    db.query("Select * from tipo_hab where codigo = ?", [codigo], (err, resultTipoHab) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        if (resultTipoHab.length !== 0) return res.status(404).json({ error: true, message: "El tipo de habitacion ya esta creado" });

        //Creamos el nuevo tipo de habitacion
        db.query("Insert into tipo_hab (codigo, denominacion, precio, pax) Values (?,?,?,?)", [codigo, denominacion, precio, pax], (err) => {
            if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
            return res.status(201).json({ error: false, message: "Nuevo tipo de habitacion creado" });
        });
    });

}

function disponibilidadTipoHab(req, res) {
    const { pax, dia_entrada, dia_salida } = req.query;

    if (!pax || !dia_entrada || !dia_salida) {
        return res.status(400).json({ error: true, message: "Faltan parámetros" });
    }

    const f1 = new Date(dia_entrada);
    const f2 = new Date(dia_salida);

    if (isNaN(f1.getTime()) || isNaN(f2.getTime()) || f1 >= f2) {
        return res.status(400).json({ error: true, message: "Las fechas son incorrectas" });
    }

    db.query(
        `SELECT
    th.precio,
    th.codigo,
    th.denominacion,
    th.pax,
    COUNT(h.idHabitacion) AS total_habitaciones,
    COUNT(h.idHabitacion) - IFNULL(r.reservas, 0) AS habitaciones_disponibles
FROM tipo_hab th
INNER JOIN habitacion h
    ON h.codigo = th.codigo
LEFT JOIN (
    SELECT
        codigo,
        COUNT(*) AS reservas
    FROM reserva
    WHERE dia_entrada < ?
      AND dia_salida > ?
    GROUP BY codigo
) r ON r.codigo = th.codigo
WHERE th.pax = ?
GROUP BY
    th.codigo,
    th.denominacion,
    th.pax
HAVING habitaciones_disponibles > 0;


        `,
        [dia_salida, dia_entrada, pax],
        (err, result) => {
            if (err) {
                console.error(err);
                return res.status(500).json({ error: true, message: "Error en el servidor" });
            }
            return res.status(200).json({ error: false, result });
        }
    );
}



module.exports = { getAllTipoHab, getTipoHabPorPax, createTipoHab, disponibilidadTipoHab }