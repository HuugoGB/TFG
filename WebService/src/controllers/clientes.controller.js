const db = require("../../db");

function createCliente(req, res) {
    const { nombre, apellido, dni } = req.body;

    if (!nombre || !apellido || !dni) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    db.query("Insert into cliente (nombre, apellido, dni) values (?,?,?)", [nombre, apellido, dni], (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        return res.status(201).json({ error: false, clienteId: result.insertId });
    });

}

function getCliente(req, res) {
    const {nombre, apellido, dni } = req.query;
    //Validar que los parametros del url si estan todos y si son validos
    if (!nombre || !apellido || !dni) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });


    //Se realiza la consulta para obtener toda la informacion de un cliente
    db.query("Select idCliente from cliente where nombre = ? and apellido= ? and dni=?", [nombre,apellido,dni], (err, cliente) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        return res.status(200).json({ error: false, cliente });
    });

}

function updateCliente(req, res) {
    const { idCliente } = req.params;
    var { nombre, apellido, dni, cif } = req.body;
    //Validar que los parametros del url si estan todos y si son validos
    if (!idCliente) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Confirmamos que el cliente existe
    db.query("Select * from cliente where idCliente  = ?", [idCliente], (err, selectCliente) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        if (selectCliente.length === 0) return res.status(404).json({ error: true, message: "El id del cliente no existe" });

        const cliente = selectCliente[0];

        //En caso de que no se vaya a modificar alguno de esos campos, se mantienen los que ya existen, para asi poder hacer el update
         // Mantener los valores originales si no se envían nuevos
        const nuevoNombre = nombre || cliente.nombre;
        const nuevoApellido = apellido || cliente.apellido;
        const nuevoDni = dni || cliente.dni;
        const nuevoCif = cif || cliente.cif;

        //Comprobamos que el cif de la agencia si no este vacio, sea uno valido
        if (isNaN(cif)) {
            db.query("Select * from agencia where cif = ?", [cif], (err, result) => {
                if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
                if (result.length === 0) return res.status(404).json({ error: true, message: "El cif de la agencia no existe" });
                
                actualizarCliente();
            })
        }else{

            actualizarCliente();
        }

        function actualizarCliente() {
            db.query(
                "UPDATE cliente SET nombre=?, apellido=?, dni=?, cif=? WHERE idCliente=?",
                [nuevoNombre, nuevoApellido, nuevoDni, nuevoCif, idCliente],
                (err) => {
                    if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });

                    return res.status(200).json({
                        error: false,
                        message: "Cliente actualizado correctamente"
                    });
                }
            );
        }
    });
}




function deleteCliente(req, res) {
    const { idCliente } = req.params;
    //Validar que los parametros del url si estan todos y si son validos
    if (!idCliente) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Se hace una consulta para confirmar que la reserva existe
    db.query("Select * from cliente where idCliente = ?", [idCliente], (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        if (result.length === 0) return res.status(404).json({ error: true, message: "El id del cliente no existe" });

        //Una vez confirmado, se borra la reserva de la base de datos
        db.query("Delete from cliente where idCliente = ?", [idCliente], (err, resultBorrado) => {
            if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
            return res.status(200).json({ error: false, message: "Cliente borrado satisfactoriamente" });
        })


    });


}

function getReservasCliente(req, res) {
    const { idCliente } = req.params;

    if (!idCliente) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });
    //Se hace una consulta para confirmar que la reserva existe
    db.query("Select * from cliente where idCliente = ?", [idCliente], (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        if (result.length === 0) return res.status(404).json({ error: true, message: "El id del cliente no existe" });

        //Una vez confirmado, se leen todas las reserva del cliente
        db.query("SELECT dia_entrada,dia_salida,pagado,precio_total,totalPersonas,codigo,tipoRegimen FROM reserva JOIN cliente ON reserva.idCliente = cliente.idCliente AND cliente.idCliente = ?;", [idCliente], (err, resultReservas) => {
            if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
            return res.status(200).json({ error: false, resultReservas });
        })


    });



}

module.exports = { createCliente, getCliente, updateCliente, deleteCliente, getReservasCliente };  