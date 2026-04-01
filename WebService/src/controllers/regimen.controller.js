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
    let { precio, descripcion } = req.body;

    // Validamos que precio y tipoRegimen existen
    if (!precio || !tipoRegimen || !descripcion) 
        return res.status(400).json({ error: true, message: "Faltan campos obligatorios" });

    // Buscamos el régimen actual
    db.query("SELECT * FROM regimen WHERE tipoRegimen = ?", [tipoRegimen], (err, resultRegimen) => {
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        if (resultRegimen.length === 0) 
            return res.status(404).json({ error: true, message: "El régimen no existe" });

        // Si descripcion no se envía o es vacía, mantener la actual
        if (!descripcion || descripcion.trim() === "") {
            descripcion = resultRegimen[0].descripcion;
        }

        // Si precio es vacío, mantener el actual
        if (precio === "") {
            precio = resultRegimen[0].precio;
        }

        // Actualizamos el régimen
        db.query(
            "UPDATE regimen SET precio = ?, descripcion = ? WHERE tipoRegimen = ?",
            [precio, descripcion, tipoRegimen],
            (err) => {
                if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
                return res.status(200).json({ error: false, message: "Régimen modificado satisfactoriamente" });
            }
        );
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