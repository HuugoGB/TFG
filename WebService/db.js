const mysql = require('mysql');

const con = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    user: process.env.DB_USER || "root",
    password: "",
    database: process.env.DB_NAME || "MOTOR_RESERVAS",
    dateStrings: true
});

con.connect((err) => {
    if (err) {
        console.error("Error conectando a la base de datos:", err);
        return;
    }
    console.log("Conexión a MySQL establecida correctamente");
});

module.exports = con;