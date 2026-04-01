const express = require("express");
const { getAllReservas, getReservas, createReserva, getAllReservasEnFechas, deleteReserva, updateReserva, asignarHabitacion, disponibilidadHabitacion} = require("../controllers/reservas.controller");

const router = express.Router();

router.get("/",getAllReservas);
router.get("/buscar", getReservas);
router.post("/create", createReserva);
router.get("/entre_fechas", getAllReservasEnFechas);
router.delete("/delete/:idReserva", deleteReserva);
router.put("/update/:idReserva", updateReserva);
router.patch("/asignar/:idReserva", asignarHabitacion);
module.exports = router;
