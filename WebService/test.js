const mysql = require("mysql");

const con = mysql.createConnection({
  host: "127.0.0.1",
  user: "root",
  password: "",
  database: "MOTOR_RESERVAS"
});

con.connect((err) => {
  if (err) {
    console.error("❌ ERROR:", err);
    return;
  }

  console.log("✅ CONECTADO OK");
});