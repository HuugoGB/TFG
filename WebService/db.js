const mysql = require('mysql');

const con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "MOTOR_RESERVAS",
    dateStrings: true,
    connectTimeout: 10000
});

con.connect((err) => {
    if (err) {
        console.error("ERROR CONECTANDO MYSQL:", err.message);
        return;
    }

    console.log("Conexión a MySQL establecida correctamente");
});

module.exports = con;