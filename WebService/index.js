//CommonJS
const express = require("express");
require("dotenv").config();
const cors = require("cors");

const agenciaRoutes = require("./src/routes/agencia.routes.js")
const reservasRoutes = require("./src/routes/reservas.routes.js");
const clientesRoutes = require("./src/routes/clientes.routes.js");
const habitacionesRoutes = require("./src/routes/habitaciones.router.js");
const tipoHabitacionRoutes = require("./src/routes/tipohab.routes.js")
const regimenRoutes = require("./src/routes/regimen.routes.js");
const serivicioReservaRoutes = require("./src/routes/serviciosreserva.route.js")
const servicioExtraRoutes = require("./src/routes/serviciosextra.routes.js")
const errorHandler = require("./src/middleware/errorHandler.js");


const app = express();
app.use(express.json());

// Habilitar CORS para permitir que WordPress acceda al API
app.use(cors({
    origin: "*",  
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"]
}));

// rutas
app.use("/api/agencia",agenciaRoutes);
app.use("/api/reservas", reservasRoutes);
app.use("/api/clientes", clientesRoutes);
app.use("/api/habitaciones",habitacionesRoutes);
app.use("/api/tipo_habitacion",tipoHabitacionRoutes);
app.use("/api/regimen",regimenRoutes);
app.use("/api/servicio_reserva",serivicioReservaRoutes);
app.use("/api/servicio_extra",servicioExtraRoutes);




// health
app.get("/health", (req, res) => res.json({ status: "ok" }));

// error handler
//app.use(errorHandler);



const PORT = process.env.PORT;
app.listen(PORT, () => console.log(`API running on port ${PORT}`));