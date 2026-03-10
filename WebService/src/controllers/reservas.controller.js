const db = require("../../db");

function createReserva(req, res) {
    const { dia_entrada, dia_salida, totalPersonas, tipoRegimen, codigo, idCliente } = req.body;

    //Validar que todos los datos se han insertado en el endpoint
    if (!dia_entrada || !dia_salida || !totalPersonas || !tipoRegimen || !codigo || !idCliente) {
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

                //Calcular el precio total de la reserva
                const dias = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
                const precioTotal = (regimen.precio + tipoHab.precio) * dias;
                const consulta = "Insert into Reserva (dia_entrada, dia_salida, pagado, precio_total, totalPersonas, codigo, tipoRegimen, idCliente, idHabitacion) values (?, ?, 0, ?, ?, ?, ?, ?, null)";

                //Insertar la nueva reserva
                db.query(consulta, [checkIn, checkOut, precioTotal, totalPersonas, codigo, tipoRegimen, idCliente], (err, result) => {
                    if(err) return res.status(500).json({error:true, message: "Error en el sistema" });
                    return res.status(201).json({message: "Reserva creada", reservaId: result.insertId});

                });

            });

        });
    });

}

function getAllReservasEnFechas(req,res) {
    const{dia_1, dia_2} = req.query;

    //Validar que todos los datos se han insertado en el endpoint
    if (!dia_1 || !dia_2) return res.status(400).json({ error: true, message: "Faltan campos obligatorios buscar las reservas" });

    //Parsean los datos en fechas y se confirman que estan bien parseados
    const primerDia = new Date(dia_1);
    const segundoDia = new Date(dia_2);
    if(isNaN(primerDia) || isNaN(segundoDia) || primerDia >= segundoDia) return res.status(400).json({error: true, message: "Las fechas son incorrectas"});

    //Se hace la consulta a la base de datos y se muestran todas las reserva que haya entre las fechas indicadas
    db.query("SELECT * FROM reserva where reserva.dia_entrada >= ? AND reserva.dia_salida <= ?;", [primerDia,segundoDia], (err,reservas) =>{
        if(err) return res.status(500).json({error: true, message: "Error en el sistema cliente"});
        return res.status(200).json({error: false, totalReservas: reservas.length, reservas: reservas})
    })
    

}

function deleteReserva(req, res){
    const {idReserva} = req.query;

    //Se validan los datos pasado en los parametros del endpoint
    if(!idReserva) return res.status(400).json({error:true, message:"Faltan campos obligatorios."});

    //Se hace una consulta para confirmar que la reserva existe
    db.query("Select * from Reserva where idReserva = ?", [idReserva], (err,reservaResult) =>{
        if(err) return res.status(500).json({error:true, message: "Error en el servidor"});
        if (reservaResult.length === 0) return res.status(404).json({error: true, message: "La reserva no existe"});

        //Una vez confirmado, se borra la reserva de la base de datos
        db.query("Delete from reserva where idReserva = ?", [idReserva], (err,result)=>{
            if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
            return res.status(200).json({error: false, message: "Reserva borrada satisfactoriamente"});
        });

    });
}
function updateReserva(req, res){
    const {idReserva} = req.params;
    const camposModificar= req.body;

    //Validar los datos de la url tanto los paramteros como el body
    if(!idReserva) return res.status(400).json({error: true, message: "Falta el id de la reserva"});
    if(Object.keys(camposModificar).length === 0) return res.status(400).json({error:true, message: "No hay datos que modificar"});

    //Se comprueba que la reserva exista antes de modificarlas
    db.query("Select * from reserva where idReserva =? ", [idReserva], (err, reservaResult) =>{
        if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
        if (reservaResult.length === 0) return res.status(404).json({error: true, message: "La reserva no existe"});
        
         //Crear la parte dinámica del UPDATE
        const campos = Object.keys(camposModificar);   // ej: [ "dia_salida", "totalPersonas" ]
        const valores = Object.values(camposModificar); // ej: [ "2025-03-10", 4 ]
    
        const setSQL = campos.map(c => `${c} = ?`).join(", ");

        //Ejecutar UPDATE dinámico
        const sql = `UPDATE reserva SET ${setSQL} WHERE idReserva = ?`;
        

        db.query(sql, [...valores, idReserva], (err) => { //... Asegura que se pasen todos los valores de los campos antes de la idReserva al final
            if (err)
                return res.status(500).json({ error: true, message: "Error actualizando reserva" });

            return res.json({
                error: false,
                message: "Reserva actualizada correctamente",
                camposModificados: campos
            });
        });
    });


}

function asignarHabitacion(req, res){
    //Antes de ejecutar este endpoint, siempre se le pasan una habitacion y una reserva que se han confirmado con el de disponibilidadHabitacion
    const {idHabitacion} = req.body;
    const {idReserva} = req.params;

    if(!idHabitacion || !idReserva) return res.status(400).json({error: true, message: "Falta campos obligatorios"});

    //Valida que tanto la habitacion como la reserva existen
    db.query("Select * from habitacion where idHabitacion = ?", [idHabitacion],(err, resultHab) =>{
        if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
        if(resultHab.length === 0) return res.status(404).json({error: true, message: "La habitacion no existe"});
        db.query("Select * from reserva where idReserva = ?", [idReserva], (err, resultReserva) => {
            if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
            if(resultReserva.length === 0) return res.status(404).json({error: true, message: "La reserva no existe"});

            //Actualizamos la reserva asignando la habitacion
            db.query("Update reserva set idHabitacion = ? where idReserva = ?",[idHabitacion,idReserva], (err) => {
                if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
                return res.status(200).json({
                    error: false,
                    message: "Reserva actualizada satisfactoriamente"
                })

            })

        });
    });
}


module.exports = { createReserva, getAllReservasEnFechas, deleteReserva, updateReserva, asignarHabitacion};
