const express = require("express");
const { createReserva, getAllReservasEnFechas, deleteReserva, updateReserva, asignarHabitacion, disponibilidadHabitacion} = require("../controllers/reservas.controller");

const router = express.Router();

router.post("/create", createReserva);
router.get("/entre_fechas", getAllReservasEnFechas);
router.delete("/:idReserva", deleteReserva);
router.patch("/update/:idReserva", updateReserva);
router.patch("/asignar/:idReserva", asignarHabitacion);
module.exports = router;
