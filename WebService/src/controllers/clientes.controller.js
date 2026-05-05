const db = require("../../db");

function getAllClientes(req,res){
    db.query("Select * from Cliente", (err, resultClientes) =>{
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, resultClientes });
    })

}

function createCliente(req, res) {
    const { nombre, apellido, dni, cif, email, contrasena, numTelefono } = req.body;

    if (!nombre || !apellido || !dni || cif === undefined ||!email || !contrasena || !numTelefono) {
        return res.status(400).json({
            error: true,
            message: "Faltan campos obligatorios"
        });
    }

    //Comprobar si el email ya existe
    db.query("SELECT * FROM cliente WHERE email = ?", [email], (err, results) => {
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
            "INSERT INTO cliente (nombre, apellido, dni,cif, email, contrasena, numTelefono) VALUES (?,?,?,?,?,?,?)",
            [nombre, apellido, dni,cif, email, contrasena, numTelefono],
            (err, result) => {
                if (err) {
                    return res.status(500).json({
                        error: true,
                        message: "Error con el servidor"
                    });
                }

                return res.status(201).json({
                    error: false,
                    clienteId: result.insertId
                });
            }
        );
    });
}

function inicioSesionCliente(req,res){
    const {email, contrasena, cif } = req.query;
    //Validar que los parametros del url si estan todos y si son validos
    if (!email || !contrasena) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Se realiza la consulta para obtener el id del cliente
    db.query("Select idCliente from cliente where email = ? and contrasena= ? and cif=?", [email,contrasena,cif], (err, cliente) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        return res.status(200).json({ error: false, cliente });
    });
}

function getCliente(req, res) {

    const { campo, valor } = req.query;

    // Validar parámetros
    if (!campo || !valor) {
        return res.status(400).json({
            error: true,
            message: "Faltan campos obligatorios"
        });
    }

    // Campos permitidos
    const camposValidos = ["idCliente", "nombre", "apellido", "dni","cif","email","contrasena"];

    if (!camposValidos.includes(campo)) {
        return res.status(400).json({
            error: true,
            message: "Campo no válido"
        });
    }

    // Validar idCliente numérico
    if (campo === "idCliente" && isNaN(valor)) {
        return res.status(400).json({
            error: true,
            message: "El idCliente debe ser numérico"
        });
    }

    // Construir query dinámica
    const sql = `SELECT * FROM cliente WHERE ${campo} = ?`;

    db.query(sql, [valor], (err, cliente) => {

        if (err) {
            return res.status(500).json({
                error: true,
                message: "Error en el servidor"
            });
        }

        return res.status(200).json({
            error: false,
            resultCliente: cliente
        });

    });
}

function updateCliente(req, res) {
    const { idCliente } = req.params;
    var { nombre, apellido, dni, cif, email, contrasena, numTelefono } = req.body;
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
        const nuevoEmail = email || cliente.email;
        const nuevoContrasena = contrasena || cliente.contrasena;
        const nuevoNumTelefono = numTelefono || cliente.numTelefono;

        //Comprobamos que el cif de la agencia si no este vacio, sea uno valido
        if (cif !== undefined && cif !== null && cif !== "") {
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
                "UPDATE cliente SET nombre=?, apellido=?, dni=?, cif=?, email=?,numTelefono=?, contrasena=? WHERE idCliente=?",
                [nuevoNombre, nuevoApellido, nuevoDni, nuevoCif,nuevoEmail, nuevoNumTelefono, nuevoContrasena, idCliente],
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
    const { idCliente } = req.query;

    if (!idCliente) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });
    //Se hace una consulta para confirmar que la reserva existe
    db.query("Select * from cliente where idCliente = ?", [idCliente], (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        if (result.length === 0) return res.status(404).json({ error: true, message: "El id del cliente no existe" });

        //Una vez confirmado, se leen todas las reserva del cliente
        db.query("SELECT dia_entrada,dia_salida,pagado,precio_total,totalPersonas,codigo,tipoRegimen,idReserva,estado FROM reserva JOIN cliente ON reserva.idCliente = cliente.idCliente AND cliente.idCliente = ?;", [idCliente], (err, resultReservas) => {
            if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
            return res.status(200).json({ error: false, resultReservas });
        })


    });
}

function getReservasClienteEnVigor(req, res) {
    const { idCliente } = req.query;

    if (!idCliente) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });
    //Se hace una consulta para confirmar que la reserva existe
    db.query("Select * from cliente where idCliente = ?", [idCliente], (err, result) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        if (result.length === 0) return res.status(404).json({ error: true, message: "El id del cliente no existe" });

        //Una vez confirmado, se leen todas las reserva del cliente
        db.query("SELECT dia_entrada,dia_salida,pagado,precio_total,totalPersonas,codigo,tipoRegimen,idReserva FROM reserva JOIN cliente ON reserva.idCliente = cliente.idCliente Where cliente.idCliente = ? AND reserva.dia_entrada >= CURDATE()", [idCliente], (err, resultReservas) => {
            if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
            return res.status(200).json({ error: false, resultReservas });
        })


    });
}

module.exports = { getAllClientes, createCliente, inicioSesionCliente,getCliente, updateCliente, deleteCliente, getReservasCliente, getReservasClienteEnVigor };  