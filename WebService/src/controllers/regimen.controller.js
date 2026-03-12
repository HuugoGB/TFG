const db = require("../../db");

function getAllRegimenes(req, res) {
    db.query("Select * from regimen", (err, resultRegimen) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, resultRegimen });
    })

}

function getPrecioRegimen(req, res) {
    const { tipoRegimen } = req.query;
    if (!tipoRegimen) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    db.query("Select precio from regimen where tipoRegimen = ?", [tipoRegimen], (err, resultPrecioRegimen) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({
            error: false,
            precioRegimen: resultPrecioRegimen.length > 0 ? resultPrecioRegimen[0].precio : 0
        });
    });
}

function createRegimen(req, res) {
    const { tipoRegimen, precio, descripcion } = req.body;
    //Validar que estan todos los elementos de la tabla de regimen
    if (!tipoRegimen || !precio || !descripcion) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Consultamos que el regimen no exista
    db.query("Select * from regimen where tipoRegimen = ?", [tipoRegimen], (err, resultRegimen) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        if (resultRegimen.length !== 0) return res.status(404).json({ error: true, message: "El regimen ya esta creado" });

        //Creamos el nuevo regimen
        db.query("Insert into regimen (tipoRegimen, precio, descripcion) Values (?,?,?)", [tipoRegimen, precio, descripcion], (err) => {
            if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
            return res.status(201).json({ error: false, message: "Nuevo regimen creado" });
        });
    });

}

function updateRegimen(req, res) {
    const { tipoRegimen } = req.params;
    const { precio, descripcion } = req.body;
    //Validamos que estan todos los elementos necesarios para hacer la modificacion
    if (!precio || !tipoRegimen || !descripcion) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    //Validamos que el tipo de regimen existe
    db.query("Select * from regimen where tipoRegimen = ?", [tipoRegimen], (err, resultRegimen) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        if (resultRegimen.length === 0) return res.status(404).json({ error: true, message: "El regimen no existe" });

        if(descripcion == "") descripcion = resultRegimen[0].descripcion;
        //Actualizamos el precio del regimen
        db.query("Update regimen set precio = ? and descripcion = ? where tipoRegimen = ?", [precio,,descripcion, tipoRegimen], (err) => {
            if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
            return res.status(200).json({ error: false, message: "Regimen modificado satisfactoriamente" });

        })
    });

}

function deleteRegimen(req, res){
    const {tipoRegimen} = req.params;
    if(!tipoRegimen) return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    db.query("DELETE FROM regimen WHERE tipoRegimen = ?", [tipoRegimen], (err, result) => {
            if (err) {
                return res.status(500).json({
                    error: true,
                    message: "Error en el servidor"
                });
            }

            if (result.affectedRows === 0) {
                return res.status(404).json({
                    error: true,
                    message: "Regimen no encontrado"
                });
            }

            return res.status(200).json({
                error: false,
                message: "Regimen borrado correctamente"
            });
        }
    );

}

module.exports = { getAllRegimenes, getPrecioRegimen, updateRegimen, createRegimen, deleteRegimen };