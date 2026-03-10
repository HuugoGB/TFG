const db = require("../../db");

// Mapeo de códigos válidos → número de camas por defecto
const tiposHabitacion = {
    "DV": { camas: 2},
    "DB": { camas: 2},
    "DVS": { camas: 2},
    "TR": { camas: 3},
    "TL": { camas: 3},
    "QUA": { camas: 4}
};

function createHabitaciones(req, res) {
    const { cantidad } = req.params;
    const { codigo } = req.body;

    if (!codigo || !cantidad) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    const cantidadHabs = parseInt(cantidad);

    //Validar que codigo es un tipo de habitacion existente
    db.query("Select * from tipo_hab where codigo= ?", [codigo], (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        if (result.length === 0) return res.status(404).json({ error: true, message: "El codigo del tipo de habitacion no existe" });

        //Buscamos el ultimo numero de habitacion del tipo de habitacion
        db.query("Select MAX(numero_hab) as ultimaHab from habitacion ", (err, resultadoUltimaHab) => {
            if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
            numeroHab = resultadoUltimaHab[0].ultimaHab || 1000;
            const nuevasHabitaciones = [];

            // Generamos las habitaciones
            for (let i = 1; i <= cantidadHabs; i++) {
                nuevasHabitaciones.push([
                    numeroHab + i,       
                    tiposHabitacion[codigo].camas,             
                    "",     
                    codigo                  
                ]);
            }
            db.query("Insert into habitacion (numero_hab, camas, observaciones, codigo) values ?", [nuevasHabitaciones], (err, resultHabs) => {
                if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
                return res.status(201).json({ error: false, insertadas: resultHabs.affectedRows, habitaciones_creadas: resultHabs });
            });
        });
    });

}

function disponibilidadHabitacion(req, res){
    //Valdiar que los datos son correctos y validos para la consulata
    const {dia_entrada,dia_salida,codigo} = req.query;
    if(!dia_entrada || !dia_salida || !codigo) return res.status(400).json({error: true, message: "Faltan campos obligatorios"});
    //Validar que las fechas son correctas y validas
    const checkIn = new Date(dia_entrada);
    const checkOut = new Date(dia_salida);
    if (isNaN(checkIn) || isNaN(checkOut) || checkIn >= checkOut) {
        return res.status(400).json({ error: true, message: "Las fechas son incorrectas" });
    }

    //Validamos que el tipo de habitacion existe
    db.query("Select * from tipo_hab where codigo = ?", [codigo], (err, resultTipoHab) => {
        if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
        if(resultTipoHab.length === 0) return res.status(404).json({error: true, message: "El tipo de habitacion no existe"});

        //Consultamos la disponibilidad de habitaciones en las fechas indicadas
        const sql = 'SELECT h.* FROM habitacion h LEFT JOIN reserva r ON h.idHabitacion = r.idHabitacion AND r.dia_entrada <= ? AND r.dia_salida >= ? WHERE h.codigo = ? AND r.idReserva IS NULL ORDER BY h.numero_hab;'
        db.query(sql,[dia_salida,dia_entrada,codigo], (err, resultDisponibilidad) =>{
            if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
            if( resultDisponibilidad.length === 0) return res.status(200).json({error: false, message: "No hay habitaciones disponibles"});
            return res.status(200).json({error: false, resultDisponibilidad});
        })

    });

    
}

module.exports = { createHabitaciones, disponibilidadHabitacion };