const db = require("../../db");

function getAllAgencias(req,res){
    db.query("Select * from Agencia", (err,result) =>{
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, result });
    })
}

function getNombreAgencia(req, res){
    const {cif} = req.query;

    db.query("Select * from Agencia where cif = ?",[cif], (err,res) =>{
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, result });
    })
}

function inicioSesionAgencia(req, res){
   
    const {email, contrasena,cif } = req.query;
    //Validar que los parametros del url si estan todos y si son validos
    if (!email || !contrasena || !cif) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Se realiza la consulta para obtener el id del cliente
    db.query("Select * from agencia where email = ? and contrasena= ? and cif=?", [email,contrasena,cif], (err, agencia) => {
        if (err) return res.status(500).json({ error: true, message: "Error con el servidor" });
        return res.status(200).json({ error: false, agencia });
    });

}

function crearAgencia(){
    const { nombreAgencia, url, cif, email, numTelefono, contrasena } = req.body;

    if (!nombreAgencia || !url || !numTelefono || cif === undefined ||!email || !contrasena) {
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
            [nombreAgencia, url, cif, email, numTelefono ],
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

function getReservasAgencia(req, res){


}

function getReservasClienteAgencia(req, res){
    
}

module.exports = {getAllAgencias, getNombreAgencia, inicioSesionAgencia, crearAgencia};