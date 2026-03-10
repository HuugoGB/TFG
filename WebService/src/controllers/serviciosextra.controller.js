const db = require("../../db");

function getAllServiciosExtra(req, res){
    db.query("Select * from servicios_extras",(err, resultServicioExtra)=>{
        if(err) return res.status(500).json({error: true, message: "Error en el servidor"});
        return res.status(200).json({error:false, resultServicioExtra});
    })

}

function getPrecioServicioExtra(req, res){
    const {idServicioExtra} = req.query;
    if(!idServicioExtra) return res.status(400).json({error: true, message: "Faltan campos obligatorios"});

    db.query("Select precio, porDia from servicios_extras where idServiciosExtras = ?", [idServicioExtra], (err, resultPrecioServicioExtra) =>{
        if(err) return res.status(500).json({error: true, message: "Error en el servidor"}); 
        return res.status(200).json({error:false, precioServicioExtra: resultPrecioServicioExtra});
    });
}

module.exports = {getAllServiciosExtra, getPrecioServicioExtra}