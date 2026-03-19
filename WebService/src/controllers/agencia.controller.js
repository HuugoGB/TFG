const db = require("../../db");

function getAllAgencias(req,res){
    db.query("Select * from Agencia", (err,result) =>{
        if (err) return res.status(500).json({ error: true, message: "Error en el servidor" });
        return res.status(200).json({ error: false, result });
    })
}

module.exports = {getAllAgencias};